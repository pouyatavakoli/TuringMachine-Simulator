from flask import Blueprint,render_template, jsonify, request
from .utils import *
import os

main_bp = Blueprint('routes', __name__)
MACHINES_DIR = "machines"
machines: Dict[str, TuringMachine] = {}

@main_bp.route('/')
def index():
    return render_template('index.html')

# api endpoint routes:

@main_bp.route('/api/machines', methods=['GET'])
def get_machines():
    """List available machine files"""
    result = []
    for fname in os.listdir(MACHINES_DIR):
        if fname.endswith(".txt"):
            machine_id = os.path.splitext(fname)[0]
            result.append({"id": machine_id, "name": machine_id.replace("_", " ").title()})
    return jsonify(result)

@main_bp.route('/api/init', methods=['POST'])
def initialize_machine():
    data = request.get_json(force=True)
    machine_id = data.get("machine")
    tape_str = data.get("tape", "")

    path = os.path.join(MACHINES_DIR, f"{machine_id}.txt")
    if not os.path.exists(path):
        return jsonify({"error": "machine definition not found"}), 404

    try:
        definition = parse_machine_file(path)
        machine = create_machine_from_dict(definition)
        machine.reset(initial_tape=list(tape_str))
        machines[machine_id] = machine
    except Exception as e:
        #import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "status": "initialized",
        "machine_id": machine_id,
        "state": {
            "current_state": machine.state.current_state,
            "steps": machine.state.steps,
            "halted": machine.state.halted,
            "head_position": machine.state.head_position,
            "tape": machine.get_tape_snapshot()
        },
        "machine_info": definition
    })

@main_bp.route('/api/reset', methods=['POST'])
def reset_machine():
    data = request.get_json(force=True)
    machine_id = data.get("machine_id")
    tape_str = data.get("tape", "")

    if machine_id not in machines:
        return jsonify({"error": "Machine not initialized"}), 400

    try:
        machines[machine_id].reset(list(tape_str))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    machine = machines[machine_id]
    return jsonify({
        "status": "reset",
        "machine_id": machine_id,
        "state": {
            "current_state": machine.state.current_state,
            "steps": machine.state.steps,
            "halted": machine.state.halted,
            "head_position": machine.state.head_position,
            "tape": machine.get_tape_snapshot()
        }
    })


@main_bp.route('/api/step', methods=['POST'])
def step_machine():
    data = request.get_json(force=True)
    machine_id = data.get("machine_id")

    if machine_id not in machines:
        return jsonify({"error": "Machine not initialized"}), 400

    machine = machines[machine_id]
    alive = machine.step()  # returns False if halted

    return jsonify({
        "status": "stepped",
        "alive": alive,
        "state": {
            "current_state": machine.state.current_state,
            "steps": machine.state.steps,
            "halted": machine.state.halted,
            "head_position": machine.state.head_position,
            "tape": machine.get_tape_snapshot()
        }
    })


@main_bp.route('/api/run', methods=['POST'])
def run_machine():
    data = request.get_json()
    machine_id = data.get("machine_id")
    # TODO: complete this 
    return jsonify({"status": "ran"})
