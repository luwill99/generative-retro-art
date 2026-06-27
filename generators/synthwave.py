"""Retro synthwave grid and sun generator."""

from __future__ import annotations

import math
from pathlib import Path

from .common import ArtConfig, add_background, create_drawing, palette, polar_point, seeded_rng


def generate(path: Path, seed: int, config: ArtConfig) -> Path:
    """Draw a perspective grid, striped sun, and simple mountain silhouettes."""

    rng, _ = seeded_rng(seed)
    colors = palette(config)
    dwg = create_drawing(path, config)
    add_background(dwg, config, colors)

    w, h = config.width, config.height
    horizon = h * 0.55
    cx = w / 2
    grid_color = "#000000" if config.tshirt_mode else colors[3 % len(colors)]
    sun_color = "#000000" if config.tshirt_mode else colors[2 % len(colors)]

    # Sun stripes are separate rectangles clipped only by their own position,
    # keeping the SVG easy to edit after import.
    sun_radius = min(w, h) * 0.19
    for i in range(10):
        sun_center_y = horizon + sun_radius * 0.05
        y = sun_center_y - sun_radius + i * sun_radius * 0.2
        stripe_h = sun_radius * 0.12

        if y + stripe_h > horizon:
            continue

        half_width = math.sqrt(max(0, sun_radius**2 - (y + stripe_h / 2 - sun_center_y) ** 2))
        dwg.add(
            dwg.rect(
                insert=(cx - half_width, y),
                size=(2 * half_width, stripe_h),
                fill=sun_color,
                opacity=0.85,
            )
        )

    # Mountains are editable polylines rather than a raster silhouette.
    points = [(0, horizon)]
    for i in range(9):
        x = w * i / 8
        y = horizon - rng.uniform(h * 0.06, h * 0.18)
        points.append((x, y))
    points.append((w, horizon))
    dwg.add(dwg.polyline(points=points, fill="none", stroke=colors[-1], stroke_width=5))

    # Horizontal grid lines get closer together near the horizon.
    for i in range(1, config.line_density + 10):
        t = i / (config.line_density + 10)
        y = horizon + (h - horizon) * (t**1.8)
        dwg.add(dwg.line(start=(0, y), end=(w, y), stroke=grid_color, stroke_width=2, opacity=0.8))

    # Lines radiating from the vanishing point make the flat grid feel 3D.
    for i in range(-config.line_density, config.line_density + 1):
        x = cx + i * w / max(1, config.line_density)
        dwg.add(dwg.line(start=(cx, horizon), end=(x, h), stroke=grid_color, stroke_width=2, opacity=0.8))

    # A few orbital arcs add motion without relying on gradients or filters.
    for r in [sun_radius * 1.45, sun_radius * 1.7, sun_radius * 2.0]:
        pts = [polar_point(cx, horizon, r, math.radians(a)) for a in range(205, 336, 5)]
        dwg.add(dwg.polyline(points=pts, fill="none", stroke=colors[1 % len(colors)], stroke_width=2, opacity=0.65))

    dwg.save()
    return path
