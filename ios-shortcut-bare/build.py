#!/usr/bin/env python3
"""Generate .cherri files from templates using config.json"""

import json
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Error: jinja2 not installed. Run: pip install jinja2")
    exit(1)

ROOT = Path(__file__).parent
TEMPLATES = ROOT / "templates"
BUILD = ROOT / "build"
CONFIG = ROOT / "config.json"


def main():
    if not CONFIG.exists():
        print(f"Error: {CONFIG} not found")
        exit(1)

    BUILD.mkdir(exist_ok=True)

    with open(CONFIG) as f:
        config = json.load(f)

    env = Environment(loader=FileSystemLoader(TEMPLATES))

    api = config["api"]
    defaults = config.get("defaults", {})

    generated = []
    for shortcut_id, settings in config["shortcuts"].items():
        if not settings.get("enabled", True):
            print(f"Skipping disabled: {shortcut_id}")
            continue

        template_name = f"{shortcut_id}.cherri.j2"
        template_path = TEMPLATES / template_name

        if not template_path.exists():
            print(f"Warning: template not found: {template_name}")
            continue

        template = env.get_template(template_name)

        # Merge config: api + defaults + shortcut-specific settings
        context = {
            "endpoint": api["endpoint"],
            "auth_header": api["auth_header"],
            "auth_value": api["auth_value"],
            **defaults,
            **settings,
        }

        output = template.render(**context)
        output_path = BUILD / f"{shortcut_id}.cherri"
        output_path.write_text(output)
        generated.append(shortcut_id)
        print(f"Generated: {output_path.name}")

    if generated:
        print(f"\n{len(generated)} file(s) generated in {BUILD}/")
    else:
        print("No files generated")


if __name__ == "__main__":
    main()
