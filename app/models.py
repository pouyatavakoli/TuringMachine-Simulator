from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any
from enum import Enum

class MoveDirection(Enum):
    LEFT = 'L'
    RIGHT = 'R'

@dataclass
class Transition:
    current_state: str
    read_symbol: str
    next_state: str
    write_symbol: str
    move: MoveDirection

@dataclass
class MachineDefinition:
    states: Set[str]
    input_alphabet: Set[str]
    tape_alphabet: Set[str]
    transitions: List[Transition]
    blank: str
    initial_state: str
    final_states: Set[str]

@dataclass
class MachineState:
    head_position: int
    current_state: str
    halted: bool = field(default=False)
    steps: int = field(default=0)

@dataclass
class TuringMachine:
    definition: MachineDefinition
    tape: Dict[int, str] = field(default_factory=dict)
    state: MachineState = field(init=False)
    history: List[Dict[str, Any]] = field(default_factory=list, init=False)
    
    def __post_init__(self):
        self.validate_definition()
        self.reset()
    
    def validate_definition(self):
        # initial state should be member if states set
        if self.definition.initial_state not in self.definition.states:
            raise ValueError(f"Initial state '{self.definition.initial_state}' not in states")
        
        # final states should be subset of states set
        if not self.definition.final_states.issubset(self.definition.states):
            invalid_states = self.definition.final_states - self.definition.states
            raise ValueError(f"Final states {invalid_states} not in states")
        # blank should be a tape alphabet
        if self.definition.blank not in self.definition.tape_alphabet:
            raise ValueError(f"Blank symbol '{self.definition.blank}' not in tape alphabet")
        
        # Validate transition functions
        for transition in self.definition.transitions:
            if transition.current_state not in self.definition.states:
                raise ValueError(f"Transition state '{transition.current_state}' not in states")
            
            if transition.read_symbol not in self.definition.tape_alphabet:
                raise ValueError(f"Read symbol '{transition.read_symbol}' not in tape alphabet")
            
            if transition.next_state not in self.definition.states:
                raise ValueError(f"Next state '{transition.next_state}' not in states")
            
            if transition.write_symbol not in self.definition.tape_alphabet:
                raise ValueError(f"Write symbol '{transition.write_symbol}' not in tape alphabet")
    
    def reset(self, initial_tape: Optional[List[str]] = None):
        """Reset the machine with optional initial tape"""
        if initial_tape is None:
            initial_tape = []
        
        # Clear and initialize tape
        self.tape.clear()
        for index, symbol in enumerate(initial_tape):
            if symbol not in self.definition.tape_alphabet:
                raise ValueError(f"Initial tape symbol '{symbol}' not in tape alphabet")
            self.tape[index] = symbol
        
        # Initialize machine state
        self.state = MachineState(
            head_position=0,
            current_state=self.definition.initial_state,
            halted=False,
            steps=0
        )
        
        self.history.clear()
    
    def read_from_tape(self) -> str:
        """Read symbol at current head position"""
        return self.tape.get(self.state.head_position, self.definition.blank)
    
    def write_to_tape(self, symbol: str):
        """Write symbol at current head position"""
        if symbol == self.definition.blank:
            self.tape.pop(self.state.head_position, None)
        else:
            if symbol not in self.definition.tape_alphabet:
                raise ValueError(f"Symbol '{symbol}' not in tape alphabet")
            self.tape[self.state.head_position] = symbol
    
    def move_head(self, direction: MoveDirection):
        if direction == MoveDirection.RIGHT:
            self.state.head_position += 1
        elif direction == MoveDirection.LEFT:
            self.state.head_position -= 1
    
    def find_transition(self) -> Optional[Transition]:
        """Find applicable transition for current state and head position"""
        current_symbol = self.read_from_tape()
        
        for transition in self.definition.transitions:
            if (transition.current_state == self.state.current_state and 
                transition.read_symbol == current_symbol):
                return transition
        return None
    
    def step(self) -> bool:
        """Execute one step of computation"""
        if self.state.halted:
            return False
        
        # Record state before transition
        self.history.append({
            'step': self.state.steps,
            'state': self.state.current_state,
            'head_position': self.state.head_position,
            'tape_snapshot': self.get_tape_snapshot(),
            'current_symbol': self.read_from_tape()
        })
        
        # Find applicable transition
        transition = self.find_transition()
        
        if transition is None:
            self.state.halted = True
            return False
        
        # Apply transition
        self.write_to_tape(transition.write_symbol)
        self.move_head(transition.move)
        self.state.current_state = transition.next_state
        self.state.steps += 1
        
        # Check if reached final state
        if self.state.current_state in self.definition.final_states:
            self.state.halted = True
        
        #returns false it halted in returns true if not
        return True
    
    def run(self, max_steps: int = 1000) -> bool:
        """Run machine until halt or max steps reached"""
        while not self.state.halted and self.state.steps < max_steps:
            if not self.step():
                #break the loop is machine is halted
                break
        return self.state.halted
    
    def get_tape_snapshot(self) -> List[str]:
        """Get current tape as list with proper blank symbols"""
        if not self.tape:
            return [self.definition.blank]
        
        min_index = min(self.tape.keys()) if self.tape else self.state.head_position
        max_index = max(self.tape.keys()) if self.tape else self.state.head_position
        
        min_index = min(min_index, self.state.head_position)
        max_index = max(max_index, self.state.head_position)
        
        tape_snapshot = []
        for i in range(min_index, max_index + 1):
            tape_snapshot.append(self.tape.get(i, self.definition.blank))
        
        return tape_snapshot