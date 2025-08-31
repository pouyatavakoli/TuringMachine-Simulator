import os
import logging
from typing import Dict, List
from flask import Blueprint, render_template, jsonify, request
import re
from werkzeug.utils import secure_filename

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
    tape_data = machine.get_tape_snapshot()
    return {
        "current_state": machine.state.current_state,
        "steps": machine.state.steps,
        "halted": machine.state.halted,
        "head_position": machine.state.head_position,
        "tape": tape_data["tape"],
        "min_index": tape_data["min_index"],
        "max_index": tape_data["max_index"]
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

@main_bp.route('/create', methods=['GET'])
def create_machine_page():
    """Render the machine creation page."""
    return render_template('create.html')

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
    
@main_bp.route('/api/machines/create', methods=['POST'])
def create_machine():
    """Create a new machine definition from form data."""
    try:
        data = request.get_json(force=True)
        
        # Validate required fields
        required_fields = ['name', 'states', 'input_alphabet', 'tape_alphabet', 
                          'blank', 'initial_state', 'final_states']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f"Missing required field: {field}")
        
        # Validate transitions
        if 'transitions' not in data or not data['transitions']:
            return error_response("At least one transition is required")
        
        # Create machine definition string
        machine_name = data['name']
        states = data['states']
        input_alphabet = data['input_alphabet']
        tape_alphabet = data['tape_alphabet']
        blank = data['blank']
        initial_state = data['initial_state']
        final_states = data['final_states']
        transitions = data['transitions']
        
        # Format the machine definition
        definition = f"# Turing Machine: {machine_name}\n"
        definition += f"states: {states}\n"
        definition += f"input_alphabet: {input_alphabet}\n"
        definition += f"tape_alphabet: {tape_alphabet}\n"
        definition += f"blank: {blank}\n"
        definition += f"initial_state: {initial_state}\n"
        definition += f"final_states: {final_states}\n"
        definition += "transitions:\n"
        
        for transition in transitions:
            definition += f"{transition['current_state']},{transition['read_symbol']} -> {transition['next_state']},{transition['write_symbol']},{transition['move']}\n"
        
        # Save to file
        filename = secure_filename(machine_name.replace(" ", "_")) + ".txt"
        filepath = os.path.join(MACHINES_DIR, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            return error_response("A machine with this name already exists")
        
        with open(filepath, 'w') as f:
            f.write(definition)
        
        return jsonify({
            "status": "created",
            "message": f"Machine '{machine_name}' created successfully",
            "filename": filename
        })
        
    except Exception as e:
        logging.exception("Failed to create machine")
        return error_response(str(e))