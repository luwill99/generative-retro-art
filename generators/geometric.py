"""Symmetric geometric pattern generator."""

from __future__ import annotations

import math
from pathlib import Path

from .common import ArtConfig, add_background, create_drawing, palette, regular_polygon, rotate_point, seeded_rng


def generate(path: Path, seed: int, config: ArtConfig) -> Path:
    """Draw layered polygons and mirrored line segments around the center."""

    rng, _ = seeded_rng(seed)
    colors = palette(config)
    dwg = create_drawing(path, config)
    add_background(dwg, config, colors)

    cx, cy = config.center
    max_radius = min(config.width, config.height) * 0.43
    stroke_color = "#000000" if config.tshirt_mode else colors[-1]

    # Concentric polygons build the main poster shape.
    for layer in range(config.line_density):
        t = (layer + 1) / config.line_density
        sides = max(3, config.symmetry + (layer % 4) - 1)
        radius = max_radius * t
        rotation = layer * math.pi / max(3, config.symmetry)
        fill = "none" if layer % 2 else colors[(layer + 1) % len(colors)]
        opacity = 0.12 if fill != "none" and not config.tshirt_mode else 1

        dwg.add(
            dwg.polygon(
                points=regular_polygon(cx, cy, radius, sides, rotation),
                fill=fill,
                stroke=stroke_color,
                stroke_width=2 + layer % 3,
                opacity=opacity,
            )
        )

    # A single random segment is copied around the center to create symmetry.
    for _ in range(config.line_density * 4):
        x1 = cx + rng.uniform(-max_radius * 0.65, max_radius * 0.65)
        y1 = cy + rng.uniform(-max_radius * 0.65, max_radius * 0.65)
        x2 = cx + rng.uniform(-max_radius * 0.65, max_radius * 0.65)
        y2 = cy + rng.uniform(-max_radius * 0.65, max_radius * 0.65)

        for arm in range(max(2, config.symmetry)):
            angle = 2 * math.pi * arm / max(2, config.symmetry)
            p1 = rotate_point(x1, y1, angle, config.center)
            p2 = rotate_point(x2, y2, angle, config.center)
            dwg.add(
                dwg.line(
                    start=p1,
                    end=p2,
                    stroke=colors[(arm + 2) % len(colors)] if not config.tshirt_mode else "#000000",
                    stroke_width=1.6,
                    opacity=0.75,
                )
            )

    dwg.save()
    return path
