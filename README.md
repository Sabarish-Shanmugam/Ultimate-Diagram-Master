# Ultimate Diagram Master

**Automated Architecture, Data Flow, and Business Process Diagrams**

Welcome to **Ultimate Diagram Master**, a powerful tool designed to automatically generate professional diagrams from your configuration files. Whether you need Azure architecture visualizations, Threat Modeling Data Flow Diagrams (DFD), or Business Process Model and Notation (BPMN) flows, this tool streamlines the process using Python-as-Code.

## 🚀 Features

*   **Azure Architecture Diagrams**: Automatically generate detailed Azure infrastructure diagrams using the `diagrams` library.
*   **Data Flow Diagrams (DFD)**: Create clear data flow visualizations for threat modeling and system analysis.
*   **BPMN Support**: Generate business process flows using `processpiper`.
*   **Unified Pipeline**: A single entry point (`pipeline_controller.py`) manages all diagram generation tasks.
*   **Configuration Driven**: Define your requirements in simple YAML files (`config/project_requirements.yaml`).
*   **Editable Outputs**: Generates diagrams in PNG, DOT, and Draw.io formats for easy editing.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
2.  **GraphViz**: Critical for rendering diagrams.
    *   [Download GraphViz](https://graphviz.org/download/)
    *   **Important**: During installation, select "Add GraphViz to the system PATH for all users".

## 🛠️ Installation & Setup

We provide a simple setup script that handles everything for you.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Sabarish-Shanmugam/Ultimate-Diagram-Master.git
    cd Ultimate-Diagram-Master/Arch_Diagrams
    ```

2.  **Run the Setup Script**:
    Double-click `setup_and_run.bat` or run it from the terminal:
    ```powershell
    .\setup_and_run.bat
    ```
    *   This script will automatically:
        *   Check for Python.
        *   Create a virtual environment (`venv`).
        *   Install all dependencies from `requirements.txt`.
        *   Initialize the project configuration if missing.
        *   Run the diagram generation pipeline.

## 📖 Usage

### Automatic Mode
Simply run the `setup_and_run.bat` script. It will execute the pipeline based on the configuration in `config/project_requirements.yaml`.

### Manual Mode
If you prefer to run commands manually:

1.  **Activate the Virtual Environment**:
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

2.  **Initialize Project (if starting fresh)**:
    ```bash
    python src/pipeline_controller.py init
    ```
    This creates a `config/project_requirements.yaml` file from the template.

3.  **Run the Pipeline**:
    ```bash
    python src/pipeline_controller.py run
    ```

### Configuration
Edit `config/project_requirements.yaml` to define what diagrams you want to generate.

**Example Configuration:**
```yaml
requirements:
  - id: "REQ-001"
    name: "Azure Web App Architecture"
    type: "architecture"
    # ... specific details ...

  - id: "REQ-002"
    name: "Order Processing Flow"
    type: "business_process"
    # ... specific details ...
```

## 📂 Project Structure

```
Arch_Diagrams/
├── config/                 # Configuration files (requirements.yaml)
├── generated_diagrams/     # Output folder for all diagrams (PNG, DOT, Draw.io)
├── src/                    # Source code
│   ├── arch_generator/     # Azure Architecture logic
│   ├── bpmn_generator/     # BPMN logic
│   ├── dfd_generator/      # Data Flow Diagram logic
│   └── pipeline_controller.py # Main entry point
├── venv/                   # Python virtual environment (created on setup)
├── requirements.txt        # Python dependencies
├── setup_and_run.bat       # One-click setup and execution script
└── README.md               # This documentation
```

## ❓ Troubleshooting

**Error: `ExecutableNotFound: failed to execute WindowsPath('dot')`**
*   **Cause**: GraphViz is not installed or not in your system PATH.
*   **Solution**: Install GraphViz and ensure the `bin` folder (e.g., `C:\Program Files\Graphviz\bin`) is added to your system Environment Variables. The `setup_and_run.bat` attempts to handle this, but a system-level install is best.

**Error: `ImportError` or Module not found**
*   **Solution**: Ensure you have activated the virtual environment (`.\venv\Scripts\Activate.ps1`) before running python scripts manually.
