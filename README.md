# 🤖 Smart CNC Controller & Path Generator

An intelligent 2-axis CNC path generation system that combines **Natural Language Processing (Ollama)**, **Mathematical Expression Parsing**, and **Computer Vision** to create precise toolpaths. Designed for seamless integration with Telegram and AVR-based CNC hardware.

---

## 🌟 Key Features

### 1. 🧠 Intelligent NLP Parser (Ollama)
The system uses the `qwen2.5:0.5b` model via Ollama to understand human requests. You can type things like:
- *"Draw a heart shape for my girlfriend"*
- *"Make a circle with a radius of 15"*
- *"Plot a butterfly curve"*
The bot automatically converts these into the correct parametric equations.

### 2. 📈 Advanced Math Engine
Beyond NLP, the system features a robust regex-based math parser that handles:
- **Direct Equations:** `y = sin(x)`, `x = y^2 + 5`, `y = 2x^2 + 3x`
- **Implicit Multiplication:** `2x` becomes `2*x`, `(x+1)(x-1)` works automatically.
- **Trig & Math Functions:** Supports `sin`, `cos`, `tan`, `sqrt`, `exp`, `log`, `abs`, and `pi`.

### 3. 🖼️ Image-to-Path (Cartoon Trace)
Send any photo to the Telegram bot, and it will:
1. Apply **Gaussian Blur** to remove noise.
2. Use **Adaptive Thresholding** to find edges.
3. Simplify contours using the **Douglas-Peucker algorithm** for a "cartoon" effect.
4. Convert the result into optimized CNC toolpaths.

### 4. 📺 Virtual CNC Simulator
Visualize paths in real-time with the built-in Tkinter-based simulator (`CNC_simulation.py`). See exactly what the machine will do before you send it to the hardware.

### 5. 🔌 AVR-Ready Output (`Custom.h`)
All paths—whether from an image, an equation, or a preset—are exported to a single, consistent file: `Custom.h`. 
- **Consistency:** No more searching for different filenames; the AVR code just includes one file.
- **Data:** Exports `path_x[]`, `path_y[]`, and `path_z[]` as float arrays along with a `NUM_POINTS` constant.

---

## 📂 Project Architecture

| File | Description |
| :--- | :--- |
| `main_auto.py` | **Entry Point.** Telegram bot logic, NLP pipeline, and Ollama integration. |
| `new.py` | **Core Engine.** Contains the `Draw` class and logic for curve generation and image tracing. |
| `CNC_simulation.py`| **Simulator.** High-performance Tkinter canvas for path visualization. |
| `create_c_array.py` | **Exporter.** Converts Python numpy arrays into C-style header files. |
| `chat_history.json` | **Memory.** Stores the last 10 conversational messages to provide context-aware help. |

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **Ollama:** [Download Ollama](https://ollama.com/) and run `ollama run qwen2.5:0.5b`.

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
Open `main_auto.py` and update:
- `API`: Your Telegram Bot Token.
- `ALLOWED_USERS`: Your Telegram User ID (use `/myid` to find it).

### 4. Run
```bash
python main_auto.py
```

---

## 🤖 Bot Commands

- `/start` or `/help` - Show the interactive guide.
- `/demo` - Run a sequence of 5 beautiful preset shapes.
- `/draw x|y|pts` - Manual mode for parametric experts.
- `/myid` - Quick way to get your Telegram ID for whitelist setup.

---

## 🛠️ Hardware Integration (AVR/Arduino)

Simply include the generated header in your C++ project:

```cpp
#include "Custom.h"

void executePath() {
    for(int i = 0; i < NUM_POINTS; i++) {
        moveTo(path_x[i], path_y[i]);
    }
}
```

---

## 📄 License
No MIT License. Feel free to use, modify, and distribute.
