import os
import logging
from typing import Dict, List
from flask import Blueprint, render_template, jsonify, request

from .models import TuringMachine, MachineDefinition
from .utils import parse_machine_file, create_machine_from_dict

# ------------------------
# Blueprint
# ------------------------
main_bp = Blueprint('routes', __name__)

# ------------------------
# Config & Globals
# ------------------------
MACHINES_DIR = "machines"
machines: Dict[str, TuringMachine] = {}

# ------------------------
# Helper Functions
# ------------------------
def serialize_machine_state(machine: TuringMachine) -> dict:
    """Return JSON-serializable snapshot of a TuringMachine state."""
    return {
        "current_state": machine.state.current_state,
        "steps": machine.state.steps,
        "halted": machine.state.halted,
        "head_position": machine.state.head_position,
        "tape": machine.get_tape_snapshot(),
    }

def serialize_machine_info(definition: MachineDefinition) -> dict:
    """Return JSON-serializable machine definition with consistent field names."""
    return {
        "states": list(definition.states),
        "input_alphabet": list(definition.input_alphabet),
        "tape_alphabet": list(definition.tape_alphabet),
        "blank": definition.blank,
        "initial_state": definition.initial_state,
        "final_states": list(definition.final_states),
        "transitions": [
            {
                "current_state": t.current_state,
                "read_symbol": t.read_symbol,  # Consistent field name
                "next_state": t.next_state,
                "write_symbol": t.write_symbol,
                "move": t.move.value
            }
            for t in definition.transitions
        ]
    }

def get_machine(machine_id: str) -> TuringMachine:
    """Fetch initialized machine or raise an error."""
    machine = machines.get(machine_id)
    if not machine:
        raise ValueError(f"Machine '{machine_id}' is not initialized")
    return machine

def error_response(message: str, code: int = 400):
    """Standard error JSON response."""
    return jsonify({"error": message}), code

# ------------------------
# Routes
# ------------------------
@main_bp.route('/')
def index():
    return render_template('index.html')

# api endpoint routes:

@main_bp.route('/api/machines', methods=['GET'])
def get_machines():
    """Return list of available machine files."""
    machine_files = [
        {"id": os.path.splitext(fname)[0],
         "name": os.path.splitext(fname)[0].replace("_", " ").title()}
        for fname in os.listdir(MACHINES_DIR) if fname.endswith(".txt")
    ]
    return jsonify(machine_files)


@main_bp.route('/api/init', methods=['POST'])
def initialize_machine():
    try:
        data = request.get_json(force=True)
        machine_id = data.get("machine")
        if not machine_id:
            return error_response("Missing machine ID")

        tape_str = data.get("tape", "")

        path = os.path.join(MACHINES_DIR, f"{machine_id}.txt")
        if not os.path.exists(path):
            return error_response("Machine definition not found", 404)

        # Parse definition and create TuringMachine
        definition = parse_machine_file(path)
        machine = create_machine_from_dict(definition)
        machine.reset(list(tape_str))
        machines[machine_id] = machine

        # Create a properly serialized machine info response
        machine_info = serialize_machine_info(machine.definition)

        return jsonify({
            "status": "initialized",
            "machine_id": machine_id,
            "state": serialize_machine_state(machine),
            "machine_info": machine_info  # Use serialized info instead of raw definition
        })

    except Exception as e:
        logging.exception("Failed to initialize machine")
        return error_response(str(e))

@main_bp.route('/api/reset', methods=['POST'])
def reset_machine():
    try:
        data = request.get_json(force=True)
        machine_id = data.get("machine_id")
        tape_str = data.get("tape", "")

        machine = get_machine(machine_id)
        machine.reset(list(tape_str))

        return jsonify({
            "status": "reset",
            "machine_id": machine_id,
            "state": serialize_machine_state(machine)
        })

    except Exception as e:
        logging.exception("Failed to reset machine")
        return error_response(str(e))


@main_bp.route('/api/step', methods=['POST'])
def step_machine():
    try:
        data = request.get_json(force=True)
        machine_id = data.get("machine_id")

        machine = get_machine(machine_id)
        alive = machine.step()

        return jsonify({
            "status": "stepped",
            "alive": alive,
            "state": serialize_machine_state(machine),
            "history": machine.history  # include full history
        })

    except Exception as e:
        logging.exception("Failed to step machine")
        return error_response(str(e))


@main_bp.route('/api/run', methods=['POST'])
def run_machine():
    try:
        data = request.get_json(force=True)
        machine_id = data.get("machine_id")
        max_steps = int(data.get("max_steps", 1000))

        machine = get_machine(machine_id)
        machine.run(max_steps)

        return jsonify({
            "status": "ran",
            "halted": machine.state.halted,
            "state": serialize_machine_state(machine),
            "history": machine.history  # include full history
        })

    except ValueError:
        return error_response("max_steps must be an integer")
    except Exception as e:
        logging.exception("Failed to run machine")
        return error_response(str(e))