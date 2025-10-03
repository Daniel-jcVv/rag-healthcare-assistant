# Demo Images

This directory contains screenshots and demo materials for the project.

## TODO: Add the following

1. **demo.gif** - Animated GIF showing chat interaction (using Peek or similar)
2. **ui-screenshot.png** - Screenshot of the chat interface
3. **architecture-diagram.png** - Visual architecture diagram (optional)

## How to create demo.gif

### Option 1: Using Peek (Linux)
```bash
sudo apt install peek  # or your package manager
peek
# Record 10-15 seconds of interaction
# Save as demo.gif
```

### Option 2: Using OBS Studio
```bash
# Record video with OBS
# Convert to GIF using ffmpeg:
ffmpeg -i demo.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" demo.gif
```

### What to show in demo:
1. Open http://localhost:5000
2. Type question: "What is diabetes?"
3. Wait for response
4. Show answer + sources
5. (Optional) Ask second question

Keep it under 15 seconds for fast loading!
