import telebot
from telebot import apihelper
import new
import numpy as np
import re
import ollama
import json

# --- CONFIGURATION ---
API = "8690254124:AAG4hFS89yHbsEcNT3Wsfoa6io1jlVUAGgI"
bot = telebot.TeleBot(token=API)
apihelper.CONNECT_TIMEOUT = 30
apihelper.READ_TIMEOUT = None  # infinite — drawing can take a while
OLLAMA_MODEL = "qwen2.5:0.5b"
ALLOWED_USERS = [8058658801,1667679794]

# ── PRESET SHAPES (from mathplot.py) ──────────────────────────────────────────
# (x_expr, y_expr, t_start, t_end, description)
PRESETS = {
    "circle":        ("r*cos(t)",            "r*sin(t)",                              0, 2*np.pi,       "Circle"),
    "heart":         ("16*sin(t)**3",         "13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)", 0, 2*np.pi, "Heart Curve"),
    "heart_curve":   ("16*sin(t)**3",         "13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)", 0, 2*np.pi, "Heart Curve"),
    "rose":          ("r*cos(5*t)*cos(t)",   "r*cos(5*t)*sin(t)",                      0, np.pi,       "Petal Rose"),
    "petal_rose":    ("r*cos(5*t)*cos(t)",   "r*cos(5*t)*sin(t)",                      0, np.pi,       "Petal Rose"),
    "lissajous":     ("r*sin(t)",            "r*sin(2*t)",                             0, 2*np.pi,     "Lissajous Figure-8"),
    "butterfly":     ("r*sin(t)*(exp(cos(t))-2*cos(4*t)-sin(t/12)**5)",
                                             "r*cos(t)*(exp(cos(t))-2*cos(4*t)-sin(t/12)**5)", 0, 10*np.pi, "Butterfly Curve"),
    "spiral":        ("(r/10)*t*cos(t)",     "(r/10)*t*sin(t)",                        0, 8*np.pi,     "Archimedean Spiral"),
    "cardioid":      ("r*(1+cos(t))*cos(t)", "r*(1+cos(t))*sin(t)",                    0, 2*np.pi,     "Cardioid"),
    "astroid":       ("r*cos(t)**3",         "r*sin(t)**3",                            0, 2*np.pi,     "Astroid"),
    "epitrochoid":   ("(r+r/3)*cos(t)-(r/2)*cos(4*t)",
                                             "(r+r/3)*sin(t)-(r/2)*sin(4*t)",          0, 2*np.pi,     "Epitrochoid"),
    "hypotrochoid":  ("(r-r/4)*cos(t)+(r/2)*cos(3*t)",
                                             "(r-r/4)*sin(t)-(r/2)*sin(3*t)",          0, 2*np.pi,     "Hypotrochoid"),
    "rhodonea":      ("r*cos(7*t)*cos(t)",   "r*cos(7*t)*sin(t)",                      0, np.pi,       "Rhodonea 7-petal"),
    "limacon":       ("r*(1+0.5*cos(t))*cos(t)", "r*(1+0.5*cos(t))*sin(t)",            0, 2*np.pi,     "Limacon"),
    "cycloid":       ("r*(t-sin(t))",        "r*(1-cos(t))",                           0, 4*np.pi,     "Cycloid"),
    "deltoid":       ("r*(2*cos(t)+cos(2*t))", "r*(2*sin(t)-sin(2*t))",                0, 2*np.pi,     "Deltoid"),
    "lemniscate":    ("r*cos(t)/(1+sin(t)**2)", "r*sin(t)*cos(t)/(1+sin(t)**2)",       0, 2*np.pi,     "Lemniscate"),
    "sine":          ("t",                    "r*sin(3*t)",                            -10, 10,         "Sine Wave"),
    "parabola":      ("t",                    "t**2",                                  -4, 4,           "Parabola"),
    "logspiral":     ("(r/20)*exp(0.2*t)*cos(t)", "(r/20)*exp(0.2*t)*sin(t)",           0, 4*np.pi,    "Logarithmic Spiral"),
    "logarithmic_spiral": ("(r/20)*exp(0.2*t)*cos(t)", "(r/20)*exp(0.2*t)*sin(t)",     0, 4*np.pi,    "Logarithmic Spiral"),
    "infinity":      ("r*sin(t)",             "r*sin(t)*cos(t)/(1+sin(t)**2)",          0, 2*np.pi,    "Infinity Symbol"),
    "star":          ("r*cos(t)*(1+0.3*cos(5*t))", "r*sin(t)*(1+0.3*cos(5*t))",        0, 2*np.pi,    "5-point Star"),
    "rainbow":       ("(r/3)*t*cos(t)",      "(r/3)*t*sin(t)",                         0, 12*np.pi,   "Rainbow Spiral"),
}

