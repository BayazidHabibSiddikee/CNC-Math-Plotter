"""Test every user input path without Telegram or Tkinter."""
import sys, traceback
sys.path.insert(0, '.')

# Patch out Tkinter rendering in main_auto
import main_auto
main_auto.solution = lambda xc, yc, t, title: None

from main_auto import try_nlp, _eval_expr, PRESETS
import numpy as np

INPUTS = [
    # --- preset names exact ---
    "circle", "heart", "heart_curve", "butterfly", "spiral", "cardioid",
    "astroid", "lissajous", "rose", "petal_rose", "epitrochoid", "hypotrochoid",
    "rhodonea", "limacon", "cycloid", "deltoid", "lemniscate", "sine",
    "parabola", "logspiral", "logarithmic_spiral", "infinity", "star", "rainbow",
    # --- NLP natural language ---
    "draw a heart", "draw a heart curve", "show me a butterfly",
    "I want a circle", "make a spiral", "plot a parabola",
    "draw something like a flower", "can you draw infinity symbol",
    "I want to see a lemniscate", "draw a star", "show rainbow",
    "draw love", "round shape", "figure eight", "figure-eight",
    "bernoulli curve", "archimedean spiral", "logarithmic spiral",
    "sin wave", "sine wave",
    # --- equations ---
    "y = x^2", "y = x^2 + 3", "y = x^2 + c",
    "y = sin(x)", "y = cos(x)", "y = sin(x) + cos(x)",
    "y = 2*x + 1", "y = x^3", "y = x^3 - 2*x",
    "y = sqrt(x)", "y = exp(x)", "y = log(x)",
    "y = sin(x) + x", "y = cos(x)*x",
    "x = y^2", "x = sin(y)", "x = y^2 + 5",
    # --- /draw style (raw expressions) ---
    "r*cos(t)", "16*sin(t)**3",
    # --- edge cases ---
    "y = x", "y = 1", "y = -x",
    "circle radius 5", "circle radius 15",
    "heart curve", "petal rose",
]

passed = failed = 0
failures = []

for inp in INPUTS:
    try:
        result = try_nlp(inp)
        if result is None:
            failures.append((inp, "returned None"))
            failed += 1
            continue
        # validate expressions actually evaluate
        t = np.linspace(result.get("t_start", 0), result.get("t_end", 2*np.pi), 10)
        xc = _eval_expr(result["x_expr"], t, result.get("r", 10))
        yc = _eval_expr(result["y_expr"], t, result.get("r", 10))
        assert len(xc) == 10 and len(yc) == 10
        passed += 1
        print(f"  OK  {inp!r:45s} → {result.get('name', result['x_expr'])}")
    except Exception as e:
        failures.append((inp, str(e)))
        failed += 1
        print(f" FAIL {inp!r:45s} → {e}")

print(f"\n{passed} passed, {failed} failed out of {len(INPUTS)}")
if failures:
    print("\nFailed inputs:")
    for inp, err in failures:
        print(f"  {inp!r}: {err}")
