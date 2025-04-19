#!/usr/bin/env python3
from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Dict, Type

import click

from engine import ColorWarsEngine
from visualizers.feedback_visualizer import FeedbackVisualizer
from visualizers.ascii_visualizer import AsciiVisualizer
from visualizers.image_visualizer import ImageVisualizer

VISUALIZERS: Dict[str, Type["AbstractVisualizer"]] = {
    "ascii": AsciiVisualizer,
    "image": ImageVisualizer,
}

def _load_config(path_like: str | Path):
    path = Path(path_like)
    if path.exists():
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[path.stem] = mod
            spec.loader.exec_module(mod)
            return mod
        raise ImportError(f"Cannot import config from {path}")
    return importlib.import_module(str(path_like))

@click.group(help="ColorWars CLI")
def cli():
    pass


@cli.command("run")
@click.option("-c", "--config", default="config.py", help="Config file or module.")
@click.option("-o", "--output", type=click.Path(), help="Path to save raw JSON scores.")
@click.option("-m", "--me",
              type=int,
              default=0,
              help="Index of your player in `player_classes` (for highlighting).")
@click.option("-f", "--feedback",
              type=click.Path(),
              default="feedback.json",
              show_default=True,
              help="Path to write minimal feedback JSON for visualization.")
def run(config: str, output: str | None, me: int, feedback: str):
    cfg = _load_config(config)
    try:
        player_classes = cfg.player_classes
        grid_size = cfg.grid_size
        num_games = cfg.num_games
    except AttributeError as err:
        raise click.ClickException("Config must define player_classes, grid_size, num_games") from err

    result = ColorWarsEngine.grade(player_classes, grid_size, num_games)
    result.print_result()

    if output:
        Path(output).write_text(json.dumps(result.scores, indent=2))
        click.echo(f"Saved raw scores to {output}")


@cli.command()
@click.argument("feedback", type=click.Path(exists=True))
@click.option("-v", "--visualizer", default="ascii", type=click.Choice(VISUALIZERS))
@click.option("-o", "--output", type=click.Path(), help="Output file path for visualization.")
@click.option("-g", "--game-index", type=int, help="Render only the N‑th game (0‑based).")
def visualize(feedback: str, visualizer: str, output: str | None, game_index: int | None):
    vis = FeedbackVisualizer(
        feedback_path=Path(feedback),
        vis_cls=VISUALIZERS[visualizer],
        output_path=Path(output) if output else None,
        game_index=game_index,
    )
    click.echo(vis.render())


if __name__ == "__main__":
    cli()
