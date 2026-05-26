<<<<<<< HEAD
# 🤖 CNC Virtual Controller & Telegram Bot

A 2-axis CNC math equation plotter with Telegram bot control, image tracing, animated simulation, and C array export.

---

## 📁 Project Structure

```
project/
├── new.py              # Core Draw class — all parametric curves + image tracing
├── draw.py             # Older version of Draw class (superseded by new.py)
├── CNC_simulation.py   # Tkinter-based animated CNC canvas
├── cnc_web.py          # Streamlit web UI for the plotter
├── main.py             # Telegram bot (full-featured)
├── telbot.py           # Telegram bot (simple/early version)
├── create_c_array.py   # Exports path as C float arrays (.h header file)
├── create_bin.py       # Exports path as binary .bin file
└── README.md
```

---

## ⚙️ Installation

```bash
pip install numpy opencv-python matplotlib streamlit pyTelegramBotAPI
```

---

## 🚀 Usage

### 1. Desktop Simulation (Tkinter)
```bash
python new.py
```
Opens an animated CNC canvas drawing all curves one by one.

### 2. Web UI (Streamlit)
```bash
streamlit run cnc_web.py
```
Opens a browser UI to select curves, adjust parameters, and download C/CSV/NumPy outputs.

### 3. Telegram Bot
```bash
python main.py
```
Control the CNC via Telegram commands. Only whitelisted user IDs can operate it.

---

## ✏️ Supported Curves

| Command | Curve | Formula |
|---|---|---|
| `/circle` | Circle | x=r·cos(t), y=r·sin(t) |
| `/heart_curve` | Heart | x=16sin³(t), y=13cos(t)−5cos(2t)... |
| `/petal_rose` | Petal Rose | r=a·cos(5θ) |
| `/lissajous` | Lissajous (∞) | x=sin(t), y=sin(2t) |
| `/butterfly` | Butterfly | x=sin(t)·(eᶜᵒˢ⁽ᵗ⁾−2cos(4t)−sin⁵(t/12)) |
| `/spiral` | Archimedean Spiral | r=a·θ |
| `/cardioid` | Cardioid | r=a(1+cos θ) |
| `/astroid` | Astroid | x=a·cos³(t), y=a·sin³(t) |
| `/epitrochoid` | Epitrochoid | Spirograph flower |
| `/hypotrochoid` | Hypotrochoid | Inner spirograph |
| `/rhodonea` | Rhodonea Rose | r=a·cos(k·θ) |
| `/limacon` | Limaçon | r=a+b·cos(θ) |
| `/cycloid` | Cycloid | Rolling wheel path |
| `/deltoid` | Deltoid | 3-cusped hypocycloid |
| `/logarithmic_spiral` | Log Spiral | r=a·eᵇᶿ |

---

## 🖼️ Image Tracing (new.py)

Send any image to the bot or call `draw_image()` directly:

```python
from new import Draw
a = Draw(0, 0, 5)
a.draw_image("your_image.png")
```

The tracer: loads the image → applies Gaussian blur → threshold → finds contours → simplifies with Douglas-Peucker → plots as CNC toolpath.

---

## 📤 Export Formats

| Format | File | Use |
|---|---|---|
| C Header `.h` | `create_c_array.py` | STM32 / Arduino microcontrollers |
| Binary `.bin` | `create_bin.py` | Direct memory read on embedded systems |
| CSV | `cnc_web.py` | Spreadsheet / CAM software |
| NumPy `.npz` | `cnc_web.py` | Python data pipelines |

---

## 🤖 Telegram Bot Commands

```
/start or /help    Show the command manual
/circle 0 0 10     Draw circle at (0,0) with radius 10
/heart_curve 0 0 1
/spiral 0 0 15
... (all 15 curves supported)
```

Send a **photo** to auto-trace it into CNC paths.

---

## ⚠️ Known Issues & Suggestions

See the [Issues](#issues) section below.

---

## 📄 License

MIT License — Free to use, modify, and distribute.
=======
# CNC Controller & Simulator

A Python-based CNC path generator and simulator that integrates with Telegram for remote control. It uses NLP (Ollama) and mathematical parsing to convert natural language or equations into CNC toolpaths, which are then exported as C header files for AVR-based CNC machines.

## Features

- **Telegram Bot Integration:** Control your CNC machine via Telegram.
- **Natural Language Processing:** Use Ollama (Qwen2.5) to parse drawing requests into parametric equations.
- **Mathematical Parser:** Supports expressions like `y = sin(x)`, `y = x^2`, and complex parametric shapes.
- **Image Tracing:** Send a photo to the bot to automatically generate simplified CNC paths.
- **Virtual Simulator:** Visualize the generated paths in a Tkinter-based simulator before running them on hardware.
- **Consistent AVR Output:** Always exports the current path to `Custom.h` for easy consumption by AVR boards.
- **Chat History:** Maintains context for conversational interactions and guides users toward CNC commands.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Ollama:**
   Ensure Ollama is running locally with the `qwen2.5:0.5b` model (or update `OLLAMA_MODEL` in `main_auto.py`).
3. **Telegram Bot Token:**
   Update the `API` token in `main_auto.py` with your bot's token.
4. **Authorized Users:**
   Add your Telegram User ID to the `ALLOWED_USERS` list in `main_auto.py`.

## Usage

Run the main bot script:
```bash
python main_auto.py
```

### Commands
- `/start` or `/help`: Show available commands and instructions.
- `/demo`: Run a sequence of preset shapes.
- `/draw x|y|pts...`: Manually specify parametric equations.
- `/myid`: Get your Telegram User ID.

### Natural Language
You can also type naturally:
- "draw a heart"
- "y = sin(x)"
- "circle radius 15"

## File Structure

- `main_auto.py`: The entry point for the Telegram bot and NLP parsing.
- `new.py`: Contains the drawing logic and coordinates the simulator and exporter.
- `CNC_simulation.py`: The virtual simulator using Tkinter.
- `create_c_array.py`: Exports toolpaths to C header files (`Custom.h`).
- `Custom.h`: The output file intended for the AVR board.
- `chat_history.json`: Stores the last 10 messages for conversational context.

## Hardware Integration

The generated `Custom.h` file contains `path_x`, `path_y`, and `path_z` arrays along with `NUM_POINTS`. Include this file in your AVR project to drive the motors according to the generated coordinates.
>>>>>>> 82a874b (Refactor: Centralized AVR output to Custom.h, added chat history with CNC guidance, and cleaned up unused scripts/files.)
