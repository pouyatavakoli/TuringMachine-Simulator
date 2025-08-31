# Turing Machine Simulator

A beautiful, interactive web-based Turing Machine simulator built with Flask that allows you to visualize and understand computation through step-by-step execution of Turing machines.

![Turing Machine Simulator](https://img.shields.io/badge/Python-3.8%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Visual Simulation**: Watch the Turing machine execute step-by-step with tape visualization
- **Multiple Machine Support**: Load different Turing machine definitions from text files
- **Computation History**: Track every step of the computation with detailed history
- **RESTful API**: Clean API endpoints for programmatic interaction

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/pouyatavakoli/TuringMachine-Simulator.git
cd TuringMachine-Simulator
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
flask run
```

5. Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
TuringMachine-Simulator/
├── app/                          # Main application package
│   ├── __init__.py              # Flask application factory
│   ├── models.py                # Turing machine data models and core logic
│   ├── routes.py                # API endpoints and web routes
│   ├── utils.py                 # Helper functions and file parsing utilities
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   │   └── style.css        # Custom styles and animations
│   │   └── js/
│   │       └── script.js        # Frontend interactivity and API communication
│   └── templates/               # Jinja2 templates
│       └── index.html           # Main application interface
├── machines/                     # Turing machine definition files
│   └── example.txt              # Sample machine configuration
├── tests/                       # Test suite
│   ├── conftest.py              # pytest configuration and fixtures
│   ├── __init__.py              # Test package initialization
│   ├── test_app_basic.py        # Application-level tests
│   └── test_models.py           # Turing machine model tests
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # Project documentation (this file)

```

## 🧪 Input File Format

Turing machines are defined using a simple text format. Here's an example that increments a binary number:

```plaintext
states: q0,q1,halt
input_alphabet: 0,1
tape_alphabet: 0,1,□
blank: □
initial_state: q0
final_states: halt
transitions:
q0,0 -> q0,0,R
q0,1 -> q0,1,R
q0,□ -> q1,□,L
q1,0 -> halt,1,L
q1,1 -> q1,0,L
q1,□ -> halt,1,L
```

### Format Specification

- **states**: Comma-separated list of state names
- **input_alphabet**: Symbols the machine reads from initial tape
- **tape_alphabet**: All symbols that can appear on the tape (includes input_alphabet + blank)
- **blank**: The blank symbol (typically □ or _)
- **initial_state**: The starting state
- **final_states**: Comma-separated list of halting states
- **transitions**: List of transition rules in format:  
  `current_state,read_symbol -> next_state,write_symbol,move_direction`  
  Where move_direction is either L (left) or R (right)

## 🎮 How to Use

1. **Select a Machine**: Choose from available machines in the dropdown
2. **Set Initial Tape**: Enter the initial tape content (optional, baesd on your machine defenition)
3. **Initialize**: Click "Initialize" to load the machine
4. **Control Execution**:
   - **Step**: Execute one transition at a time
   - **Run**: Execute continuously at a moderate pace
   - **Fast**: Execute up to 1000 steps without animation
   - **Reset**: Return to initial state

5. **Observe**: Watch the tape change, head movement, and state transitions in real-time

## 🔧 API Endpoints

The simulator provides a RESTful API for programmatic control:

- `GET /api/machines` - List available machines
- `POST /api/init` - Initialize a machine with optional tape content
- `POST /api/reset` - Reset a machine to initial state
- `POST /api/step` - Execute a single step
- `POST /api/run` - Execute up to a specified number of steps

## 🛠️ Development

### Adding New Machines

1. Create a new text file in the `machines/` directory
2. Follow the input format specification above
3. The file will automatically appear in the machine selection dropdown

### Code Structure

- **Backend (Flask)**:
  - `app.py`: Main application and route definitions
  - `models.py`: Turing machine data models and logic
  - `utils.py`: File parsing and helper functions

- **Frontend**:
  - `index.html`: Main page structure
  - `script.js`: Interactive functionality and API communication
  - `style.css`: Custom styling and animations

### Running Tests

```bash
python -m pytest tests/
```

### Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Alan Turing's revolutionary work on computation
- Built with [Flask](https://flask.palletsprojects.com/)
- Icons from [Font Awesome](https://fontawesome.com/)

## 📊 Status

![GitHub issues](https://img.shields.io/github/issues/pouyatavakoli/TuringMachine-Simulator)
![GitHub pull requests](https://img.shields.io/github/issues-pr/pouyatavakoli/TuringMachine-Simulator)
![GitHub last commit](https://img.shields.io/github/last-commit/pouyatavakoli/TuringMachine-Simulator)

---

⭐ Star this repo!
