# Desktop Janitor :broom:

A sleek, configurable CLI tool to automatically organize your files and keep your folders tidy.

![Desktop Janitor Demo](https://i.imgur.com/example.gif)  <!-- Replace with a real demo GIF if you make one! -->

## Features

- **Rule-Based Sorting:** Clean up files based on their extension, name, age, and more.
- **Highly Configurable:** Define your own rules in a simple `janitor_config.json` file.
- **Beautiful CLI:** A modern, user-friendly interface with spinners, progress bars, and summary tables.
- **Safe Dry Runs:** Preview the changes before they happen with the `--dry-run` flag.
- **Cross-Platform:** Built with Python, so it runs on Windows, macOS, and Linux.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/xaviersupreme/Desktop-Janitor.git
    cd desktop-janitor
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Configure your rules:**
    Open the `janitor_config.json` file and customize it to your needs. You can add, remove, or edit the rules to match your workflow.

    -   `folders_to_watch`: A list of folders you want the janitor to clean.
    -   `rules`: A list of sorting rules. The janitor will apply the first rule that a file matches.

2.  **Run a dry run (recommended):**
    To see what changes the janitor will make without actually moving any files, use the `--dry-run` flag.
    ```bash
    python desktop_janitor.py --dry-run
    ```

3.  **Run the janitor:**
    When you're ready, run the script without any flags to start the cleanup.
    ```bash
    python desktop_janitor.py
    ```

## Example Rule

Here's an example of a rule that moves all `.png` files with "screenshot" in their name to a specific folder:

```json
{
    "name": "Screenshots",
    "destination": "C:\Users\YourUser\Pictures\Screenshots",
    "conditions": {
        "extensions": [".png"],
        "filename_contains": ["screenshot"]
    }
}
```

## Contributing

Contributions are welcome! If you have any ideas for new features or improvements, feel free to open an issue or submit a pull request.

```
