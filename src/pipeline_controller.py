import os
import sys
import yaml
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add GraphViz to PATH
graphviz_path = r"C:\Program Files\Graphviz\bin"
if os.path.exists(graphviz_path) and graphviz_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + graphviz_path
    logger.info(f"Added GraphViz to PATH: {graphviz_path}")

class PipelineController:
    def __init__(self, config_path: str = "config/project_requirements.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.root_dir = Path(__file__).parent.parent

    def _load_config(self) -> Dict[str, Any]:
        """Loads the project requirements configuration."""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file {self.config_path} not found. Using empty config.")
            return {"requirements": []}
        
        with open(self.config_path, 'r') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                logger.error(f"Error parsing config file: {e}")
                return {"requirements": []}

    def init_project(self):
        """Initializes the project by creating a requirements file from template."""
        template_path = self.root_dir / "config" / "requirements_template.yaml"
        target_path = self.root_dir / "config" / "project_requirements.yaml"

        if not template_path.exists():
            logger.error("Template file not found!")
            return

        if target_path.exists():
            logger.warning("project_requirements.yaml already exists. Skipping initialization.")
            return

        import shutil
        shutil.copy(template_path, target_path)
        logger.info(f"Initialized project requirements at {target_path}")

    def run(self):
        """Main execution loop."""
        logger.info("Starting Ultimate Diagram Master Pipeline...")
        
        requirements = self.config.get("requirements", [])
        if not requirements:
            logger.warning("No requirements found in config. Run 'init' to start or add requirements.")
            return

        for req in requirements:
            self._process_requirement(req)

        logger.info("Pipeline execution completed.")

    def _process_requirement(self, req: Dict[str, Any]):
        """Processes a single requirement based on its type."""
        req_id = req.get("id")
        req_type = req.get("type")
        req_name = req.get("name")

        logger.info(f"Processing Requirement: {req_id} ({req_type}) - {req_name}")

        try:
            if req_type == "architecture":
                self._run_arch_generator(req)
            elif req_type == "data_flow":
                self._run_dfd_generator(req)
            elif req_type == "business_process":
                self._run_bpmn_generator(req)
            else:
                logger.warning(f"Unknown requirement type: {req_type}")
        except Exception as e:
            logger.error(f"Failed to process {req_id}: {e}")

    def _run_arch_generator(self, req: Dict[str, Any]):
        """Triggers Architecture Generation."""
        # TODO: Import and call actual generator
        from src.arch_generator.arch_generator import generate_architecture
        generate_architecture(req)

    def _run_dfd_generator(self, req: Dict[str, Any]):
        """Triggers DFD Generation."""
        # TODO: Import and call actual generator
        from src.dfd_generator.dfd_mapper import generate_dfd
        generate_dfd(req)

    def _run_bpmn_generator(self, req: Dict[str, Any]):
        """Triggers BPMN Generation."""
        # TODO: Import and call actual generator
        from src.bpmn_generator.bpmn_processor import generate_bpmn
        generate_bpmn(req)

def main():
    parser = argparse.ArgumentParser(description="Ultimate Diagram Master Pipeline")
    parser.add_argument("command", nargs="?", default="run", choices=["run", "init"], help="Command to execute")
    
    args = parser.parse_args()
    
    controller = PipelineController()
    
    if args.command == "init":
        controller.init_project()
    else:
        controller.run()

if __name__ == "__main__":
    main()
