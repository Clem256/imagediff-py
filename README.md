# imagediff-py

A Python image comparison tool using **Binary Spatial Partitioning (BSP)** trees to detect visual differences and
generate difference heatmaps.

---

## Installation

```bash
# Clone the repository
git clone git@github.com:Clem256/imagediff-py.git
cd imagediff-py

# Setup environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install numpy pillow PyQt6
```

---

## Usage

### Command Line Interface (CLI)

**Basic diff:**

```bash
python3 -m core path/to/imgA.png path/to/imgB.png
```

**Generate diff heatmap:**

```bash
python3 -m core path/to/imgA.png path/to/imgB.png --heatmap diff.png
```

**Custom parameters:**

```bash
python3 -m core imgA.png imgB.png --min-block 8 --tolerance 12 --heatmap diff.png
```

### Graphical Interface (GUI)

```bash
python3 -m ui.main_ui
```

or

```bash
python -m ui.main_ui
```