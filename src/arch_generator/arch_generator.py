import os
import re
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, Any, List, Tuple

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import VM
from diagrams.azure.network import VirtualNetworks, Subnets, PublicIpAddresses, NetworkSecurityGroupsClassic
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.database import SQLServers, SQLDatabases
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.devops import ApplicationInsights
from diagrams.azure.web import AppServices
from diagrams.onprem.client import Client

logger = logging.getLogger(__name__)

def parse_tf(path: str) -> List[Tuple[str, str]]:
    """Parses a Terraform file to extract resource types and names."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        logger.error(f"Terraform file not found: {path}")
        return []

    # find resource blocks: resource "TYPE" "NAME"
    pattern = re.compile(r'resource\s+"([^"]+)"\s+"([^"]+)"', re.IGNORECASE)
    resources = pattern.findall(text)
    return resources

def categorize(rtype: str) -> str:
    """Categorizes Azure resources based on their type."""
    if rtype.startswith("azurerm_network"):
        return "network"
    if rtype.startswith("azurerm_subnet") or rtype.endswith("/subnet"):
        return "network"
    if rtype.startswith("azurerm_linux_virtual_machine") or rtype.startswith("azurerm_linux") or rtype.startswith("azurerm_virtual_machine"):
        return "compute"
    if rtype.startswith("azurerm_storage_account"):
        return "storage"
    if rtype.startswith("azurerm_mssql") or rtype.startswith("azurerm_sql"):
        return "database"
    if rtype.startswith("azurerm_log_analytics_workspace") or rtype.startswith("azurerm_application_insights"):
        return "monitoring"
    if rtype.startswith("azurerm_service_plan") or rtype.startswith("azurerm_linux_web_app"):
        return "app"
    return "other"

def generate_architecture(req: Dict[str, Any]):
    """Generates an architecture diagram based on the requirement."""
    req_id = req.get("id")
    req_name = req.get("name")
    source_file = req.get("source")
    
    # Determine output directory
    # diagrams/Req_Arch_XXX/
    out_dir = Path("generated_diagrams") / f"{req_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Filename without extension
    filename = out_dir / f"{req_id}_{req_name.replace(' ', '_')}"
    
    logger.info(f"Generating Architecture Diagram for {req_id} from {source_file}")
    
    resources = parse_tf(source_file)
    if not resources:
        logger.warning(f"No resources found in {source_file} or file missing.")
        return

    graph_attr = {
        "splines": "ortho",
        "nodesep": "0.6",
        "ranksep": "0.9",
        "fontsize": "12",
        "bgcolor": "white",
        "pad": "0.5",
        "rankdir": "LR",
    }

    grouped = defaultdict(list)
    for rtype, name in resources:
        grouped[categorize(rtype)].append((rtype, name))

    # Output formats
    outformats = req.get("output_formats", ["png", "dot", "pdf"])

    # Create Diagram
    # Note: diagrams library context manager handles rendering
    try:
        with Diagram(f"{req_id}: {req_name}", filename=str(filename), outformat=outformats, show=False, graph_attr=graph_attr):
            nodes = {}
            # network
            if grouped.get("network"):
                with Cluster("Network"):
                    for rtype, name in grouped["network"]:
                        if "virtual_network" in rtype:
                            nodes[name] = VirtualNetworks(name)
                        elif "subnet" in rtype:
                            nodes[name] = Subnets(name)
                        elif "public_ip" in rtype:
                            nodes[name] = PublicIpAddresses(name)
                        elif "network_security_group" in rtype:
                            nodes[name] = NetworkSecurityGroupsClassic(name)

            # compute
            if grouped.get("compute"):
                with Cluster("Compute"):
                    for rtype, name in grouped["compute"]:
                        nodes[name] = VM(name)

            # app
            if grouped.get("app"):
                with Cluster("App Services"):
                    for rtype, name in grouped["app"]:
                        if "service_plan" in rtype:
                            nodes[name] = AppServices(name + "-plan")
                        else:
                            nodes[name] = AppServices(name)

            # storage
            if grouped.get("storage"):
                for rtype, name in grouped["storage"]:
                    nodes[name] = StorageAccounts(name)

            # database
            if grouped.get("database"):
                for rtype, name in grouped["database"]:
                    if "database" in rtype or "mssql" in rtype:
                        nodes[name] = SQLDatabases(name)
                    else:
                        nodes[name] = SQLServers(name)

            # monitoring
            if grouped.get("monitoring"):
                for rtype, name in grouped["monitoring"]:
                    if "log_analytics" in rtype:
                        nodes[name] = LogAnalyticsWorkspaces(name)
                    else:
                        nodes[name] = ApplicationInsights(name)

            # Connections Logic (Heuristic)
            client = Client("Users")
            
            web = None
            for k in nodes:
                if "webapp" in k or ("web" in k and "sql" not in k):
                    web = nodes[k]
                    break
            if not web:
                for k in nodes:
                    if isinstance(nodes[k], VM):
                        web = nodes[k]
                        break
            
            db = None
            for k in nodes:
                if "sqldb" in k or "sql" in k:
                    db = nodes[k]
                    break

            if client and web:
                client >> Edge(label="HTTP/HTTPS") >> web
            if web and db:
                web >> Edge(label="SQL") >> db

        logger.info(f"Architecture diagram generated at {filename}.*")
        
        # Post-process DOT for better labels if it exists
        dot_path = str(filename) + ".dot"
        if os.path.exists(dot_path):
             _post_process_dot(dot_path)
             
    except Exception as e:
        logger.error(f"Error generating diagram: {e}")

def _post_process_dot(dot_path: str):
    try:
        with open(dot_path, "r", encoding="utf-8") as f:
            txt = f.read()
        if "label=" in txt:
            txt2 = txt.replace("label=", "xlabel=")
            with open(dot_path, "w", encoding="utf-8") as f:
                f.write(txt2)
            logger.info(f"Post-processed DOT: {dot_path}")
    except Exception as e:
        logger.warning(f"DOT post-processing failed: {e}")
