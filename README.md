# Generative Retro Art

Generative Retro Art is a beginner-friendly Python project for creating editable procedural SVG artwork. The designs are algorithmic: no machine learning, no AI training, and no raster-only tricks.

The generated files use simple SVG shapes such as lines, rectangles, circles, polygons, and polylines so they can be imported into Affinity Designer for T-shirt, poster, and print layout work.

## Included Styles

- Symmetric geometric patterns
- Retro synthwave grids and striped suns
- Fractal-inspired recursive line art
- Voronoi-style abstract patterns
- Circular mandala-like structures
- Randomized abstract poster compositions
- Minimal black-and-white T-shirt mode

## Install

```bash
cd generative-retro-art
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Run

Open the menu:

```bash
python main.py --menu
```

Generate 10 artworks automatically:

```bash
python main.py --style all --count 10
```

Generate only synthwave art:

```bash
python main.py --style synthwave --count 5 --seed 4200
```

Generate minimal black-and-white T-shirt designs:

```bash
python main.py --style all --count 10 --tshirt
```

SVG files are written to the `output/` folder.

## Customization

All important controls are available as command-line options:

```bash
python main.py --style mandala --count 3 --width 2400 --height 2400 --palette miami --symmetry 12 --line-density 18 --color-count 4
```

Useful parameters:

- `--width` and `--height`: SVG export resolution.
- `--line-density`: more lines, rings, cells, or shapes depending on the style.
- `--symmetry`: number of repeated radial arms.
- `--recursion-depth`: fractal branch depth.
- `--randomness`: variation strength. Try values from `0.1` to `1.0`.
- `--color-count`: number of colors used from the palette.
- `--palette`: choose `synthwave`, `sunset`, `arcade`, `miami`, or `mono`.
- `--seed`: reproduce the same artwork later.

## Importing Into Affinity Designer

1. Open Affinity Designer.
2. Choose **File > Open** and select an SVG from the `output/` folder.
3. Ungroup layers if you want to edit individual lines, polygons, circles, or blocks.
4. Adjust strokes, fills, scaling, and layout for your poster or T-shirt composition.

Because the SVGs use simple vector elements, they should remain editable after import.

## Project Structure

```text
generative-retro-art/
|-- main.py
|-- generators/
|   |-- geometric.py
|   |-- synthwave.py
|   |-- fractal.py
|   |-- mandala.py
|   |-- voronoi.py
|   |-- poster.py
|   |-- common.py
|-- output/
|-- requirements.txt
|-- README.md
```

## How It Works

Each generator receives a seed and an `ArtConfig`. The seed makes the random choices reproducible, while the config controls canvas size, density, symmetry, recursion, palette, and T-shirt mode.

The math is intentionally approachable:

- Polar coordinates place points around circles.
- Rotation copies shapes around a center point.
- Recursive functions create fractal branching.
- Nearest-neighbor distances create Voronoi-style cells.
- Perspective lines create the synthwave grid.