# NLP keyword → preset key mapping
_NLP_KEYWORDS = {
    "heart": "heart", "love": "heart",
    "circle": "circle", "round": "circle",
    "rose": "rose", "flower": "rose", "petal": "rose",
    "lissajous": "lissajous", "figure eight": "lissajous", "figure-eight": "lissajous", "infinity": "infinity",
    "butterfly": "butterfly",
    "spiral": "spiral", "archimedean": "spiral",
    "cardioid": "cardioid",
    "astroid": "astroid", "star polygon": "astroid",
    "epitrochoid": "epitrochoid",
    "hypotrochoid": "hypotrochoid",
    "rhodonea": "rhodonea",
    "limacon": "limacon",
    "cycloid": "cycloid",
    "deltoid": "deltoid",
    "lemniscate": "lemniscate", "bernoulli": "lemniscate",
    "sine": "sine", "sin wave": "sine", "sine wave": "sine",
    "parabola": "parabola",
    "log spiral": "logspiral", "logarithmic spiral": "logspiral",
    "star": "star",
    "rainbow": "rainbow",
}

# ── SAFE MATH EVAL ─────────────────────────────────────────────────────────────
_SAFE_MATH = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "sqrt": np.sqrt, "exp": np.exp, "log": np.log, "log10": np.log10,
    "abs": np.abs, "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
    "pi": np.pi, "e": np.e,
}

# Ignore numpy errors (like log(-1)) to prevent __import__ errors in restricted eval
np.seterr(all='ignore')

def _eval_expr(expr, t, r=10.0):
    safe = {"t": t, "r": r, "np": np, **_SAFE_MATH}
    val = eval(expr, {"__builtins__": {}}, safe)
    if isinstance(val, (int, float)):
        val = np.full_like(t, float(val))
    return val

import threading, queue
_draw_queue = queue.Queue()

def _render(x_expr, y_expr, t_start, t_end, n_points, r, title, chat_id=None):
    _draw_queue.put((x_expr, y_expr, t_start, t_end, n_points, r, title, chat_id))

# ── NLP PIPELINE ───────────────────────────────────────────────────────────────
_SYSTEM_DRAW_PROMPT = """\
You are a CNC math parser. Convert user input to parametric equations with parameter t.

RULES:
1. Return ONLY valid JSON (no markdown, no explanation):
   {"x_expr": "...", "y_expr": "...", "t_start": 0, "t_end": 6.28, "n_points": 300, "r": 10}
2. Python syntax: t**2 (not t^2), functions: sin(t), cos(t), sqrt(t), exp(t), pi, abs(t)
3. Examples:
   - "y = x^2"         -> {"x_expr": "t", "y_expr": "t**2", "t_start": -4, "t_end": 4, "n_points": 300, "r": 10}
   - "circle radius 5" -> {"x_expr": "5*cos(t)", "y_expr": "5*sin(t)", "t_start": 0, "t_end": 6.28, "n_points": 300, "r": 5}
   - "draw a heart"    -> {"x_expr": "16*sin(t)**3", "y_expr": "13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)", "t_start": 0, "t_end": 6.28, "n_points": 300, "r": 10}
   - "parabola"        -> {"x_expr": "t", "y_expr": "t**2", "t_start": -4, "t_end": 4, "n_points": 300, "r": 10}
4. If NOT a draw request, reply exactly: NOT_DRAW
5. NO code blocks, NO explanations, ONLY the JSON or NOT_DRAW.
"""

def _ollama_parse(text):
    try:
        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_DRAW_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        raw = resp["message"]["content"]
        if "NOT_DRAW" in raw:
            return None
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", raw.strip())
        cleaned = re.sub(r"\s*```$", "", cleaned)
        data = json.loads(cleaned)
        if data.get("x_expr", "").strip() and data.get("y_expr", "").strip():
            return data
    except Exception:
        pass
    return None

