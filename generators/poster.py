"""Randomized abstract poster composition generator."""

from __future__ import annotations

from pathlib import Path

from .common import ArtConfig, add_background, create_drawing, palette, regular_polygon, seeded_rng


def generate(path: Path, seed: int, config: ArtConfig) -> Path:
    """Compose circles, blocks, lines, and polygons into a retro poster."""

    rng, _ = seeded_rng(seed)
    colors = palette(config)
    dwg = create_drawing(path, config)
    add_background(dwg, config, colors)

    w, h = config.width, config.height
    count = max(18, config.line_density * 4)
    stroke = "#000000" if config.tshirt_mode else colors[-1]

    for i in range(count):
        x = rng.uniform(w * 0.08, w * 0.92)
        y = rng.uniform(h * 0.08, h * 0.92)
        size = rng.uniform(w * 0.035, w * 0.17) * (0.7 + config.randomness)
        color = "#000000" if config.tshirt_mode else colors[i % len(colors)]
        shape = rng.choice(["circle", "rect", "poly", "line"])

        if shape == "circle":
            dwg.add(dwg.circle(center=(x, y), r=size / 2, fill="none", stroke=color, stroke_width=4, opacity=0.9))
        elif shape == "rect":
            dwg.add(
                dwg.rect(
                    insert=(x - size / 2, y - size / 2),
                    size=(size, size * rng.uniform(0.35, 1.4)),
                    fill="none" if config.tshirt_mode else color,
                    stroke=stroke,
                    stroke_width=2,
                    opacity=0.45 if not config.tshirt_mode else 1,
                )
            )
        elif shape == "poly":
            dwg.add(
                dwg.polygon(
                    points=regular_polygon(x, y, size / 2, rng.randint(3, 7), rng.random()),
                    fill="none",
                    stroke=color,
                    stroke_width=3,
                )
            )
        else:
            dwg.add(
                dwg.line(
                    start=(x - size, y),
                    end=(x + size, y + rng.uniform(-size, size)),
                    stroke=color,
                    stroke_width=rng.uniform(2, 8),
                    opacity=0.9,
                )
            )

    dwg.save()
    return path
