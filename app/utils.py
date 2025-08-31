from typing import Dict, Any, List
from app import models
from .models import TuringMachine, MachineDefinition, Transition, MoveDirection

def create_machine_from_dict(definition_dict: Dict[str, Any]) -> TuringMachine:
    """
    Create a TuringMachine object from a parsed definition dictionary.
    Ensures transitions and states are mapped correctly.
    """
    transitions: List[Transition] = []
    for t in definition_dict['transitions']:
        try:
            transitions.append(Transition(
                current_state=t['current_state'],
                read_symbol=t['read_symbol'],
                next_state=t['next_state'],
                write_symbol=t['write_symbol'],
                move=MoveDirection(t['move'])
            ))
        except ValueError as e:
            raise ValueError(f"Invalid move direction in transition {t}: {e}")

    definition = MachineDefinition(
        states=set(definition_dict['states']),
        input_alphabet=set(definition_dict['input_alphabet']),
        tape_alphabet=set(definition_dict['tape_alphabet']),
        blank=definition_dict['blank'],
        initial_state=definition_dict['initial_state'],
        final_states=set(definition_dict['final_states']),
        transitions=transitions,
    )
    return TuringMachine(definition=definition)


def parse_machine_file(path: str) -> Dict[str, Any]:
    """
    Parse a Turing Machine definition from a .txt file into dictionary format.
    Format:
        states: q0,q1,halt
        input_alphabet: 0,1
        tape_alphabet: 0,1,□
        blank: □
        initial_state: q0
        final_states: halt
        q0,1 -> q1,1,R
    """
    definition: Dict[str, Any] = {
        "states": [],
        "input_alphabet": [],
        "tape_alphabet": [],
        "blank": None,
        "initial_state": None,
        "final_states": [],
        "transitions": []
    }

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("states:"):
                definition["states"] = [s.strip() for s in line.split(":", 1)[1].split(",")]
            elif line.startswith("input_alphabet:"):
                definition["input_alphabet"] = [s.strip() for s in line.split(":", 1)[1].split(",")]
            elif line.startswith("tape_alphabet:"):
                definition["tape_alphabet"] = [s.strip() for s in line.split(":", 1)[1].split(",")]
            elif line.startswith("blank:"):
                definition["blank"] = line.split(":", 1)[1].strip()
            elif line.startswith("initial_state:"):
                definition["initial_state"] = line.split(":", 1)[1].strip()
            elif line.startswith("final_states:"):
                definition["final_states"] = [s.strip() for s in line.split(":", 1)[1].split(",")]
            elif "->" in line:
                try:
                    left, right = line.split("->")
                    current_state, read_symbol = [x.strip() for x in left.split(",")]
                    next_state, write_symbol, move = [x.strip() for x in right.split(",")]
                except ValueError:
                    raise ValueError(f"Malformed transition line: {line}")
                definition["transitions"].append({
                    "current_state": current_state,
                    "read_symbol": read_symbol,
                    "next_state": next_state,
                    "write_symbol": write_symbol,
                    "move": move
                })

    return definition
