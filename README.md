# Pyxel Pet Simulator

A simple retro simulation game built with Python and Pyxel.

## Requirements

- Python 3.12 or newer
- uv
- Pyxel-compatible desktop environment

## Installation

Clone the repository:

```bash
git clone https://github.com/yazdannejat/pyxel-pet-simulator.git
cd pyxel-pet-simulator
```

Install dependencies:

```bash
uv sync
```

## Run the game

```bash
uv run pet-simulator
```

Alternatively:

```bash
uv run python -m pet_simulator.game
```

## Controls

- Arrow keys: Move spaceship
- Space: Shoot
- R: Restart after game over

## Development

Run the game using:

```bash
uv run pet-simulator
```

Dependencies are managed by uv using `pyproject.toml` and `uv.lock`.

## License

MIT
