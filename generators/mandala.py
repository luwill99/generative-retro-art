"""Circular mandala-like structure generator."""

from __future__ import annotations

import math
from pathlib import Path

from .common import ArtConfig, add_background, create_drawing, palette, polar_point, seeded_rng


def generate(path: Path, seed: int, config: ArtConfig) -> Path:
    """Create radial petals, rings, and dot patterns."""

    rng, _ = seeded_rng(seed)
    colors = palette(config)
    dwg = create_drawing(path, config)
    add_background(dwg, config, colors)

    cx, cy = config.center
    rings = max(4, config.line_density)
    arms = max(4, config.symmetry)
    max_radius = min(config.width, config.height) * 0.42

    for ring in range(1, rings + 1):
        r = max_radius * ring / rings
        color = "#000000" if config.tshirt_mode else colors[ring % len(colors)]
        dwg.add(dwg.circle(center=(cx, cy), r=r, fill="none", stroke=color, stroke_width=2, opacity=0.82))

        # Petals are closed polygons with points on neighboring rings.
        for arm in range(arms):
            a = 2 * math.pi * arm / arms
            width = math.pi / arms * (0.55 + config.randomness * rng.random())
            inner = max(12, r - max_radius / rings * 0.75)
            outer = r + max_radius / rings * 0.35
            points = [
                polar_point(cx, cy, inner, a - width),
                polar_point(cx, cy, outer, a),
                polar_point(cx, cy, inner, a + width),
                polar_point(cx, cy, max(8, inner * 0.92), a),
            ]
            dwg.add(
                dwg.polygon(
                    points=points,
                    fill="none" if config.tshirt_mode else colors[(ring + arm) % len(colors)],
                    stroke=color,
                    stroke_width=1.5,
                    opacity=0.35 if not config.tshirt_mode else 1,
                )
            )

    for arm in range(arms * 2):
        a = 2 * math.pi * arm / (arms * 2)
        for ring in range(2, rings, 2):
            r = max_radius * ring / rings
            dwg.add(dwg.circle(center=polar_point(cx, cy, r, a), r=5 + ring, fill=colors[-1]))

    dwg.save()
    return path
