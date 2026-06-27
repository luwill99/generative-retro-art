"""Detailed flower mandala generator."""

from __future__ import annotations

import math
from pathlib import Path

from .common import ArtConfig, add_background, create_drawing, palette, polar_point, seeded_rng


def _petal_points(cx, cy, inner, outer, angle, width, resolution=50):
    """Create one closed pointed petal using polar coordinates."""
    length = outer - inner
    points = []

    # left edge: base -> tip
    for i in range(resolution):
        t = i / (resolution - 1)
        r = inner + length * t

        # width is zero at base and tip, maximal around the middle
        local_width = width * (math.sin(math.pi * t) ** 0.85)

        theta = angle - local_width
        points.append(polar_point(cx, cy, r, theta))

    # right edge: tip -> base
    for i in range(resolution - 1, -1, -1):
        t = i / (resolution - 1)
        r = inner + length * t
        local_width = width * (math.sin(math.pi * t) ** 0.85)

        theta = angle + local_width
        points.append(polar_point(cx, cy, r, theta))

    return points




def _draw_petal_ring(
    dwg,
    cx,
    cy,
    inner,
    outer,
    arms,
    width,
    stroke,
    fill= None,
    stroke_width=2.0,
    rotation=0.0,
    vein_count=5,
):
    """Draw a full ring of flower petals."""
    for arm in range(arms):
        angle = rotation + 2 * math.pi * arm / arms
        points = _petal_points(cx, cy, inner, outer, angle, width)

        dwg.add(
            dwg.polygon(
                points=points,
                fill=fill,
                fill_opacity=0.25,
                stroke=stroke,
                stroke_width=stroke_width,
                opacity=1.0,
            )
        )

        # center vein
        dwg.add(
            dwg.line(
                start=polar_point(cx, cy, inner, angle),
                end=polar_point(cx, cy, outer, angle),
                stroke=stroke,
                stroke_width=max(0.6, stroke_width * 0.45),
                opacity=0.85,
            )
        )

        # side veins
        length = outer - inner
        for j in range(1, vein_count + 1):
            t = j / (vein_count + 1)
            r = inner + length * t
            local_width = width * (math.sin(math.pi * t) ** 0.85)

            center = polar_point(cx, cy, r, angle)
            left = polar_point(cx, cy, r + length * 0.035, angle - local_width * 0.45)
            right = polar_point(cx, cy, r + length * 0.035, angle + local_width * 0.45)

            dwg.add(dwg.line(start=center, end=left, stroke=stroke, stroke_width=0.8, opacity=0.75))
            dwg.add(dwg.line(start=center, end=right, stroke=stroke, stroke_width=0.8, opacity=0.75))


def _draw_detail_ring(dwg, cx, cy, radius, arms, stroke):
    """Small decorative arcs/circles without the old giant dot pattern."""
    for arm in range(arms):
        angle = 2 * math.pi * arm / arms
        p = polar_point(cx, cy, radius, angle)
        dwg.add(dwg.circle(center=p, r=4, fill="none", stroke=stroke, stroke_width=1.4))


def generate(path: Path, seed: int, config: ArtConfig) -> Path:
    """Create a detailed black-and-white flower mandala."""

    rng, _ = seeded_rng(seed)
    colors = palette(config)
    dwg = create_drawing(path, config)
    add_background(dwg, config, colors)

    cx, cy = config.center
    size = min(config.width, config.height)
    stroke = "#000000" if config.tshirt_mode else colors[-1]

    arms = max(12, config.symmetry * 2)
    # Manual mandala controls
    mandala_rings = 3          # how many petal layers
    arms = 16                  # number of petals per ring
    mandala_scale = 0.75       # overall size, 1.0 = large
    outer_width_scale = 0.9    # smaller = less overlap
    show_veins = True
    show_detail_circles = True

    # Clean flower style
    if config.tshirt_mode:
        stroke = "#000000"
    else:
        stroke = colors[-1]

    # configurable mandala layers
    layers = [
        (0.035, 0.135, 0.75, 1.5, math.pi / arms, 3),
        (0.10,  0.27,  0.95, 2.0, 0.0,           4),
        (0.20,  0.43,  0.85, 2.4, math.pi / arms, 5),
        (0.34,  0.68,  0.72, 3.0, 0.0,           6),
    ]

    for inner_f, outer_f, width_f, stroke_w, rotation, veins in layers[:mandala_rings]:

        ring_color = colors[(layers.index((inner_f, outer_f, width_f, stroke_w, rotation, veins)) + 1) % len(colors)]

        _draw_petal_ring(
            dwg,
            cx,
            cy,
            inner=size * inner_f * mandala_scale,
            outer=size * outer_f * mandala_scale,
            arms=arms,
            width=math.pi / arms * width_f * outer_width_scale,
            stroke=ring_color,
            fill=ring_color if not config.tshirt_mode else "none",
            stroke_width=stroke_w,
            rotation=rotation,
            vein_count=veins if show_veins else 0,
        )

    # thin construction/detail circles
    for radius in [0.075, 0.145, 0.285, 0.455, 0.68]:
        dwg.add(
            dwg.circle(
                center=(cx, cy),
                r=size * radius,
                fill="none",
                stroke=stroke,
                stroke_width=1.2,
                opacity=0.55,
            )
        )

    # small subtle decorative ring, not huge filled dots
    _draw_detail_ring(dwg, cx, cy, size * 0.075, arms, stroke)

    # central circles
    dwg.add(dwg.circle(center=(cx, cy), r=size * 0.035, fill="none", stroke=stroke, stroke_width=2.2))
    dwg.add(dwg.circle(center=(cx, cy), r=size * 0.018, fill="none", stroke=stroke, stroke_width=1.5))

    dwg.save()
    return path