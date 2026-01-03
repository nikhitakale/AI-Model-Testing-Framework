# Creating Your Demo Video

Here's how to create and add a demo video to your README:

## Recording the Demo

### Option 1: Terminal Recording (Recommended for CLI)

**Using asciinema** (Creates a shareable web player):
```bash
# Install
brew install asciinema  # macOS
# or: pip install asciinema

# Record your demo
asciinema rec demo.cast

# Then run your commands:
python cli/main.py list-tests
python cli/main.py test-llm --prompt "What is machine learning?"
# Press Ctrl+D when done

# Upload to asciinema.org
asciinema upload demo.cast
# You'll get a shareable link!
```

**Using terminalizer** (Creates an animated GIF):
```bash
# Install
npm install -g terminalizer

# Record
terminalizer record demo

# Run your commands, then Ctrl+D to stop

# Render as GIF
terminalizer render demo
```

### Option 2: Screen Recording

**macOS (Built-in)**:
1. Press `Cmd + Shift + 5`
2. Select "Record Selected Portion"
3. Choose your terminal window
4. Click Record
5. Run your demo commands
6. Stop recording (menu bar icon)

**Tools**:
- **Kap** (macOS): https://getkap.co - Great for GIFs
- **OBS Studio** (All platforms): https://obsproject.com - Professional
- **LICEcap** (Windows/macOS): Simple GIF recorder

## What to Show in Your Demo

Create a 1-2 minute demo showing:

1. **Quick Setup** (5-10 seconds)
   ```bash
   source .venv/bin/activate
   python cli/main.py list-tests
   ```

2. **LLM Testing** (20-30 seconds)
   ```bash
   python cli/main.py test-llm --prompt "Explain machine learning in simple terms"
   ```

3. **Performance Test** (15-20 seconds)
   ```bash
   python cli/main.py test-performance --num-requests 10
   ```

4. **Bias Detection** (15-20 seconds)
   ```bash
   python cli/main.py test-bias
   ```

5. **Report Generation** (10 seconds)
   ```bash
   python cli/main.py generate-report
   ls reports/
   ```

## Adding to README

### Option A: Video File in Repo

1. Record your video (MP4 or MOV)
2. Keep it under 10MB if possible (compress if needed)
3. Create an `assets/` folder
4. Add to your repo:
   ```bash
   mkdir -p assets
   mv demo.mp4 assets/
   git add assets/demo.mp4
   ```

5. Update README:
   ```markdown
   ## Quick Demo
   
   https://github.com/YOUR_USERNAME/YOUR_REPO/assets/demo.mp4
   
   <!-- Or use relative path -->
   ![Demo](./assets/demo.mp4)
   ```

### Option B: GIF (Best for README)

1. Record and convert to GIF (max 10MB recommended)
2. Add to assets folder
3. Embed in README:
   ```markdown
   ## Quick Demo
   
   ![Framework Demo](./assets/demo.gif)
   ```

### Option C: External Hosting (Recommended for Large Videos)

**YouTube**:
1. Upload to YouTube
2. Get embed link
3. Add to README:
   ```markdown
   ## Quick Demo
   
   [![Watch the demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
   ```

**Asciinema** (For Terminal):
```markdown
## Quick Demo

[![asciicast](https://asciinema.org/a/YOUR_ID.svg)](https://asciinema.org/a/YOUR_ID)
```

**Loom/Vimeo**:
- Upload video
- Get shareable link
- Add to README with a preview image

## Tips for a Great Demo

1. **Clean your terminal**: Use a nice color scheme
2. **Set up your prompt**: Make it simple and readable
3. **Use clear commands**: Type slowly or edit the recording
4. **Show real output**: Don't mock the API responses if possible
5. **Keep it short**: 1-2 minutes max
6. **Add captions**: Use tools like Kapwing if needed

## Compressing Videos

**For MP4**:
```bash
# Install ffmpeg
brew install ffmpeg

# Compress video
ffmpeg -i demo.mp4 -vcodec h264 -acodec aac -vf scale=1280:-1 demo_compressed.mp4
```

**For GIF**:
```bash
# Convert video to GIF
ffmpeg -i demo.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" -c:v gif demo.gif

# Or use gifsicle to optimize
brew install gifsicle
gifsicle -O3 --colors 256 demo.gif -o demo_optimized.gif
```

## Current README Setup

I've already added a demo section placeholder in your README. Once you record your video:

1. Upload it to your preferred platform
2. Replace the placeholder link in README.md
3. Commit and push!

## Example Demo Script

Here's a script you can follow:

```bash
# Terminal 1: Show the setup
echo "AI Model Testing Framework Demo"
echo "================================"
echo ""

# Show available tests
python cli/main.py list-tests

# Run LLM test
echo ""
echo "Let's test an LLM..."
python cli/main.py test-llm --prompt "What is the future of AI testing?"

# Run performance test
echo ""
echo "How about performance?"
python cli/main.py test-performance --num-requests 5

# Show report
echo ""
echo "And here are the results!"
ls -lh reports/

# Open report (optional)
open reports/test_report.html
```

Ready to record your awesome demo!
