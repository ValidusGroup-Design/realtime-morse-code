"""
Continuous Text-to-Morse Code Playback

This script converts text into Morse code and plays it in real-time using audio.
Designed for the NVIDIA Jetson Orin Nano Developer Board.

MIT License

Copyright (c) 2025 Fred Fisher, Validus Group Inc.
Website: https://www.validusgroup.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import torchaudio
import torch
import subprocess
import time

# Morse code dictionary
MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..",
    "9": "----.", "0": "-----", " ": "/"
}

SAMPLE_RATE = 44100  # Audio sample rate


def wpm_to_timing(wpm):
    """Convert WPM to Morse code timing parameters."""
    dot_duration = 1.2 / wpm
    return {
        "dot": dot_duration,
        "dash": dot_duration * 3,
        "symbol_space": dot_duration,
        "char_space": dot_duration * 3,
        "word_space": dot_duration * 7,
    }


def text_to_morse(text):
    """Convert text to Morse code."""
    return " ".join(MORSE_CODE.get(char, "") for char in text.upper())


def generate_tone(duration, freq=600):
    """Generate a sine wave tone for a given duration."""
    t = torch.linspace(0, duration, int(SAMPLE_RATE * duration), dtype=torch.float32)
    wave = 0.5 * torch.sin(2 * torch.pi * freq * t)  # Scaled to avoid clipping
    return wave


def generate_silence(duration):
    """Generate silence for a given duration."""
    return torch.zeros(int(SAMPLE_RATE * duration), dtype=torch.float32)


def generate_morse_audio(morse_code, timing):
    """Generate the audio waveform for a Morse code sequence."""
    waveform = []

    for char in morse_code:
        if char == ".":
            waveform.append(generate_tone(timing["dot"]))
        elif char == "-":
            waveform.append(generate_tone(timing["dash"]))
        elif char == " ":
            waveform.append(generate_silence(timing["symbol_space"]))
        elif char == "/":
            waveform.append(generate_silence(timing["word_space"]))
        waveform.append(generate_silence(timing["symbol_space"]))  # Space between symbols

    return torch.cat(waveform)


def play_morse_realtime(text_stream, wpm=20):
    """Continuously read text, convert to Morse code, and play it in real-time."""
    timing = wpm_to_timing(wpm)

    # Stream playback setup
    process = subprocess.Popen(
        ["aplay", "-D", "plughw:2,0", "-f", "FLOAT_LE", "-r", str(SAMPLE_RATE)],
        stdin=subprocess.PIPE,
    )

    try:
        for text_chunk in text_stream:
            text_chunk = text_chunk.strip()  # Clean input text
            if not text_chunk:
                continue  # Skip empty lines

            morse_code = text_to_morse(text_chunk)
            print(f"Text: {text_chunk}")
            print(f"Morse: {morse_code}")

            # Generate audio waveform for the Morse code
            waveform = generate_morse_audio(morse_code, timing)

            # Stream waveform to audio playback
            process.stdin.write(waveform.numpy().astype("float32").tobytes())
            process.stdin.flush()

    except KeyboardInterrupt:
        print("\nStopping Morse code playback.")
    finally:
        process.stdin.close()
        process.wait()


# Simulated text stream (e.g., reading a book line by line)
def simulated_text_stream():
    lines = [
        "This is a test of continuous Morse code playback.",
        "Morse code allows text communication through sound.",
        "The quick brown fox jumps over the lazy dog.",
        "73 DE WF9Q",
    ]
    for line in lines:
        yield line
        time.sleep(3)  # Simulate delay between lines


# Entry point
if __name__ == "__main__":
    message = "DE WF9Q"
    words_per_minute = 20  # Default WPM

    # Example: Play simulated text stream
    play_morse_realtime(simulated_text_stream(), wpm=words_per_minute)
