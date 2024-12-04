# Bucket Catch Game

A fun and interactive game where players control a bucket to catch falling objects. As you progress, the game becomes more challenging with increasing object and bucket speeds. The game supports a server-client architecture, allowing controls from a client machine.

## Features
- **Dynamic Gameplay**: Falling objects speed up as you collect more of them.
- **Server-Client Architecture**: The game display runs on the server, while the client handles controls.
- **Restart and Quit Options**: Seamlessly restart the game or quit at any time.
- **Customizable Design**:
  - Change object and bucket shapes.
  - Modify colors for various elements.
  - Add a background image for enhanced visuals.

## How to Play
1. **Start the Game**:
   - Launch the server (`GameServer.py`) and client (`GameClient.py`).
   - Press the **Spacebar** on the client to start the game.

2. **Control the Bucket**:
   - Use the following keys:
     - `W`: Move up
     - `A`: Move left
     - `S`: Move down
     - `D`: Move right

3. **Catch Objects**:
   - Control the bucket to catch as many falling objects as possible.
   - Avoid letting the objects reach the bottom of the screen.

4. **Restart or Quit**:
   - Press `V` (or your configured key) to restart the game.
   - Press `Q` to quit the game.

## Installation
### Requirements
- Python 3.8 or higher
- `pygame` library
- `keyboard` library

### Steps to Install
1. Clone or download this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
