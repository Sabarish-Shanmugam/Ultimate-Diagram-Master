# Diagram generation for `iis-2vm-sql-1vm` Bicep demo

This document explains, step-by-step, how to generate architecture diagrams from the `bicep-demo/demos/iis-2vm-sql-1vm` sample and how the generator script in this workspace maps Bicep resources into a visual diagram.

Location

- Bicep sample: `bicep-demo/demos/iis-2vm-sql-1vm`
- Diagram generator (script): `Arch_Diagrams/bicep_iis_sql_diagram.py`
- Diagram outputs: `Arch_Diagrams/diagrams/` (PNG, DOT, DRAWIO)

## Overview

The Bicep demo creates a small IaaS environment: 1–2 IIS web VMs in an Availability Set behind a Load Balancer, plus a SQL Server VM in a separate subnet. The provided diagram generator script reads a hard-coded representation of that architecture and produces GraphViz DOT, PNG, and draw.io files.

## Step-by-step instructions (what and why)

1. Prerequisites — why: the `diagrams` toolchain renders images using GraphViz and pygraphviz. On Windows you need GraphViz installed and a Python toolchain that can build or install `pygraphviz`.

- Install GraphViz and ensure `dot` is on your PATH (EXE installer recommended):

```powershell
choco install graphviz    # or download from https://graphviz.org/download/
# verify
dot -V
```

- Install Visual C++ Build Tools only if `pygraphviz` needs to be compiled (Windows):

```powershell
# GUI: download "Build Tools for Visual Studio"
# or use winget:
winget install --id Microsoft.VisualStudio.2022.BuildTools -e
```

2. Use the repository's virtual environment (recommended)

- Switch to the `Arch_Diagrams` folder and create/activate the venv (this project already contains `Arch_Diagrams/venv` used in examples):

```powershell
cd "C:\Users\Venom\Downloads\Architecture_Diagrams_Python_AI-main\Arch_Diagrams"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Why: using the repository venv avoids polluting your system Python and keeps package versions reproducible.

3. Install Python dependencies

```powershell
# make sure pip is recent
pip install --upgrade pip setuptools wheel

# Install pygraphviz (graphviz dev files must be installed and reachable)
# If the install fails, see Troubleshooting below for pre-built wheel options.
pip install pygraphviz

# Install the diagram toolchain
pip install diagrams graphviz graphviz2drawio
```

Why: `diagrams` creates the DOT; `pygraphviz`/`graphviz` render it; `graphviz2drawio` converts DOT to editable draw.io.

4. Generate the diagram for the Bicep demo

Run the generator script I added to the workspace:

```powershell
# From repo root (or from Arch_Diagrams)
& .\venv\Scripts\python.exe ..\Arch_Diagrams\bicep_iis_sql_diagram.py
# or, from repo root
& .\Arch_Diagrams\venv\Scripts\python.exe Arch_Diagrams\bicep_iis_sql_diagram.py
```

What the script does (brief explanation)

- Creates a `VNet` cluster with two subnets (FE and DB)
- Shows the Load Balancer and its public IP
- Shows the Availability Set and 1–2 web VMs
- Shows the SQL VM with a public IP
- Adds NSGs and connections with labelled edges (LB → web VMs → SQL)

5. Convert DOT to draw.io (editable)

```powershell
& .\venv\Scripts\graphviz2drawio "Arch_Diagrams\diagrams\bicep_iis_2vm_sql_1vm.dot" -o "Arch_Diagrams\diagrams\bicep_iis_2vm_sql_1vm.drawio"
```

6. Open and refine

- Open the `.drawio` file in VS Code (install `hediet.vscode-drawio`) or open in draw.io online to reposition nodes, change colors, and add annotations.

## Troubleshooting

- Error: "dot not found" or `ExecutableNotFound`: ensure GraphViz is installed and `C:\Program Files\Graphviz\bin` is on your PATH. You can add it for the current session in PowerShell:

```powershell
$env:PATH = "C:\Program Files\Graphviz\bin;$env:PATH"
```

- Error: "Failed building wheel for pygraphviz" or C1083 cannot find `graphviz/cgraph.h` — this means the GraphViz headers/libs aren't visible to the compiler. Fixes:

  - Install GraphViz via the EXE installer and add its `include`/`lib` to environment variables before installing `pygraphviz`.
  - Or install a pre-built wheel from Christoph Gohlke's site (Windows wheels): https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz
  - Or use `conda`/`mamba` and `conda-forge` to install `pygraphviz` and `graphviz` easily.

- Warning: GraphViz may emit "size too small for label" or "Orthogonal edges do not currently handle edge labels" — these are layout warnings. You can:
  - Increase `nodesep` / `ranksep` in the script's `graph_attr`.
  - Use a different `splines` value (e.g., `spline`), or post-process DOT to use `xlabels` for edges.

## Mapping of Bicep resources to diagram elements

- `Microsoft.Network/virtualNetworks` → `VNet` cluster
- `Microsoft.Network/subnets` → `Cluster` per subnet
- `Microsoft.Network/networkSecurityGroups` → `NSG` nodes inside subnets
- `Microsoft.Network/loadBalancers` → `LoadBalancer` node + public IP
- `Microsoft.Compute/availabilitySets` + `virtualMachines` → `Availability Set` cluster with `VM` nodes
- `Microsoft.Network/publicIPAddresses` → `Public IP` nodes tied to VM/LB

## Extending or customizing the diagram

- If you want more detail: modify `Arch_Diagrams/bicep_iis_sql_diagram.py` to add backend pools, NAT rules, probes, NICs, or per-VM names.
- To produce additional diagrams (public-only vs internal-only), duplicate the script and filter which nodes/edges you include.

Files in this demo folder (quick explanation)

- `main.bicep` — the Bicep template that defines the demo resources (VMs, LB, VNet, NSGs).
- `azuredeploy.json` / `azuredeploy.parameters.json` — ARM JSON variants and parameters for deployment.
- `images/` — sample architecture images used in the demo README (visual reference).
- `scripts/` — helper scripts for deployment/testing (if present).

If you'd like, I can:

- Add a second script that parses the Bicep file and auto-generates the diagram from resource declarations (more work, but doable).
- Increase spacing and post-process DOT to use `xlabels` so edge labels don't overlap.

---

Created by automation in this workspace to speed diagram generation. If you want me to modify the script to include additional details (probes, NAT rules, explicit backend pools), tell me which items to add and I'll update the generator and re-run it.
