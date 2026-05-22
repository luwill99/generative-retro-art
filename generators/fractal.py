"""Fractal-inspired recursive line art generator."""

from __future__ import annotations

import math
from pathlib import Path

from .common import ArtConfig, add_background, create_drawing, palette, polar_point, seeded_rng


def _branch(dwg, start, length, angle, depth, rng, colors, config):
    """Recursive branching: each line creates two smaller child lines."""

    if depth <= 0 or length < 6:
        return

    end = polar_point(start[0], start[1], length, angle)
    color = "#000000" if config.tshirt_mode else colors[depth % len(colors)]
    dwg.add(
        dwg.line(
            start=start,
            end=end,
            stroke=color,
            stroke_width=max(1.0, depth * 0.9),
            opacity=0.9,
        )
    )

    spread = math.radians(18 + config.randomness * rng.uniform(10, 34))
    shrink = 0.66 + rng.uniform(-0.08, 0.05)
    _branch(dwg, end, length * shrink, angle - spread, depth - 1, rng, colors, config)
    _branch(dwg, end, length * shrink, angle + spread, depth - 1, rng, colors, config)


def generate(path: Path, seed: int, config: ArtConfig) -> Path:
    """Place several recursive trees in radial arrangement."""

    rng, _ = seeded_rng(seed)
    colors = palette(config)
    dwg = create_drawing(path, config)
    add_background(dwg, config, colors)

    cx, cy = config.center
    arms = max(3, config.symmetry)
    base_length = min(config.width, config.height) * 0.16

    for arm in range(arms):
        angle = -math.pi / 2 + 2 * math.pi * arm / arms
        start = polar_point(cx, cy, min(config.width, config.height) * 0.08, angle + math.pi)
        _branch(
            dwg,
            start,
            base_length,
            angle,
            max(1, config.recursion_depth),
            rng,
            colors,
            config,
        )

    dwg.add(dwg.circle(center=(cx, cy), r=base_length * 0.28, fill="none", stroke=colors[-1], stroke_width=3))
    dwg.save()
    return path
