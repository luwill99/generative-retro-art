"""Generative Retro Art command-line menu.

Run this file to create editable SVG artworks for Affinity Designer.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from generators.common import ArtConfig, PALETTES, safe_filename
from generators import fractal, geometric, mandala, poster, synthwave, voronoi


Generator = Callable[[Path, int, ArtConfig], Path]

GENERATORS: dict[str, Generator] = {
    "geometric": geometric.generate,
    "synthwave": synthwave.generate,
    "fractal": fractal.generate,
    "mandala": mandala.generate,
    "voronoi": voronoi.generate,
    "poster": poster.generate,
}


def build_config(args: argparse.Namespace) -> ArtConfig:
    return ArtConfig(
        width=args.width,
        height=args.height,
        line_density=args.line_density,
        symmetry=args.symmetry,
        recursion_depth=args.recursion_depth,
        randomness=args.randomness,
        color_count=args.color_count,
        palette_name=args.palette,
        tshirt_mode=args.tshirt,
    )


def generate_artworks(styles: list[str], count: int, seed: int, output: Path, config: ArtConfig) -> list[Path]:
    """Generate several artworks while keeping every seed reproducible."""

    output.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for index in range(count):
        style = styles[index % len(styles)]
        artwork_seed = seed + index
        path = output / f"{style}_{config.palette_name}_{artwork_seed}.svg"
        GENERATORS[style](path, artwork_seed, config)
        created.append(path)

    return created


def menu() -> argparse.Namespace:
    """Simple beginner-friendly text menu for interactive use."""

    print("\nGenerative Retro Art")
    print("====================")
    print("Choose a style:")
    print("  1. all styles")
    for number, name in enumerate(GENERATORS, start=2):
        print(f"  {number}. {name}")

    choice = input("Style number [1]: ").strip() or "1"
    palette_name = input(f"Palette {list(PALETTES)} [synthwave]: ").strip() or "synthwave"
    count = int(input("Number of artworks [10]: ").strip() or "10")
    seed = int(input("Seed [1000]: ").strip() or "1000")
    tshirt = (input("Black-and-white T-shirt mode? y/N: ").strip().lower() == "y")

    style_names = list(GENERATORS)
    if choice == "1":
        style = "all"
    else:
        style = style_names[max(0, min(len(style_names) - 1, int(choice) - 2))]

    return argparse.Namespace(
        style=style,
        count=count,
        seed=seed,
        width=1600,
        height=1600,
        line_density=12,
        symmetry=8,
        recursion_depth=5,
        randomness=0.45,
        color_count=5,
        palette=palette_name,
        tshirt=tshirt,
        output=Path("output"),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate procedural retro SVG artworks.")
    parser.add_argument("--style", choices=["all", *GENERATORS.keys()], default=None, help="Artwork style to generate.")
    parser.add_argument("--count", type=int, default=10, help="Number of SVG files to export.")
    parser.add_argument("--seed", type=int, default=1000, help="Base random seed for reproducible output.")
    parser.add_argument("--width", type=int, default=1600, help="SVG canvas width.")
    parser.add_argument("--height", type=int, default=1600, help="SVG canvas height.")
    parser.add_argument("--line-density", type=int, default=12, help="Controls grid lines, rings, and shape count.")
    parser.add_argument("--symmetry", type=int, default=8, help="Radial symmetry amount.")
    parser.add_argument("--recursion-depth", type=int, default=5, help="Depth for recursive fractal line art.")
    parser.add_argument("--randomness", type=float, default=0.45, help="Random variation from 0.0 to about 1.0.")
    parser.add_argument("--color-count", type=int, default=5, help="Number of colors used from the chosen palette.")
    parser.add_argument("--palette", choices=PALETTES.keys(), default="synthwave", help="Color palette.")
    parser.add_argument("--tshirt", action="store_true", help="Generate minimal black-and-white artwork.")
    parser.add_argument("--output", type=Path, default=Path("output"), help="Output directory for SVG files.")
    parser.add_argument("--menu", action="store_true", help="Open the interactive menu.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.menu or args.style is None:
        args = menu()

    styles = list(GENERATORS) if args.style == "all" else [args.style]
    config = build_config(args)
    created = generate_artworks(styles, max(1, args.count), args.seed, args.output, config)

    print(f"\nCreated {len(created)} SVG artworks:")
    for path in created:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
