import os
import json
import shutil
import time
from datetime import datetime, timedelta

import rich
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text

CONFIG_FILE = "janitor_config.json"

def load_config():
    """Loads the configuration from the JSON file."""
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def get_file_age_days(file_path):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(file_path)
        return (time.time() - mtime) / (24 * 3600)
    except OSError:
        return 0

def run_janitor(dry_run=False):
    """Runs the main janitor logic."""
    config = load_config()
    if not config:
        console.print(f"[bold red]Error:[/] Config file '{CONFIG_FILE}' not found.")
        return

    console.print(Panel(Text("Desktop Janitor", justify="center", style="bold cyan")))

    folders_to_watch = config.get("folders_to_watch", [])
    rules = config.get("rules", [])
    actions = []

    with Progress(console=console) as progress:
        for folder in folders_to_watch:
            if not os.path.isdir(folder):
                continue

            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            task = progress.add_task(f"[cyan]Scanning {os.path.basename(folder)}...", total=len(files))

            for filename in files:
                progress.update(task, advance=1)
                time.sleep(0.01) # Simulate work
                
                file_path = os.path.join(folder, filename)
                
                for rule in rules:
                    conditions = rule.get("conditions", {})
                    matches = True

                    # Check source folder condition
                    if "source_folder" in conditions and folder != conditions["source_folder"]:
                        matches = False

                    # Check extension condition
                    if "extensions" in conditions:
                        if not any(filename.lower().endswith(ext) for ext in conditions["extensions"]):
                            matches = False
                    
                    # Check filename contains condition
                    if "filename_contains" in conditions:
                        if not any(keyword.lower() in filename.lower() for keyword in conditions["filename_contains"]):
                            matches = False

                    # Check age condition
                    if "age_days" in conditions:
                        if get_file_age_days(file_path) < conditions["age_days"]:
                            matches = False

                    if matches:
                        action = rule.get("action", "move")
                        destination = rule.get("destination")
                        
                        if action == "move":
                            if not destination:
                                continue
                            if not dry_run:
                                os.makedirs(destination, exist_ok=True)
                                shutil.move(file_path, os.path.join(destination, filename))
                            actions.append(("Moved", filename, destination))
                        elif action == "delete":
                            if not dry_run:
                                os.remove(file_path)
                            actions.append(("Deleted", filename, "N/A"))
                        break # Stop processing rules for this file

    # Print summary table
    if actions:
        table = Table(title="Janitor Actions Summary", style="cyan")
        table.add_column("Action", style="magenta")
        table.add_column("File", style="green")
        table.add_column("Destination", style="blue")

        for action, filename, destination in actions:
            table.add_row(action, filename, destination)
        
        console.print(table)
    else:
        console.print("[bold green]No actions were needed. Everything is tidy! :sparkles:")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="A CLI tool to clean up your desktop and other folders.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the cleanup without actually moving or deleting files.")
    args = parser.parse_args()

    console = Console()
    run_janitor(dry_run=args.dry_run)
    console.input("\n[bold yellow]Press Enter to exit...[/]")
