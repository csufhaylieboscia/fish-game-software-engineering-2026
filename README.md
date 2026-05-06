# Hooked

**Group Name:** Hooked Development Team  
**Group Members:** Calista Ruiz, Ngoc Le, Haylie Boscia

---

## Description

Hooked is a relaxing 2D fishing game developed in Python using the Pygame library. Players explore a tiled overworld, cast their fishing line, and engage in a timing-based minigame to reel in their catch. The game features a dynamic weather system, multiple fish species of varying rarity, an in-game shop, and a personal aquarium for displaying collected fish.

**Languages:** Python, Pygame  
**IDE:** VS Code

---

## Features

### Fishing Minigame — `fishDiffuculty.py`, `rhythm.py`
When a player initiates a cast, a timing-based minigame is launched. A slider moves across a bar and the player must press the spacebar to land within a target zone. The number of successful hits required and the speed and size of the target zone are all governed by the difficulty level assigned to the fish being caught.

### Fish Difficulty System — `fishDiffuculty.py`
Each fish is assigned a difficulty rating from 1 to 4. Higher difficulty fish have smaller target zones, faster sliders, and require more successful hits before the fish is landed. A progress bar on screen tracks the player's current number of hits toward the required total.

### Fish and Rarity — `fish.py`, `fishDiffuculty.py`
The game includes a roster of standard fish available under normal conditions, as well as a set of rare, special fish that can only be encountered during rain. Rain fish are assigned weighted probabilities ranging from ultra-rare (1 in 1,000) to rare (1 in 200), making certain catches a meaningful achievement.

### Weather and Rain System — `sky.py`, `weather_sprites.py`
A dynamic weather cycle runs in the background during gameplay. Rain periods last three minutes and occur at randomized intervals, with visual rain drop sprites rendered across the map. The active weather state directly influences which fish are available for the player to catch.

### Player and Walkable Areas — `player.py`
The player character navigates a tiled overworld using keyboard input. The character supports idle, run, and fishing animations loaded from sprite sheets, and correctly mirrors sprites based on the direction of movement. Collision and hitbox logic restricts movement to valid walkable areas defined by the tilemap.

### Aquarium — `aquarium.py`
Upon catching a fish, it is registered in the player's aquarium. The aquarium screen renders all collected fish as animated swimming sprites against a layered underwater background complete with light shafts, bubbles, and animated seaweed. Fish swim back and forth across the screen and bob vertically using sine-wave motion.

### Shop — `shop.py`
An in-game shop allows players to spend earned currency on items and upgrades.

### Inventory and Saving — `models.py`, `inventory.py`
Caught fish are tracked in a persistent inventory stored as a JSON file (`player_fish.json`). The inventory records the name, rarity, and count of each species the player has caught and is automatically saved and loaded between sessions.

### Main Menu — `menu.py`, `ui.py`
The main menu features a scrolling parallax water background with layered animation. Menu buttons support hover states and scale correctly when the window is resized or set to fullscreen. Background music plays on loop from the menu screen.

### Display and Fullscreen — `display.py`, `main.py`
The game window is resizable and supports toggling to fullscreen via F11. A render surface is scaled and letterboxed to maintain the base resolution of 800x600 regardless of the window size.

---

## Requirements

This project requires **Python 3.12**. Note that this is a downgrade from newer Python versions — please ensure you have Python 3.12 installed before proceeding.

The following packages are also required:

```
pygame==2.6.1
pygame-menu==4.5.2
pyperclip==1.11.0
PyTMX==3.32
typing_extensions==4.15.0
```

---

## Getting Started

### 1. Clone the Repository

In GitHub, click the **Code** button and copy the HTTPS or SSH link, then run the following in your terminal:

```bash
git clone <copied-link>
```

To verify your local copy is up to date:

```bash
git status
```

If updates are available, pull them:

```bash
git pull
```

### 2. Set Up a Python 3.12 Virtual Environment

Navigate into the project folder, then create and activate a virtual environment using Python 3.12. This step is required as the project is not compatible with newer Python versions.

**macOS / Linux:**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
py -3.12 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment active, install all required packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Game

```bash
python main.py
```

---

## How to Play

1. Launch the game and select **Start** from the main menu.
2. Use **W / A / S / D** or the **arrow keys** to move the player character across the overworld.
3. Approach a body of water and initiate a cast to begin the fishing minigame.
4. When the minigame starts, press **Spacebar** to hit the target zone on the slider bar. The number of successful hits required depends on the fish's difficulty.
5. Upon a successful catch, the fish is added to your inventory and aquarium.
6. Visit the **Shop** to spend your earnings on upgrades.
7. Open the **Aquarium** to view your collected fish swimming in a decorated underwater environment.
8. Fish availability changes based on weather. Keep an eye out for rain, as it unlocks rare species not catchable under normal conditions.
9. Progress is saved automatically between sessions.