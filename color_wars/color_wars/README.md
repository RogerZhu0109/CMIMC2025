# Color Wars Starter Code

## Directory Structure

```
color_wars/
├── config.py                 # Configure players, grid size, and game count
├── engine.py                 # Core game logic
├── players/                  # Player implementations
│   ├── player.py             # Base Player abstract class
│   ├── random.py             # Example random player
│   └── stupid.py             # Example minimal player
├── visualizers/              # Visualization tools
│   ├── abstract.py           # Abstract visualizer class
│   ├── ascii_visualizer.py   # ASCII visualization backend
│   ├── image_visualizer.py   # GIF visualization backend
│   └── feedback_visualizer.py# Adapter for grader feedback JSON
├── submission.py             # Template for your submission
├── cli.py                    # CLI utility for running and visualizing games
└── debug.log                 # Debug logs appear here
├── requirements.txt          # Python dependencies
```

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Local Testing

### Step 1: Implement Your Player
- Create a new player by subclassing the `Player` class (`players/player.py`) inside the `players` directory.
- See provided examples: `players/random.py` and `players/stupid.py`.

### Step 2: Configure the Game
- Open `config.py`:
  - Add your player class to `player_classes`.
  - Set the grid size (`grid_size`) and number of games (`num_games`).

### Step 3: Run the Game
Use the CLI:

```bash
python cli.py run
```

This runs the configured players, displaying results in the terminal.

#### CLI Parameters

The `run` command supports the following options:

- `-c`, `--config` *(default: "config.py")*: Path to the configuration file or module.
- `-o`, `--output`: Optional path to save the raw JSON scores.
- `-m`, `--me` *(default: 0)*: Index of your player in the `player_classes` list (used for highlighting).
- `-f`, `--feedback` *(default: "feedback.json")*: Path to write feedback JSON for visualization.

Example usage:

```bash
python cli.py run --config my_config.py --output scores.json --me 2 --feedback my_feedback.json
```

## Visualization

To visualize game states from grader feedback JSON:

```bash
python cli.py visualize <path_to_feedback.json> [-v ascii|image]
```

- Default visualization: `ascii`.
- Image visualization (`image`) generates an animated GIF.

## Submission

### Prepare Your Submission
- Edit `submission.py` and implement your logic in the `SubmissionPlayer` class.
- **Important Submission Rules:**
  - Keep the class name as `SubmissionPlayer`.
  - Avoid using `print()` statements.
  - Leave provided execution code unchanged.

### Debugging Your Submission
- Use Python's `logging.debug()` instead of `print`.
- Debug statements are recorded in `debug.log`.

### Submit Your Player
- Upload only your completed `submission.py` file to the contest website.