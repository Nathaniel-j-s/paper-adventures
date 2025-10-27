# Paper Adventures - Digital Card Game

A PyGame-based card game foundation featuring card rendering, drag-and-drop interaction, and deck management.

## Features

- **Card System**: Customizable cards with attributes
- **Drag-and-Drop**: Smooth card interaction and manipulation
- **Deck Management**: Create, shuffle, and manage card collections
- **Save/Load**: Persistent storage of deck collections

## Requirements

- Python 3.7+
- PyGame 2.5.0+

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Project Structure

```
paper-adventures/
├── main.py                 # Entry point, game loop
├── requirements.txt        # Dependencies
├── src/
│   ├── __init__.py
│   ├── card.py            # Card class and attributes
│   ├── deck.py            # Deck management
│   ├── renderer.py        # Rendering logic
│   ├── input_handler.py   # Mouse/keyboard input
│   └── deck_manager.py    # Save/load decks
├── assets/                # Card graphics (placeholders initially)
└── data/                  # Saved decks
```

## Usage

The game window displays sample cards that can be dragged around. Cards show their name and attributes. More features to come!
