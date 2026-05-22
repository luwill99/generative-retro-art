"""Voronoi-style abstract pattern generator."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from .common import ArtConfig, add_background, create_drawing, jitter_points, palette, polar_point, seeded_rng


def generate(path: Path, seed: int, config: ArtConfig) -> Path:
    """Approximate Voronoi cells with editable irregular polygons.

    Full mathematical Voronoi clipping usually needs SciPy. This version keeps
    dependencies light by drawing local cells around seed points; nearest-neighbor
    distance controls each cell size, which produces a similar organic mosaic.
    """

    rng, np_rng = seeded_rng(seed)
    colors = palette(config)
    dwg = create_drawing(path, config)
    add_background(dwg, config, colors)

    w, h = config.width, config.height
    cell_count = max(12, config.line_density * 5)
    seeds = np.column_stack((np_rng.uniform(90, w - 90, cell_count), np_rng.uniform(90, h - 90, cell_count)))

    for idx, point in enumerate(seeds):
        distances = np.linalg.norm(seeds - point, axis=1)
        nearest = np.partition(distances, 1)[1]
        sides = rng.randint(5, 8)
        radius = nearest * rng.uniform(0.55, 0.82)
        rotation = rng.uniform(0, math.tau)
        points = [
            polar_point(point[0], point[1], radius * rng.uniform(0.72, 1.18), rotation + math.tau * i / sides)
            for i in range(sides)
        ]
        points = jitter_points(points, rng, config.randomness * 12)
        fill = "none" if config.tshirt_mode else colors[(idx + 1) % len(colors)]
        stroke = "#000000" if config.tshirt_mode else colors[-1]
        dwg.add(
            dwg.polygon(
                points=points,
                fill=fill,
                stroke=stroke,
                stroke_width=2,
                opacity=0.55 if fill != "none" else 1,
            )
        )

    dwg.save()
    return path
