
# Continuous Text-to-Morse Code Playback

This repository provides a Python application for converting text into Morse code and playing it in real-time. Designed to run on the NVIDIA Jetson Orin Nano Developer Board, the application streams audio directly to a connected speaker.

## Features
- **Real-Time Text-to-Morse Conversion**: Converts incoming text into Morse code and streams the audio live.
- **Customizable Speed**: Supports configurable playback speeds in Words Per Minute (WPM).
- **Simulated or Live Input**: Works with simulated text streams, file input, or other live data sources.

---

## Dependencies

To run this application on your **Jetson Orin Nano Developer Board**, ensure the following dependencies are installed:

### Python Libraries
    pip3 install torchaudio torch

### System Tools
- `aplay`: A command-line audio playback tool, usually available with the `alsa-utils` package.

Install with:
    sudo apt-get update
    sudo apt-get install alsa-utils

### Additional Notes
1. **Audio Output Configuration**:
   - Ensure your USB or HDMI audio device is detected. Use the following command to list audio devices:
         aplay -l
   - Replace `plughw:2,0` in the code with the appropriate device from your system.

2. **Development Environment**:
   - Python 3.6+ is required. Ensure you have access to the `pip` package manager.

---

## How It Works

### Morse Code Timing
The application adheres to standard Morse code timing:
- **Dot Duration**: \( 1.2 / 	ext{WPM} \)
- **Dash Duration**: \( 3 	imes 	ext{Dot} \)
- **Space Between Symbols**: \( 1 	imes 	ext{Dot} \)
- **Space Between Characters**: \( 3 	imes 	ext{Dot} \)
- **Space Between Words**: \( 7 	imes 	ext{Dot} \)

### Code Overview

1. **Text-to-Morse Conversion**:
   - Converts incoming text into Morse code using a dictionary lookup.

2. **Waveform Generation**:
   - Uses `torch` to generate sine wave tones for dots and dashes, and silence for spaces.

3. **Real-Time Playback**:
   - Streams generated audio waveforms to `aplay` for immediate playback.

---

## Usage Instructions

### Running the Application
1. Clone the repository:
       git clone https://github.com/ValidusGroup-Design/realtime-morse-code.git
       cd realtime-morse-code

2. Run the application:
       python3 continuous_morse_playback.py

3. To use custom input (e.g., from a file), modify the `text_stream` function:
       def file_text_stream(filepath):
           with open(filepath, "r") as file:
               for line in file:
                   yield line
                   time.sleep(0.5)  # Delay between lines

4. Replace the simulated stream with:
       play_morse_realtime(file_text_stream("book.txt"), wpm=20)

---

## Learning Highlights

### Real-Time Audio Playback
This application demonstrates how to:
1. Generate audio waveforms programmatically using `torch` and `torchaudio`.
2. Stream audio directly to a playback tool (`aplay`) in real time.

### Morse Code Encoding
Key aspects include:
- Adhering to international Morse code timing standards.
- Efficiently managing dot, dash, and spacing durations.

### Modular Design
The application is modular, making it easy to:
- Integrate with other input sources (e.g., network streams).
- Extend functionality (e.g., add GUI for input).

---

## Example Output

Running the application with the text `"DE WF9Q"` at 20 WPM:

- **Input**: `DE WF9Q`
- **Generated Morse**: `-.. . / .-- ..-. ----. --.-`

### Real-Time Audio Output
The generated Morse code audio will be streamed and played via your system's audio device.

---

## Contributing

Feel free to submit issues or pull requests to improve this project. Contributions are always welcome!

---

## License

This project is licensed under the MIT License. See `LICENSE` for more information.
```
