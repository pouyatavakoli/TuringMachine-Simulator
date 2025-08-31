import pytest
from app.models import MoveDirection, Transition, MachineDefinition, MachineState, TuringMachine

@pytest.fixture
def simple_machine_definition():
    """Fixture for a valid machine definition."""
    states = {'q0', 'q1', 'halt'}
    input_alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', '3', '_'}
    transitions = []

    transitions.append(Transition('q0', '0', 'q0', '0', MoveDirection.RIGHT))
    transitions.append(Transition('q0', '1', 'q0', '1', MoveDirection.RIGHT))
    transitions.append(Transition('q0', '_', 'halt', '_', MoveDirection.RIGHT))
    
    blank = '_'
    initial_state = 'q0'
    final_states = {'halt'}
    
    return MachineDefinition(
        states, input_alphabet, tape_alphabet, transitions, blank, initial_state, final_states
    )

def test_machine_definition_validation(simple_machine_definition):
    """Test that a valid machine definition does not raise errors."""
    # Should not raise an exception
    TuringMachine(simple_machine_definition)

def test_initial_state_not_in_states():
    """Test validation for initial state not in states."""
    states = {'q1', 'halt'}
    input_alphabet = {'0'}
    tape_alphabet = {'0', '_'}
    transitions = []
    blank = '_'
    initial_state = 'q0'  # Not in states
    final_states = {'halt'}
    
    definition = MachineDefinition(
        states, input_alphabet, tape_alphabet, transitions, blank, initial_state, final_states
    )
    with pytest.raises(ValueError, match="not in states"):
        TuringMachine(definition)

def test_final_states_not_subset_of_states():
    """Test validation for final states not subset of states."""
    states = {'q0'}
    input_alphabet = {'0'}
    tape_alphabet = {'0', '_'}
    transitions = []
    blank = '_'
    initial_state = 'q0'
    final_states = {'halt'}  # Not in states
    
    definition = MachineDefinition(
        states, input_alphabet, tape_alphabet, transitions, blank, initial_state, final_states
    )
    with pytest.raises(ValueError, match="not in states"):
        TuringMachine(definition)

def test_blank_not_in_tape_alphabet():
    """Test validation for blank not in tape alphabet."""
    states = {'q0'}
    input_alphabet = {'0'}
    tape_alphabet = {'0'}  # Blank '_' missing
    transitions = []
    blank = '_'
    initial_state = 'q0'
    final_states = {'q0'}
    
    definition = MachineDefinition(
        states, input_alphabet, tape_alphabet, transitions, blank, initial_state, final_states
    )
    with pytest.raises(ValueError, match="not in tape alphabet"):
        TuringMachine(definition)

def test_transition_validation():
    """Test validation for transitions with invalid states/symbols."""
    states = {'q0'}
    input_alphabet = {'0'}
    tape_alphabet = {'0', '_'}
    transitions = []
    transitions.append(Transition('q_invalid', '0', 'q0', '0', MoveDirection.RIGHT))  # Invalid state
    
    blank = '_'
    initial_state = 'q0'
    final_states = {'q0'}
    
    definition = MachineDefinition(
        states, input_alphabet, tape_alphabet, transitions, blank, initial_state, final_states
    )
    with pytest.raises(ValueError, match="not in states"):
        TuringMachine(definition)

def test_reset_with_initial_tape(simple_machine_definition):
    """Test resetting the machine with initial tape."""
    tm = TuringMachine(simple_machine_definition)
    initial_tape = ['0', '1', '0']
    tm.reset(initial_tape=initial_tape)
    
    assert tm.tape == {0: '0', 1: '1', 2: '0'}
    assert tm.state.current_state == 'q0'
    assert tm.state.head_position == 0
    assert tm.state.halted is False
    assert tm.state.steps == 0

def test_reset_invalid_tape_symbol(simple_machine_definition):
    """Test reset with a tape symbol not in tape alphabet."""
    tm = TuringMachine(simple_machine_definition)
    initial_tape = ['0', '2']  # '2' is invalid
    with pytest.raises(ValueError, match="not in tape alphabet"):
        tm.reset(initial_tape=initial_tape)

def test_read_from_tape(simple_machine_definition):
    """Test reading from tape at various positions."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape=['0', '1'])
    
    assert tm.read_from_tape() == '0'  # Head at position 0
    tm.state.head_position = 1
    assert tm.read_from_tape() == '1'
    tm.state.head_position = 5  # Unwritten position
    assert tm.read_from_tape() == '_'  # Blank symbol

def test_write_to_tape(simple_machine_definition):
    """Test writing to tape and handling blank symbols."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset()
    
    tm.write_to_tape('1')
    assert tm.tape[0] == '1'
    
    tm.write_to_tape('_')  # Write blank
    assert 0 not in tm.tape  # Cell should be removed

def test_write_invalid_symbol(simple_machine_definition):
    """Test writing a symbol not in tape alphabet."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset()
    
    with pytest.raises(ValueError, match="not in tape alphabet"):
        tm.write_to_tape('2')  # Not in tape alphabet

def test_move_head(simple_machine_definition):
    """Test moving the head left and right."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset()
    
    assert tm.state.head_position == 0
    tm.move_head(MoveDirection.RIGHT)
    assert tm.state.head_position == 1
    tm.move_head(MoveDirection.LEFT)
    assert tm.state.head_position == 0

def test_find_transition(simple_machine_definition):
    """Test finding a valid transition."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape=['0'])
    
    transition = tm.find_transition()
    assert transition is not None
    assert transition.current_state == 'q0'
    assert transition.read_symbol == '0'

def test_find_no_transition(simple_machine_definition):
    """Test when no transition is found."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape=['3'])  # Tape reads blank
    
    # No transition for reading 3 in q0
    transition = tm.find_transition()
    assert transition is None

def test_step_execution(simple_machine_definition):
    """Test executing a single step."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape=['0'])
    
    assert tm.step() is True  # Step successful
    assert tm.state.current_state == 'q0'
    assert tm.state.head_position == 1  # Moved right
    assert tm.tape[0] == '0'  # Symbol written (same in this case)
    assert tm.state.steps == 1

def test_step_halt(simple_machine_definition):
    """Test stepping when no transition exists (halt)."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape= ['3'])
    
    assert tm.step() is False  # No transition, halts
    assert tm.state.halted is True

def test_run_until_halt(simple_machine_definition):
    """Test running the machine until halt."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape=['0', '1'])
    
    halted = tm.run(max_steps=1000)
    assert halted is True
    assert tm.state.halted is True
    assert tm.state.current_state == 'halt'

def test_run_max_steps(simple_machine_definition):
    """Test running stops at max steps."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape=['0', '1'])
    
    halted = tm.run(max_steps=2)
    assert halted is False  # Not halted yet
    assert tm.state.steps == 2

def test_get_tape_snapshot(simple_machine_definition):
    """Test getting tape snapshot with blanks."""
    tm = TuringMachine(simple_machine_definition)
    tm.reset(initial_tape=['0', '1'])
    tm.state.head_position = 3  # Move head beyond
    
    snapshot = tm.get_tape_snapshot()
    assert snapshot['tape'] == ['0', '1', '_', '_']  # Includes blanks up to head
    assert snapshot['min_index'] == 0
    assert snapshot['max_index'] == 3