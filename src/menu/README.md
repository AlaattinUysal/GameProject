# Game Menu

## Proje Yapısı

```
src-menu/
├── menu/              
│   ├── init.py         # Package initialization
│   ├── constants.py    # Constants, configurations and shared settings
│   ├── assets.py       # Assets loading (fonts, backgrounds, characters, music)
│   ├── ui.py           # UI components (buttons, sliders, text input boxes)
│   ├── scenes.py       # Different menu screens (main menu, options, settings, etc.)
│   └── main.py         # Main Menu class that handles the scene system and game flow
|--menu.py   #should be seperated menu/ file
├── .gitignore
├── README.md
└── LICENSE
```
# The Way

"The Way" is a 2D platformer game built with Pygame that features samurai characters, multiple levels, skill upgrades, and various game mechanics.

## System Requirements

- Windows 10 or newer
- Minimum 4GB RAM
- 500MB free disk space

## Software Requirements

- Python 3.13.0 or compatible version
- Pygame 2.6.1 or newer
- NumPy 2.2.5 or newer

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install pygame numpy
```

## Usage

1. Run the game menu:

```bash
python 1src/menu.py
```

2. Navigate through the menu using your mouse:
   - **Play**: Start a new game
   - **Shop**: Purchase upgrades and skills
   - **Leaderboard**: View high scores
   - **Options**: Access game settings
   - **Login**: Create/access your profile

3. In the Options menu, you can:
   - Resume game
   - Restart game
   - Select levels
   - Adjust settings (music, sound, brightness)
   - Quit the game

4. Press **F11** to toggle fullscreen mode
5. Press **ESC** to go back or access the options menu during gameplay

## Game Features

- **Multiple levels** with increasing difficulty
- **Shop system** to purchase skills and upgrades
- **User profiles** with persistent progress
- **Settings customization** (music, sound effects, brightness)
- **Samurai characters** with unique abilities
- **Platformer gameplay** with double-jumping and item collection
- **Responsive pixel-art UI** with modern design

## Controls

- **Arrow keys/WASD**: Move character
- **Space**: Jump (press twice for double jump)
- **Mouse**: Interact with menus and UI

## Troubleshooting

If you encounter import errors when running the game, make sure that:
1. You're running the game from the main project directory
2. You have all the required dependencies installed
3. Your Python environment is set up correctly

## Development

The code has been modularized for easier maintenance and future enhancements. Each module handles a specific part of the game:

- `config.py`: Contains all configurable settings
- `assets.py`: Manages loading of game assets
- `ui.py`: Contains UI component classes
- `scenes.py`: Manages different menu scenes
- `main.py`: Controls the game flow and menu logic

## License

This project is released under the MIT License.