def _regex_parse(text):
    """Parse equations like: y = sin(x), y = x^2 + c, y = cos(x) + x."""
    raw = text.strip()
    # Support both "y = ..." and just the expression if it contains x
    m = re.match(r"^\s*([xy])\s*=\s*(.+?)\s*$", raw, re.IGNORECASE)
    if m:
        dep = m.group(1).lower()
        expr = m.group(2).strip()
    else:
        # Try to infer: if it contains 'x' it's likely 'y = f(x)'
        if 'x' in raw.lower() and '=' not in raw:
            dep = 'y'
            expr = raw
        elif 'y' in raw.lower() and '=' not in raw:
            dep = 'x'
            expr = raw
        else:
            return None

    # 1. Basic cleanup
    expr = re.sub(r"\^", "**", expr)
    
    # 2. Add parentheses to trig/math functions if missing: sin x -> sin(x), sinx -> sin(x)
    for func in ["sin", "cos", "tan", "sqrt", "exp", "log", "abs", "arcsin", "arccos", "arctan"]:
        # sin x -> sin(x)
        expr = re.sub(rf"\b{func}\s+([a-zA-Z0-9.t]+)", rf"{func}(\1)", expr)
        # sinx -> sin(x) (only if followed by x, y, or t)
        expr = re.sub(rf"\b{func}([xyt])\b", rf"{func}(\1)", expr)

    # 3. Implicit multiplication: 2x -> 2*x, (a)(b) -> (a)*(b), Digit( -> Digit*(, )Letter -> )*Letter
    expr = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expr) 
    expr = re.sub(r"(\))(\()", r"\1*\2", expr)
    expr = re.sub(r"(\d)(\()", r"\1*\2", expr)
    expr = re.sub(r"(\))([a-zA-Z])", r"\1*\2", expr)

    # 4. Replace variable with 't'
    if dep == "y":
        expr = re.sub(r"\bx\b", "t", expr)
    else:
        expr = re.sub(r"\by\b", "t", expr)

    # Replace unknown single-letter constants with 1 (excluding 't', 'r', 'e')
    expr = re.sub(r"\b(?![tre])([a-z])\b", "1", expr)
    
    # Range detection
    is_trig = bool(re.search(r"\b(sin|cos|tan)\b", expr))
    is_log_sqrt = bool(re.search(r"\b(log|sqrt)\b", expr))
    
    if is_trig:
        t0, t1 = (-2*np.pi, 2*np.pi)
    elif is_log_sqrt:
        t0, t1 = (0.1, 10)
    else:
        t0, t1 = (-4, 4)
    
    # Validate by test eval
    try:
        _eval_expr(expr, np.linspace(t0, t1, 5))
    except Exception:
        return None
        
    if dep == "y":
        return {"x_expr": "t", "y_expr": expr, "t_start": t0, "t_end": t1, "n_points": 300, "r": 10}
    else:
        return {"x_expr": expr, "y_expr": "t", "t_start": t0, "t_end": t1, "n_points": 300, "r": 10}

def _preset_lookup(text):
    """Check if text matches a preset name or NLP keyword."""
    key = text.strip().lower().replace(" ", "_")
    if key in PRESETS:
        x, y, t0, t1, desc = PRESETS[key]
        return {"x_expr": x, "y_expr": y, "t_start": t0, "t_end": t1, "n_points": 300, "r": 10, "name": desc}
    # NLP keyword scan
    tl = text.strip().lower()
    for kw, preset_key in _NLP_KEYWORDS.items():
        if kw in tl:
            x, y, t0, t1, desc = PRESETS[preset_key]
            return {"x_expr": x, "y_expr": y, "t_start": t0, "t_end": t1, "n_points": 300, "r": 10, "name": desc}
    return None

def try_nlp(text):
    """Full NLP pipeline: preset → regex → Ollama."""
    result = _preset_lookup(text)
    if result:
        return result
    result = _regex_parse(text)
    if result:
        return result
    return _ollama_parse(text)

# ── OLLAMA FREE TEXT ───────────────────────────────────────────────────────────
HISTORY_FILE = "chat_history.json"

def _load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

_SYSTEM_CHAT_PROMPT = """\
You are a CNC Machine Controller Assistant.
Your primary goal is to help users draw shapes and equations.

If the user tries to chat casually, politely discourage it and suggest they use CNC commands.
Examples of suggestions:
- "I can draw a circle, heart, or butterfly! Just ask."
- "Try typing an equation like y = sin(x) or x^2 + y^2 = 25."
- "Use /help to see all available shapes and commands."

Keep responses brief and always guide the user back to CNC operations.
"""

