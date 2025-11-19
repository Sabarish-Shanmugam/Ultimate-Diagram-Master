import logging
from pathlib import Path
from typing import Dict, Any

from processpiper import ProcessMap, EventType, ActivityType, GatewayType

logger = logging.getLogger(__name__)

def generate_bpmn(req: Dict[str, Any]):
    """Generates a BPMN diagram based on requirements."""
    req_id = req.get("id")
    req_name = req.get("name")
    lanes_def = req.get("lanes", [])
    steps_def = req.get("steps", [])

    if not lanes_def or not steps_def:
        logger.warning(f"Incomplete BPMN definition for {req_id}. Skipping.")
        return

    # Output directory
    out_dir = Path("generated_diagrams") / f"{req_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = out_dir / f"{req_id}_{req_name.replace(' ', '_')}.png"

    logger.info(f"Generating BPMN for {req_id}")

    try:
        # Increase width for better spacing and use a theme
        with ProcessMap(req_name, width=4000, height=3000, colour_theme="BLUEMOUNTAIN") as my_process:
            lanes = {}
            # Create Lanes
            for lane_def in lanes_def:
                lane_name = lane_def.get("name")
                lanes[lane_name] = my_process.add_lane(lane_name)

            elements = {}
            # Create Elements
            for step in steps_def:
                name = step.get("name")
                lane_name = step.get("lane")
                step_type = step.get("type", "task")
                
                lane = lanes.get(lane_name)
                if not lane:
                    logger.warning(f"Lane '{lane_name}' not found for step '{name}'. Skipping.")
                    continue

                elem_type = _map_type(step_type)
                element = lane.add_element(name, elem_type)
                elements[name] = element

            # Connect Elements
            for step in steps_def:
                name = step.get("name")
                current_elem = elements.get(name)
                
                if not current_elem:
                    continue

                # Simple next connection
                next_step = step.get("next")
                if next_step:
                    next_elem = elements.get(next_step)
                    if next_elem:
                        current_elem.connect(next_elem)
                
                # Conditional connections (Gateway)
                conditions = step.get("conditions", [])
                for cond in conditions:
                    next_step_cond = cond.get("next")
                    label = cond.get("label", "")
                    next_elem = elements.get(next_step_cond)
                    if next_elem:
                        current_elem.connect(next_elem, label)

            my_process.draw()
            my_process.save(str(filename))
            logger.info(f"BPMN generated at {filename}")

    except Exception as e:
        logger.error(f"Error generating BPMN: {e}")

def _map_type(type_str: str):
    """Maps string type to ProcessPiper enum."""
    type_str = type_str.lower()
    if type_str == "start":
        return EventType.START
    elif type_str == "end":
        return EventType.END
    elif type_str == "task":
        return ActivityType.TASK
    elif type_str == "subprocess":
        return ActivityType.SUBPROCESS
    elif type_str == "gateway":
        return GatewayType.EXCLUSIVE
    else:
        return ActivityType.TASK
