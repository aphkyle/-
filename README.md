# The xn-m28h presents:
😈 I'M THE EVIL TWIN 😈

Do check [CREDITS.md](CREDITS.md)! Those really helped me a lot!

# Run the game

`cd smiling_imp`

`pip install -r requirements.txt` (sorry, idk how to use poetry/venv)

`python -m src`

# `FileNotFound` Error:
Please modify the source's `constants.py` to the following:
```py
from pathlib import Path


SCREEN_TITLE = "I'M THE EVIL TWIN"
SPRITE_SCALING = 1
TILE_SCALING = 6
CHARACTER_SCALING = 1

SPRITE_IMAGE_SIZE = 32
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = SPRITE_SIZE * 30
SCREEN_HEIGHT = SPRITE_SIZE * 20

ASSETS = Path(__file__).parent.parent / "assets"
```
Guess what, I know your OS is not windows now 😈

# Story
You, J. Doe were a twin of a rich person - J. Dope.

They took away your life, all your money is now theirs.

Your task is to steal everything from their house to take back your revenge.

Who's evil? I guess you both are.

# Development
- [x] Basic Game Menu
- [x] Story Load
- [x] Game
- [x] Game over
- [x] Win

DONE, YAY
