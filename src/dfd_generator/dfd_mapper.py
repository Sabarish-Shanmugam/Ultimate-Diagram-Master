import logging
from pathlib import Path
from typing import Dict, Any

from diagrams import Diagram, Edge
from diagrams.programming.flowchart import Action, Database, Document, InputOutput

logger = logging.getLogger(__name__)

def generate_dfd(req: Dict[str, Any]):
    """Generates a Data Flow Diagram based on requirements."""
    req_id = req.get("id")
    req_name = req.get("name")
    mappings = req.get("mappings", [])
    
    if not mappings:
        logger.warning(f"No mappings defined for DFD {req_id}. Skipping.")
        return

    try:
        with Diagram(f"DFD: {req_name}", filename=str(filename), show=False, graph_attr=graph_attr):
            nodes = {}
            
            # Create nodes first
            for mapping in mappings:
                src_name = mapping.get("source")
                tgt_name = mapping.get("target")
                
                if src_name and src_name not in nodes:
                    nodes[src_name] = _create_node(src_name)
                if tgt_name and tgt_name not in nodes:
                    nodes[tgt_name] = _create_node(tgt_name)

            # Create edges
            for mapping in mappings:
                src_name = mapping.get("source")
                tgt_name = mapping.get("target")
                data_label = mapping.get("data", "")
                protocol = mapping.get("protocol", "")
                
                label = f"{data_label}\n({protocol})" if protocol else data_label
                
                if src_name in nodes and tgt_name in nodes:
                    nodes[src_name] >> Edge(label=label) >> nodes[tgt_name]

        logger.info(f"DFD generated at {filename}.png")

    except Exception as e:
        logger.error(f"Error generating DFD: {e}")

def _create_node(name: str):
    """Creates a DFD node based on name heuristics."""
    lower_name = name.lower()
    if "database" in lower_name or "store" in lower_name or "db" in lower_name:
        return Database(name)
    elif "user" in lower_name or "actor" in lower_name:
        return InputOutput(name) # Using IO for external entities/users
    elif "report" in lower_name or "document" in lower_name:
        return Document(name)
    else:
        return Action(name)