def ollama_respond(text):
    history = _load_history()
    
    messages = [{"role": "system", "content": _SYSTEM_CHAT_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": text})
    
    try:
        resp = ollama.chat(model=OLLAMA_MODEL, messages=messages)
        answer = resp["message"]["content"]
        
        # Update history (keep last 10 messages, 5 pairs)
        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": answer})
        _save_history(history[-10:])
        
        return answer
    except Exception as e:
        return f"Sorry, I'm having trouble connecting to my brain. Error: {e}"

# ── SECURITY ───────────────────────────────────────────────────────────────────
def is_authorized(message):
    uid = message.from_user.id
    if uid not in ALLOWED_USERS:
        print(f"[UNAUTHORIZED] ID: {uid}  Name: {message.from_user.full_name}")
        bot.reply_to(message, f"Access denied. Send your ID to the admin: {uid}")
        return False
    return True

# ── HANDLERS ───────────────────────────────────────────────────────────────────
@bot.message_handler(commands=['myid'])
def handle_myid(message):
    uid = message.from_user.id
    name = message.from_user.full_name
    print(f"[ID REQUEST] {name}: {uid}")
    bot.reply_to(message, f"Your Telegram ID: {uid}\nSend this to the admin to get access.")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message):
        bot.reply_to(message, "Access Denied.")
        return
    shapes = " | ".join(f"/{k}" for k in PRESETS)
    manual = (
        f"CNC Controller v4.0 — Welcome, {message.from_user.first_name}!\n\n"
        "Just type naturally — the parser is now much smarter:\n"
        "  y = sinx          (No parentheses needed)\n"
        "  y = 2x^2 + 3x     (Implicit multiplication works)\n"
        "  y = (x+1)(x-1)    (Complex groups work)\n"
        "  x^3 - 2x          (Auto-detects y=...)\n"
        "  x = sin(y)        (Plots on X axis)\n"
        "  y = logx          (Auto-ranges for log/sqrt)\n\n"
        "Commands:\n"
        "  /demo             - Run ALL shapes in sequence\n"
        "  /help             - Show this manual\n"
        "  /draw x|y|pts...  - Manual parametric mode\n\n"
        "Preset shapes (type the name or use /command):\n"
        f"  {shapes}\n\n"
        "Image mode: send any photo to auto-trace it as CNC paths."
    )
    bot.reply_to(message, manual)

@bot.message_handler(commands=['draw'])
def handle_free_draw(message):
    if not is_authorized(message): return
    parts_str = message.text.replace('/draw', '', 1).strip()
    parts = [p.strip() for p in parts_str.split('|')]
    if len(parts) < 2:
        bot.reply_to(message, "Usage: /draw x_expr | y_expr | [points=300] | [t_start=0] | [t_end=2*pi]")
        return
    x_expr, y_expr = parts[0], parts[1]
    n_points = int(parts[2]) if len(parts) > 2 and parts[2] else 300
    _safe = {"__builtins__": {}, "pi": np.pi, "e": np.e}
    t_start = eval(parts[3], _safe) if len(parts) > 3 and parts[3] else 0
    t_end   = eval(parts[4], _safe) if len(parts) > 4 and parts[4] else 2*np.pi
    try:
        _render(x_expr, y_expr, t_start, t_end, n_points, 10, f"Custom: {x_expr}", message.chat.id)
        bot.send_message(message.chat.id, f"Drew: x={x_expr}, y={y_expr}")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

ALL_SHAPES = list(PRESETS.keys())

@bot.message_handler(commands=ALL_SHAPES)
def handle_preset_command(message):
    if not is_authorized(message): return
    cmd = message.text.split()[0].replace('/', '').lower()
    if cmd not in PRESETS:
        bot.reply_to(message, f"Unknown shape: {cmd}")
        return
    # Optional: /heart [r=10]  — no X Y required
    parts = message.text.split()
    r = float(parts[1]) if len(parts) >= 2 else 10.0
    x_expr, y_expr, t0, t1, desc = PRESETS[cmd]
    bot.send_message(message.chat.id, f"Simulating {desc}...")
    try:
        _render(x_expr, y_expr, t0, t1, 300, r, desc, message.chat.id)
        bot.send_message(message.chat.id, f"{desc} complete.")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not is_authorized(message): return
    bot.reply_to(message, "Image received! Converting to CNC paths...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("input_image.jpg", 'wb') as f:
            f.write(downloaded_file)
        worker = new.Draw(0, 0, 15)
        worker.draw_cartoon("input_image.jpg")
        bot.send_message(message.chat.id, "Image trace complete!")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if not is_authorized(message): return
    user_text = message.text.strip()
    if user_text.startswith('/'):
        bot.reply_to(message, "Unknown command. Use /help.")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    data = try_nlp(user_text)

    if data:
        try:
            _render(
                data["x_expr"], data["y_expr"],
                data.get("t_start", 0), data.get("t_end", 2*np.pi),
                data.get("n_points", 300), data.get("r", 10),
                data.get("name", "Custom"),
                message.chat.id
            )
            bot.send_message(message.chat.id, f"Drew: {data.get('name', data['x_expr'])}")
            return
        except Exception as e:
            bot.reply_to(message, f"Draw error: {e}")
            return

    # Not a draw request — answer with Ollama
    answer = ollama_respond(user_text)
    bot.reply_to(message, answer)
@bot.message_handler(commands=['demo'])
def handle_demo(message):
    if not is_authorized(message): return
    demo_shapes = ["circle", "heart", "butterfly", "spiral", "rose"]
    bot.reply_to(message, f"Starting demo of 5 shapes: {', '.join(demo_shapes)}...")
    for key in demo_shapes:
        if key in PRESETS:
            x, y, t0, t1, desc = PRESETS[key]
            _draw_queue.put((x, y, t0, t1, 300, 10.0, desc, message.chat.id))
    bot.send_message(message.chat.id, "Shapes queued! They will draw one by one.")

bot.set_my_commands([
    telebot.types.BotCommand("myid",              "Get your Telegram ID (no auth needed)"),
    telebot.types.BotCommand("start",             "Show help & all commands"),
    telebot.types.BotCommand("help",              "Show help & all commands"),
    telebot.types.BotCommand("demo",              "Run 5 preset shapes as a demo"),
    telebot.types.BotCommand("draw",              "Draw custom equation: /draw x|y|[pts]|[t0]|[t1]"),
    telebot.types.BotCommand("heart",             "Heart curve"),
    telebot.types.BotCommand("circle",            "Circle — /circle [radius]"),
    telebot.types.BotCommand("butterfly",         "Butterfly curve"),
    telebot.types.BotCommand("spiral",            "Archimedean spiral"),
    telebot.types.BotCommand("rose",              "5-petal rose"),
    telebot.types.BotCommand("cardioid",          "Cardioid"),
    telebot.types.BotCommand("lissajous",         "Lissajous figure-8"),
    telebot.types.BotCommand("astroid",           "Astroid"),
    telebot.types.BotCommand("star",              "5-point star"),
    telebot.types.BotCommand("infinity",          "Infinity symbol"),
    telebot.types.BotCommand("parabola",          "Parabola y=x²"),
    telebot.types.BotCommand("sine",              "Sine wave"),
    telebot.types.BotCommand("lemniscate",        "Lemniscate of Bernoulli"),
    telebot.types.BotCommand("cycloid",           "Cycloid"),
    telebot.types.BotCommand("deltoid",           "Deltoid"),
    telebot.types.BotCommand("epitrochoid",       "Epitrochoid"),
    telebot.types.BotCommand("hypotrochoid",      "Hypotrochoid"),
    telebot.types.BotCommand("limacon",           "Limaçon"),
    telebot.types.BotCommand("rhodonea",          "Rhodonea 7-petal"),
    telebot.types.BotCommand("logspiral",         "Logarithmic spiral"),
    telebot.types.BotCommand("rainbow",           "Rainbow spiral"),
])
threading.Thread(
    target=lambda: bot.polling(none_stop=True, timeout=60, long_polling_timeout=60),
    daemon=True
).start()

# Main thread owns Tkinter — drain draw queue forever
while True:
    try:
        x_expr, y_expr, t_start, t_end, n_points, r, title, chat_id = _draw_queue.get(timeout=1)
        try:
            t = np.linspace(t_start, t_end, n_points)
            xc = _eval_expr(x_expr, t, r)
            yc = _eval_expr(y_expr, t, r)
            new.solution(xc, yc, t, title)
            if chat_id:
                bot.send_message(chat_id, f"Finished drawing: {title}")
        except Exception as e:
            print(f"[DRAW ERROR] {e}")
            if chat_id:
                bot.send_message(chat_id, f"Error drawing {title}: {e}")
    except queue.Empty:
        pass
    except KeyboardInterrupt:
        print("Stopping...")
        break
    except Exception as e:
        print(f"[MAIN LOOP ERROR] {e}")
