"""Shared helpers for clean, editable SVG artwork."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import random
from typing import Iterable

import numpy as np
import svgwrite


PALETTES: dict[str, list[str]] = {
    "synthwave": ["#0B1026", "#FF2E88", "#FFB000", "#19D3FF", "#7A5CFF", "#F4F1DE"],
    "sunset": ["#241734", "#F72585", "#FF9F1C", "#FFE66D", "#4ECDC4", "#FFFFFF"],
    "arcade": ["#101820", "#FEE715", "#FA26A0", "#05DFD7", "#A3F7BF", "#FFFFFF"],
    "miami": ["#11151C", "#00F5D4", "#F15BB5", "#FEE440", "#9B5DE5", "#FFFFFF"],
    "mono": ["#FFFFFF", "#000000"],
}


@dataclass
class ArtConfig:
    """A compact configuration object shared by every generator."""

    width: int = 1600
    height: int = 1600
    line_density: int = 12
    symmetry: int = 8
    recursion_depth: int = 5
    randomness: float = 0.45
    color_count: int = 5
    palette_name: str = "synthwave"
    tshirt_mode: bool = False

    @property
    def center(self) -> tuple[float, float]:
        return self.width / 2, self.height / 2


def seeded_rng(seed: int) -> tuple[random.Random, np.random.Generator]:
    """Return Python and NumPy random generators from the same seed."""

    return random.Random(seed), np.random.default_rng(seed)


def palette(config: ArtConfig) -> list[str]:
    """Choose a reproducible palette slice while keeping black/white mode simple."""

    if config.tshirt_mode:
        return PALETTES["mono"]
    colors = PALETTES.get(config.palette_name, PALETTES["synthwave"])
    return colors[: max(2, min(config.color_count, len(colors)))]


def create_drawing(path: Path, config: ArtConfig) -> svgwrite.Drawing:
    """Create an SVG canvas using simple features Affinity Designer handles well."""

    return svgwrite.Drawing(
        filename=str(path),
        size=(config.width, config.height),
        viewBox=f"0 0 {config.width} {config.height}",
        profile="tiny",
    )


def add_background(dwg: svgwrite.Drawing, config: ArtConfig, colors: list[str]) -> None:
    fill = "#FFFFFF" if config.tshirt_mode else colors[0]
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=fill))


def polar_point(cx: float, cy: float, radius: float, angle: float) -> tuple[float, float]:
    """Convert polar coordinates into SVG x/y coordinates."""

    return cx + math.cos(angle) * radius, cy + math.sin(angle) * radius


def rotate_point(
    x: float,
    y: float,
    angle: float,
    center: tuple[float, float],
) -> tuple[float, float]:
    """Rotate a point around a center; useful for radial symmetry."""

    cx, cy = center
    dx, dy = x - cx, y - cy
    return (
        cx + math.cos(angle) * dx - math.sin(angle) * dy,
        cy + math.sin(angle) * dx + math.cos(angle) * dy,
    )


def regular_polygon(
    cx: float,
    cy: float,
    radius: float,
    sides: int,
    rotation: float = 0.0,
) -> list[tuple[float, float]]:
    return [
        polar_point(cx, cy, radius, rotation + 2 * math.pi * i / sides)
        for i in range(sides)
    ]


def jitter_points(
    points: Iterable[tuple[float, float]],
    rng: random.Random,
    amount: float,
) -> list[tuple[float, float]]:
    """Add small hand-made variation without losing the original geometry."""

    return [(x + rng.uniform(-amount, amount), y + rng.uniform(-amount, amount)) for x, y in points]


def safe_filename(style: str, seed: int) -> str:
    return f"{style}_{seed}.svg"
