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
