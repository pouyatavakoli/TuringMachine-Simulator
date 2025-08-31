# Turing Machine Simulator

An **interactive web-based Turing Machine simulator** built with Flask that lets you **visualize computation step by step**. Perfect for learning and experimenting with the fundamentals of computation.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python\&logoColor=white)](https://www.python.org/downloads/release/python-380/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?logo=flask\&logoColor=black)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?logo=javascript\&logoColor=white)](https://www.ecma-international.org/ecma-262/6.0/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📸 Screenshots and Demo
![Machine Initialization img](https://github.com/pouyatavakoli/TuringMachine-Simulator/blob/master/readme%20assets/init.png)
![Computation History img](https://github.com/pouyatavakoli/TuringMachine-Simulator/blob/master/readme%20assets/erase%20tape%20history.png)
![create](https://github.com/pouyatavakoli/TuringMachine-Simulator/blob/master/readme%20assets/create.png)

<div align="center">
  <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
    <img src="https://github.com/pouyatavakoli/TuringMachine-Simulator/raw/master/readme%20assets/add%20transition.png" alt="Add Transition Interface" width="400"/>
    <img src="https://github.com/pouyatavakoli/TuringMachine-Simulator/raw/master/readme%20assets/create%20actions.png" alt="Preview and Actions" width="400"/>
  </div>
  <div style="display: flex; justify-content: center; gap: 130px; flex-wrap: wrap; margin-top: 10px;">
    <span><strong>Add Transition Interface</strong></span>
    <span><strong>Preview and Actions Panel</strong></span>
  </div>
</div>

demo video
![Computation History vid](https://github.com/pouyatavakoli/TuringMachine-Simulator/blob/master/readme%20assets/erase%20tape.gif)

---

## 📋 Table of Contents

* [✨ Features](#-features)
* [🚀 Quick Start](#-quick-start)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [📁 Project Structure](#-project-structure)
* [🧪 Input File Format](#-input-file-format)

  * [Format Specification](#format-specification)
* [🎮 How to Use](#-how-to-use)
* [🔧 API Endpoints](#-api-endpoints)
* [🛠️ Development](#️-development)

  * [Adding New Machines](#adding-new-machines)
  * [Code Structure](#code-structure)
  * [Running Tests](#running-tests)
  * [Contributing](#contributing)
* [📝 License](#-license)
* [📊 Status](#-status)

---

## ✨ Features

* **Visual Simulation**: Step-by-step execution with live tape visualization.
* **Multiple Machine Support**: Load and run different Turing machines from definition files.
* **Computation History**: Inspect every step of execution.
* **RESTful API**: Programmatic access to all simulator functions.

---

## 🚀 Quick Start

### Prerequisites

* Python **3.8+**
* `pip` (Python package manager)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pouyatavakoli/TuringMachine-Simulator.git
   cd TuringMachine-Simulator
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   flask run
   ```

5. Open your browser at 👉 `http://localhost:5000`

---

## 📁 Project Structure
```
TuringMachine-Simulator/
├── app/                          
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Turing machine models & logic
│   ├── routes.py                # API endpoints & routes (updated with create routes)
│   ├── utils.py                 # Parsing & helpers
│   ├── static/                  
│   │   ├── css/
│   │   │   ├── style.css        # Main styles & animations
│   │   │   └── create.css       # Creator-specific styles
│   │   └── js/
│   │       ├── script.js        # Main frontend interactivity
│   │       └── create.js        # Creator functionality
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Main simulator interface
│       └── create.html          # Machine creation interface
├── machines/                    
│   ├── add1_to_end.txt          # Example machines
│   ├── binary_incrementer.txt
│   ├── erase_tape.txt
│   ├── even_odd_checker.txt
│   └── only_ones.txt
├── readme_assets/               # README images
│   ├── add_transition.png
│   ├── create_actions.png
│   ├── create.png
│   ├── erase_tape.gif
│   ├── erase_tape_history.png
│   └── init.png
├── run.py                       # Entry point
├── requirements.txt             # Dependencies
├── LICENSE                      # License file
└── README.md                    # Documentation
```

---

## 🧪 Input File Format

Turing machines are defined in plain text.
Example: **Binary Incrementer**

```txt
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

* **states**: Comma-separated state names
* **input\_alphabet**: Symbols allowed in the input
* **tape\_alphabet**: All tape symbols (must include blank + input symbols)
* **blank**: Blank symbol (□ or `_`) `blank` ∈ `tape_alphabet`
* **initial\_state**: Starting state `initial_state` ∈ `states`
* **final\_states**: Comma-separated halting states `final_states` ⊆ `states`
* **transitions**:

  ```
  current_state,read_symbol -> next_state,write_symbol,move_direction
  ```

  where `move_direction` ∈ {`L`, `R`}

---

## 🎮 How to Use

1. **Select a Machine** from the dropdown.
2. **Set Initial Tape** (optional, depends on machine).
3. **Initialize** the machine.
4. **Control Execution**:

   * **Step** → one transition
   * **Run** → continuous execution
   * **Fast** → up to 1000 steps quickly
   * **Reset** → restart simulation
5. **Observe** tape updates, head movement, and states in real time.

---

## 🔧 API Endpoints

* `GET /api/machines` → List available machines
* `POST /api/init` → Initialize a machine (with optional tape input)
* `POST /api/reset` → Reset to initial state
* `POST /api/step` → Execute one step
* `POST /api/run` → Execute multiple steps
* `POST /api/machines/create` - Handles machine creation requests

---

## 🛠️ Development

### Adding New Machines

1. Add a `.txt` file to `machines/`.
2. Follow the input file format.
3. The new machine will automatically appear in the app.

### Code Structure

* **Backend (Flask)** → `models.py`, `routes.py`, `utils.py`
* **Frontend** → `index.html`, `script.js`, `style.css`

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repo
2. Create a branch → `git checkout -b feature/my-feature`
3. Commit changes → `git commit -m "Add feature"`
4. Push → `git push origin feature/my-feature`
5. Open a Pull Request 🎉

---

## 📝 License

Licensed under the **MIT License**. See [LICENSE](LICENSE).

---

##  Acknowledgments

* Inspired by **Alan Turing’s** pioneering work
* Built with [Flask](https://flask.palletsprojects.com/)
* Icons via [Font Awesome](https://fontawesome.com/)

---

## 📊 Status

![GitHub issues](https://img.shields.io/github/issues/pouyatavakoli/TuringMachine-Simulator)
![GitHub pull requests](https://img.shields.io/github/issues-pr/pouyatavakoli/TuringMachine-Simulator)
![GitHub last commit](https://img.shields.io/github/last-commit/pouyatavakoli/TuringMachine-Simulator)

---

⭐ If you like this project, **give it a star!**
