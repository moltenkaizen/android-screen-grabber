# Android Screenshot Grabber

A simple, interactive Python CLI tool to capture screenshots from Android devices via ADB. Perfect for documenting app flows, creating tutorials, or testing mobile applications.

## Features

- **Interactive mode**: Type screen names as you capture for organized screenshots
- **Auto-naming**: Press ENTER for automatic timestamped filenames
- **Device detection**: Automatically checks ADB connection and device status
- **Display resolution info**: Shows both physical and logical (dp) resolutions - helpful for design QA work
- **Clean output**: Screenshots saved locally with descriptive filenames
- **Single-shot mode**: Capture one screenshot and exit (great for scripts)
- **No dependencies**: Uses only Python standard library + ADB

## Requirements

- Python 3.6+
- Android Debug Bridge (ADB)
- Android device with USB debugging enabled

### Installing ADB

**macOS:**
```bash
brew install android-platform-tools
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install android-tools-adb
```

**Windows:**
Download from [Android Developer Tools](https://developer.android.com/studio/releases/platform-tools)

## Setup

1. Enable USB debugging on your Android device:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings → Developer Options
   - Enable "USB Debugging"

2. Connect your device via USB and authorize the computer when prompted

3. Clone this repository:
```bash
git clone https://github.com/moltenkaizen/android-screen-grabber.git
cd android-screen-grabber
```

4. Make the script executable (optional):
```bash
chmod +x android-screen-grabber.py
```

## Usage

### Interactive Mode (Recommended)

The most common way to use the tool:

```bash
python android-screen-grabber.py
```

You'll see a prompt where you can:
- **Type a screen name** (e.g., `login`, `dashboard`) and press ENTER to capture with that name
- **Press ENTER** without typing for auto-numbered screenshots
- **Type `i`** and press ENTER to display device and resolution info
- **Type `q`** and press ENTER to quit

**Example session:**
```
Enter screen name (or ENTER for auto, i=info, q=quit): login
📸 Capturing screenshot... ✅ Saved: screenshots/login_20231210_143022.png

Enter screen name (or ENTER for auto, i=info, q=quit): i
📱 Device: Pixel 7 (Android 13)
📐 Resolution: 1080x2400px (physical) | 412x915dp (logical)
   Density: 420 DPI

Enter screen name (or ENTER for auto, i=info, q=quit): dashboard_main
📸 Capturing screenshot... ✅ Saved: screenshots/dashboard_main_20231210_143035.png

Enter screen name (or ENTER for auto, i=info, q=quit):
📸 Capturing screenshot... ✅ Saved: screenshots/screenshot_001_20231210_143040.png

Enter screen name (or ENTER for auto, i=info, q=quit): q
✅ Done! Captured 3 screenshots
```

### Single Screenshot Mode

Capture one screenshot and exit:

```bash
# With custom name
python android-screen-grabber.py --single login_screen

# With automatic naming
python android-screen-grabber.py --single auto
```

### Custom Output Directory

Save screenshots to a specific folder:

```bash
python android-screen-grabber.py --output my_app_screens
```

## Command-Line Options

```
usage: android-screen-grabber.py [-h] [--output OUTPUT] [--single SINGLE] [--name NAME]

optional arguments:
  -h, --help            Show help message and exit
  --output, -o OUTPUT   Output directory for screenshots (default: screenshots)
  --single, -s SINGLE   Capture a single screenshot and exit
  --name, -n NAME       Screen name to include in filename
```

## Output

Screenshots are saved as PNG files with the following naming convention:

- **Named screenshots**: `{screen_name}_{timestamp}.png`
  - Example: `login_screen_20231210_143022.png`

- **Auto-named screenshots**: `screenshot_{count}_{timestamp}.png`
  - Example: `screenshot_001_20231210_143022.png`

All screenshots include a timestamp in `YYYYMMDD_HHMMSS` format.

## Resolution Info for Design QA

The tool displays both physical and logical resolutions when you start the tool or press `i`:

```
📱 Device: Pixel 7 (Android 13)
📐 Resolution: 1080x2400px (physical) | 412x915dp (logical)
   Density: 420 DPI
```

**Why is this useful for designers?**

When doing UI/UX QA work and importing screenshots into design tools like Figma:

- **Physical resolution** (1080x2400px): The actual pixel dimensions of the screenshot PNG file captured from the device
- **Logical resolution** (412x915dp): The density-independent pixel size that designers work with in design tools

**Design workflow tip:**
1. Take screenshots using this tool (captured at physical resolution, e.g., 1080x2400px)
2. Import into Figma
3. Resize the screenshot to the **logical resolution** (e.g., 412x915) to match your design artboards
4. Now you can overlay screenshots with designs for pixel-perfect QA comparisons

This ensures your screenshots are scaled correctly to match design specifications, making side-by-side comparisons accurate regardless of the device's screen density.

## Troubleshooting

**"No Android device connected"**
- Make sure USB debugging is enabled
- Check that your device appears in `adb devices`
- Try unplugging and reconnecting the USB cable
- Authorize the computer on your phone if prompted

**"ADB not found"**
- Install Android Platform Tools (see Requirements section)
- Make sure `adb` is in your system PATH

**Permission errors**
- Your device may need to authorize the computer
- Check your phone for an authorization popup

## License

MIT License - feel free to use this tool however you'd like!

## Contributing

Issues and pull requests are welcome! This is a simple tool, but improvements are always appreciated.
