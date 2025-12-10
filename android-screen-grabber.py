#!/usr/bin/env python3
"""
Android Screenshot Capture Tool
Connects to an Android device via ADB and captures screenshots on keypress
"""

import subprocess
import os
import sys
import math
from datetime import datetime
from pathlib import Path

class AndroidScreenshotTool:
    def __init__(self, output_dir="screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.screenshot_count = 0
        
    def check_adb_connection(self):
        """Check if ADB is installed and a device is connected"""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            devices = [line for line in result.stdout.split('\n')[1:] 
                      if line.strip() and 'device' in line]
            
            if not devices:
                print("❌ No Android device connected!")
                print("\nMake sure:")
                print("  1. Your phone is connected via USB")
                print("  2. USB debugging is enabled")
                print("  3. You've authorized the computer on your phone")
                return False
            
            print(f"✅ Connected to device: {devices[0].split()[0]}")
            return True
            
        except FileNotFoundError:
            print("❌ ADB not found!")
            print("\nInstall Android Platform Tools:")
            print("  brew install android-platform-tools")
            return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running ADB: {e}")
            return False
    
    def get_device_info(self):
        """Get device model and Android version"""
        try:
            model = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.model'],
                                 capture_output=True, text=True, check=True)
            version = subprocess.run(['adb', 'shell', 'getprop', 'ro.build.version.release'],
                                   capture_output=True, text=True, check=True)
            return model.stdout.strip(), version.stdout.strip()
        except:
            return "Unknown", "Unknown"

    def get_display_info(self):
        """Get display resolution info - both physical and logical (dp)"""
        try:
            # Get physical resolution
            size_result = subprocess.run(['adb', 'shell', 'wm', 'size'],
                                       capture_output=True, text=True, check=True)
            size_line = size_result.stdout.strip()
            # Parse "Physical size: 1080x2400"
            if 'Physical size:' in size_line:
                resolution = size_line.split('Physical size:')[1].strip()
                width, height = map(int, resolution.split('x'))
            else:
                return None

            # Get density
            density_result = subprocess.run(['adb', 'shell', 'wm', 'density'],
                                          capture_output=True, text=True, check=True)
            density_line = density_result.stdout.strip()
            # Parse "Physical density: 420"
            if 'Physical density:' in density_line:
                density = int(density_line.split('Physical density:')[1].strip())
            else:
                return None

            # Calculate logical resolution (dp)
            # Formula: physical_pixels / (density / 160) = dp
            # Use ceil() to match Android's viewport calculation
            dp_width = math.ceil(width / (density / 160))
            dp_height = math.ceil(height / (density / 160))

            return {
                'physical': (width, height),
                'logical': (dp_width, dp_height),
                'density': density
            }
        except:
            return None

    def display_device_info(self):
        """Display device and screen information (reusable for startup and 'i' command)"""
        model, version = self.get_device_info()
        print(f"📱 Device: {model} (Android {version})")

        display_info = self.get_display_info()
        if display_info:
            physical = display_info['physical']
            logical = display_info['logical']
            density = display_info['density']
            print(f"📐 Resolution: {physical[0]}x{physical[1]}px (physical) | {logical[0]}x{logical[1]}dp (logical)")
            print(f"   Density: {density} DPI")
        else:
            print("📐 Resolution: Unable to detect")

    def capture_screenshot(self, screen_name=None):
        """Capture a screenshot from the connected device"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screenshot_count += 1
        
        if screen_name:
            # Clean the screen name (remove special characters, replace spaces with underscores)
            clean_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in screen_name)
            filename = f"{clean_name}_{timestamp}.png"
        else:
            filename = f"screenshot_{self.screenshot_count:03d}_{timestamp}.png"
        
        filepath = self.output_dir / filename
        device_path = "/sdcard/screenshot_temp.png"
        
        try:
            # Capture screenshot on device
            print(f"📸 Capturing screenshot...", end=" ", flush=True)
            subprocess.run(['adb', 'shell', 'screencap', '-p', device_path],
                         check=True, capture_output=True)
            
            # Pull screenshot to Mac
            subprocess.run(['adb', 'pull', device_path, str(filepath)],
                         check=True, capture_output=True)
            
            # Clean up device
            subprocess.run(['adb', 'shell', 'rm', device_path],
                         check=True, capture_output=True)
            
            print(f"✅ Saved: {filepath}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {e}")
            return False
    
    def run_interactive(self):
        """Run interactive screenshot capture mode"""
        print("\n" + "="*60)
        print("  Android Screenshot Capture Tool")
        print("="*60)
        
        # Check connection
        if not self.check_adb_connection():
            return
        
        # Show device info
        self.display_device_info()
        print(f"💾 Saving to: {self.output_dir.absolute()}\n")
        
        print("Instructions:")
        print("  • Navigate your app on the phone normally")
        print("  • Type a screen name (e.g., 'login', 'dashboard') and press ENTER to capture")
        print("  • Or just press ENTER without typing for auto-naming")
        print("  • Type 'i' then ENTER to show device info")
        print("  • Type 'q' then ENTER to quit")
        print("\n" + "="*60)
        print("Ready! Start capturing screenshots...\n")
        
        try:
            while True:
                user_input = input("Enter screen name (or ENTER for auto, i=info, q=quit): ").strip()

                if user_input.lower() == 'q':
                    print(f"\n✅ Done! Captured {self.screenshot_count} screenshots")
                    print(f"📁 Location: {self.output_dir.absolute()}")
                    break
                elif user_input.lower() == 'i':
                    self.display_device_info()
                elif user_input == '':
                    # Empty input = auto-naming
                    self.capture_screenshot()
                else:
                    # Any other input is treated as screen name
                    self.capture_screenshot(screen_name=user_input)

        except KeyboardInterrupt:
            print(f"\n\n✅ Done! Captured {self.screenshot_count} screenshots")
            print(f"📁 Location: {self.output_dir.absolute()}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Capture screenshots from Android device via ADB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (prompts for screen names)
  python android_screenshot_tool.py
  
  # Save to custom folder
  python android_screenshot_tool.py --output my_app_screens
  
  # Capture single screenshot with automatic naming
  python android_screenshot_tool.py --single login
  
  # Capture single screenshot with specific name
  python android_screenshot_tool.py --single --name "login_screen"
        """
    )
    
    parser.add_argument('--output', '-o', 
                       default='screenshots',
                       help='Output directory for screenshots (default: screenshots)')
    
    parser.add_argument('--single', '-s',
                       help='Capture a single screenshot and exit')
    
    parser.add_argument('--name', '-n',
                       help='Screen name to include in filename (use with --single or interactive mode)')
    
    args = parser.parse_args()
    
    tool = AndroidScreenshotTool(output_dir=args.output)
    
    if args.single:
        # Single screenshot mode
        if not tool.check_adb_connection():
            sys.exit(1)
        
        # Use provided name or the --single argument as the name
        screen_name = args.name if args.name else args.single.replace('.png', '')
        tool.capture_screenshot(screen_name=screen_name)
    else:
        # Interactive mode
        tool.run_interactive()

if __name__ == "__main__":
    main()
