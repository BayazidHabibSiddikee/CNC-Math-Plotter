#!/usr/bin/env python3
"""
Smart CNC Controller - Comprehensive Project Documentation
Generates a complete PDF book covering all aspects of the project.
"""

from fpdf import FPDF
import os
from datetime import datetime

class ProjectBook(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Smart CNC Controller - Complete Documentation', 0, 0, 'L')
        self.cell(0, 10, f'Page {self.page_no()}', 0, 1, 'R')
        self.line(10, 15, 200, 15)
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'L')
        
    def chapter_title(self, num, title):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, f'Chapter {num}: {title}', 0, 1, 'L')
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(51, 51, 51)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
        
    def sub_section(self, title):
        self.set_font('Helvetica', 'BI', 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 7, title, 0, 1, 'L')
        self.ln(1)
        
    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(2)
        
    def code_block(self, code):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        
        lines = code.strip().split('\n')
        for line in lines:
            self.cell(0, 5, '  ' + line, 0, 1, 'L', True)
        self.ln(3)
        
    def bullet_point(self, text, indent=10):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(5, 5, '-', 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(1)
        
    def note_box(self, text):
        self.set_fill_color(255, 255, 220)
        self.set_draw_color(200, 200, 100)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 100, 0)
        
        x = self.get_x()
        y = self.get_y()
        
        self.rect(x, y, 190, 15, 'DF')
        self.set_xy(x + 5, y + 3)
        self.multi_cell(180, 4, text)
        self.set_xy(x, y + 18)


def create_book():
    pdf = ProjectBook()
    
    # ============================================
    # TITLE PAGE
    # ============================================
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, 'Smart CNC Controller', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, '& Path Generator', 0, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Complete Project Documentation', 0, 1, 'C')
    pdf.cell(0, 8, f'Version 4.0 - {datetime.now().strftime("%B %Y")}', 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 6, 
        'An intelligent 2-axis CNC path generation system combining\n'
        'Natural Language Processing, Mathematical Expression Parsing,\n'
        'and Computer Vision for precise toolpath creation.', 0, 'C')
    
    pdf.ln(15)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, 'Technologies: Python | Ollama | Tkinter | OpenCV | Telegram Bot API', 0, 1, 'C')
    pdf.cell(0, 6, 'Hardware: AVR/Arduino CNC Machines', 0, 1, 'C')
    
    # ============================================
    # TABLE OF CONTENTS
    # ============================================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, 'Table of Contents', 0, 1, 'L')
    pdf.ln(5)
    
    toc_items = [
        ('Chapter 1', 'Project Overview & Architecture', 3),
        ('Chapter 2', 'How Ollama Works - NLP Engine', 5),
        ('Chapter 3', 'How Tkinter Works - GUI Simulator', 8),
        ('Chapter 4', 'Telegram Bot Integration', 11),
        ('Chapter 5', 'Mathematical Expression Parser', 14),
        ('Chapter 6', 'Computer Vision & Image Tracing', 17),
        ('Chapter 7', 'AVR/Arduino Hardware Integration', 19),
        ('Chapter 8', 'Code Deep Dive - File by File', 21),
        ('Chapter 9', 'Docker Deployment Guide', 28),
        ('Chapter 10', 'API Reference & Commands', 30),
        ('Appendix A', 'Complete Preset Shapes Library', 32),
        ('Appendix B', 'Troubleshooting Guide', 34),
    ]
    
    for chapter, title, page in toc_items:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(25, 7, chapter, 0, 0)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(145, 7, title, 0, 0)
        pdf.cell(0, 7, str(page), 0, 1, 'R')
        pdf.ln(1)
    
    # ============================================
    # CHAPTER 1: PROJECT OVERVIEW
    # ============================================
    pdf.add_page()
    pdf.chapter_title(1, 'Project Overview & Architecture')
    
    pdf.section_title('1.1 Introduction')
    pdf.body_text(
        'The Smart CNC Controller is an intelligent 2-axis CNC path generation system that bridges '
        'the gap between human language and machine precision. By combining Natural Language Processing '
        '(NLP) via Ollama, robust mathematical expression parsing, and computer vision, this system '
        'allows users to create precise toolpaths using natural language commands, mathematical equations, '
        'or even by tracing images.'
    )
    
    pdf.body_text(
        'The system is designed as a Telegram bot interface, making it accessible from any device '
        'with Telegram installed. Users can simply type commands like "Draw a heart shape" or "Plot '
        'y = sin(x)" and the system will automatically generate the corresponding CNC paths, visualize '
        'them in a Tkinter simulator, and export them as C header files for AVR/Arduino hardware.'
    )
    
    pdf.section_title('1.2 Core Features')
    pdf.bullet_point('Intelligent NLP Parser using Ollama qwen2.5:0.5b model')
    pdf.bullet_point('Advanced regex-based mathematical expression parser')
    pdf.bullet_point('23+ preset mathematical curves and shapes')
    pdf.bullet_point('Image-to-CNC path tracing using OpenCV')
    pdf.bullet_point('Real-time visualization with Tkinter-based simulator')
    pdf.bullet_point('AVR-ready C header file export (Custom.h)')
    pdf.bullet_point('Telegram bot interface with user authentication')
    pdf.bullet_point('Docker deployment support')
    
    pdf.section_title('1.3 System Architecture')
    pdf.body_text(
        'The system follows a modular architecture with clear separation of concerns:\n\n'
        '1. Interface Layer (Telegram Bot) - Handles user interaction and authentication\n'
        '2. Processing Layer (NLP + Math Parser) - Converts user input to parametric equations\n'
        '3. Computation Layer (NumPy) - Generates coordinate arrays\n'
        '4. Visualization Layer (Tkinter) - Renders paths in real-time\n'
        '5. Export Layer (C Header Generator) - Creates hardware-ready files'
    )
    
    pdf.section_title('1.4 Project File Structure')
    pdf.code_block(
        'creating_CNC/\n'
        '  main_auto.py       - Entry point, Telegram bot logic, NLP pipeline\n'
        '  new.py             - Core engine: Draw class, curve generation, image tracing\n'
        '  CNC_simulation.py  - Tkinter-based CNC path visualizer\n'
        '  create_c_array.py  - Exports numpy arrays to C header files\n'
        '  Custom.h           - Generated C header with path data\n'
        '  requirements.txt   - Python dependencies\n'
        '  chat_history.json  - Conversation memory for context-aware responses\n'
        '  Dockerfile         - Docker deployment configuration\n'
        '  README.md          - Project documentation'
    )
    
    # ============================================
    # CHAPTER 2: HOW OLLAMA WORKS
    # ============================================
    pdf.add_page()
    pdf.chapter_title(2, 'How Ollama Works - NLP Engine')
    
    pdf.section_title('2.1 What is Ollama?')
    pdf.body_text(
        'Ollama is a lightweight framework for running large language models (LLMs) locally on your '
        'machine. It provides a simple API for interacting with various open-source models, including '
        'Llama, Mistral, and Qwen. In this project, we use Ollama to run the qwen2.5:0.5b model, '
        'which is a compact but capable language model optimized for instruction following.'
    )
    
    pdf.section_title('2.2 Installation & Setup')
    pdf.code_block(
        '# Install Ollama\n'
        'curl -fsSL https://ollama.com/install.sh | sh\n\n'
        '# Pull the qwen2.5:0.5b model\n'
        'ollama pull qwen2.5:0.5b\n\n'
        '# Start Ollama server\n'
        'ollama serve\n\n'
        '# Test the model\n'
        'ollama run qwen2.5:0.5b "Hello, how are you?"'
    )
    
    pdf.section_title('2.3 How Ollama Integration Works')
    pdf.body_text(
        'The project integrates Ollama through the official Python library. The integration works '
        'through two main functions:\n\n'
        '1. _ollama_parse(text) - Converts natural language to parametric equations\n'
        '2. ollama_respond(text) - Handles general conversation and guidance'
    )
    
    pdf.sub_section('NLP Parsing Pipeline')
    pdf.body_text(
        'When a user sends a message, the system follows this pipeline:\n\n'
        '1. First, check if the text matches a preset shape name\n'
        '2. If not, try to parse it as a mathematical equation using regex\n'
        '3. If that fails, send the text to Ollama with a specialized system prompt\n'
        '4. Ollama returns JSON with parametric equations\n'
        '5. If Ollama returns "NOT_DRAW", treat it as a conversation message'
    )
    
    pdf.section_title('2.4 System Prompt Engineering')
    pdf.body_text(
        'The system prompt for Ollama is carefully crafted to ensure reliable output. It instructs '
        'the model to:\n\n'
        '- Return ONLY valid JSON (no markdown, no explanation)\n'
        '- Use Python syntax for mathematical expressions\n'
        '- Include specific fields: x_expr, y_expr, t_start, t_end, n_points, r\n'
        '- Return "NOT_DRAW" for non-drawing requests'
    )
    
    pdf.code_block(
        '_SYSTEM_DRAW_PROMPT = """\n'
        'You are a CNC math parser. Convert user input to parametric equations.\n\n'
        'RULES:\n'
        '1. Return ONLY valid JSON:\n'
        '   {"x_expr": "...", "y_expr": "...", "t_start": 0, "t_end": 6.28,\n'
        '    "n_points": 300, "r": 10}\n'
        '2. Python syntax: t**2, sin(t), cos(t), sqrt(t), exp(t), pi\n'
        '3. If NOT a draw request, reply: NOT_DRAW\n'
        '"""'
    )
    
    pdf.section_title('2.5 Response Parsing')
    pdf.body_text(
        'The Ollama response is parsed with error handling:\n\n'
        '1. Check if response contains "NOT_DRAW"\n'
        '2. Remove markdown code block markers if present\n'
        '3. Parse JSON and validate required fields\n'
        '4. Return None on any error (falls back to conversation mode)'
    )
    
    pdf.code_block(
        'def _ollama_parse(text):\n'
        '    try:\n'
        '        resp = ollama.chat(\n'
        '            model=OLLAMA_MODEL,\n'
        '            messages=[\n'
        '                {"role": "system", "content": _SYSTEM_DRAW_PROMPT},\n'
        '                {"role": "user", "content": text},\n'
        '            ],\n'
        '        )\n'
        '        raw = resp["message"]["content"]\n'
        '        if "NOT_DRAW" in raw:\n'
        '            return None\n'
        '        cleaned = re.sub(r"^```(?:json)?\\s*\\n?", "", raw.strip())\n'
        '        cleaned = re.sub(r"\\s*```$", "", cleaned)\n'
        '        data = json.loads(cleaned)\n'
        '        return data\n'
        '    except Exception:\n'
        '        return None'
    )
    
    pdf.section_title('2.6 Conversation Memory')
    pdf.body_text(
        'The system maintains conversation history in chat_history.json. This allows Ollama to '
        'provide context-aware responses. The history is limited to the last 10 messages (5 pairs '
        'of user-assistant exchanges) to prevent context overflow.'
    )
    
    pdf.section_title('2.7 Model Selection Rationale')
    pdf.body_text(
        'The qwen2.5:0.5b model was chosen for several reasons:\n\n'
        '1. Small size (0.5 billion parameters) - runs on consumer hardware\n'
        '2. Fast inference - suitable for real-time interaction\n'
        '3. Good at following instructions - reliable JSON output\n'
        '4. Supports mathematical reasoning - understands equations\n'
        '5. Free and open source - no API costs'
    )
    
    # ============================================
    # CHAPTER 3: HOW TKINTER WORKS
    # ============================================
    pdf.add_page()
    pdf.chapter_title(3, 'How Tkinter Works - GUI Simulator')
    
    pdf.section_title('3.1 Introduction to Tkinter')
    pdf.body_text(
        'Tkinter is Python\'s standard GUI (Graphical User Interface) library. It provides a '
        'powerful set of tools for creating windows, dialogs, buttons, and drawing canvases. '
        'In this project, Tkinter is used to create a real-time CNC path visualizer that shows '
        'exactly what the machine will do before sending it to hardware.'
    )
    
    pdf.section_title('3.2 Tkinter Architecture')
    pdf.body_text(
        'Tkinter follows a hierarchical widget-based architecture:\n\n'
        '1. Root Window (Tk) - The main application window\n'
        '2. Canvas Widget - Drawing area for paths and shapes\n'
        '3. Event Loop (mainloop) - Handles user interactions and updates'
    )
    
    pdf.section_title('3.3 The CNC Simulation Class')
    pdf.body_text(
        'The CNC_simulation.py file defines a comprehensive CNC simulation class that wraps '
        'Tkinter functionality into a user-friendly API. Key features include:'
    )
    
    pdf.bullet_point('Coordinate system transformation (real coords to canvas pixels)')
    pdf.bullet_point('Animated path drawing with configurable speed')
    pdf.bullet_point('Grid and axis visualization')
    pdf.bullet_point('Tool position tracking (red dot marker)')
    pdf.bullet_point('Multiple drawing primitives: point, segment, line_to, move_to')
    pdf.bullet_point('PostScript export capability')
    
    pdf.section_title('3.4 Coordinate System Transformation')
    pdf.body_text(
        'The simulator converts real-world CNC coordinates to canvas pixel coordinates using '
        'a transformation function. The canvas has its origin at the top-left corner, while '
        'CNC coordinates have the origin at the center with Y-axis pointing up.'
    )
    
    pdf.code_block(
        'def _to_canvas_coords(self, x, y):\n'
        '    canvas_x = (x - self.x_min) * self.x_scale\n'
        '    canvas_y = self.height - (y - self.y_min) * self.y_scale\n'
        '    return canvas_x, canvas_y'
    )
    
    pdf.section_title('3.5 Animation System')
    pdf.body_text(
        'The animation system provides smooth, real-time visualization of path drawing. '
        'It uses frame-based interpolation to animate tool movement:\n\n'
        '1. Calculate number of steps based on delay or speed\n'
        '2. Interpolate between start and end points\n'
        '3. Update tool position marker at each step\n'
        '4. Draw line segments progressively\n'
        '5. Sleep between frames for smooth animation'
    )
    
    pdf.code_block(
        'def _animate_segment(self, x1, y1, x2, y2, color=\'blue\', width=2):\n'
        '    # Calculate number of steps (target 60 FPS)\n'
        '    num_steps = max(int(self.draw_delay * 60), 10)\n'
        '    \n'
        '    for i in range(num_steps + 1):\n'
        '        t = i / num_steps\n'
        '        curr_x = x1 + t * (x2 - x1)\n'
        '        curr_y = y1 + t * (y2 - y1)\n'
        '        \n'
        '        self.current_x = curr_x\n'
        '        self.current_y = curr_y\n'
        '        self._update_tool_position()\n'
        '        \n'
        '        # Draw line segment\n'
        '        if i > 0:\n'
        '            self.canvas.create_line(prev_cx, prev_cy, curr_cx, curr_cy,\n'
        '                                   fill=color, width=width)\n'
        '        \n'
        '        self.canvas.update()\n'
        '        time.sleep(self.draw_delay / num_steps)'
    )
    
    pdf.section_title('3.6 Grid and Axes Drawing')
    pdf.body_text(
        'The simulator draws a grid system with configurable spacing. Vertical and horizontal '
        'grid lines are drawn with dashed styling. The X and Y axes are drawn as solid black '
        'lines, with an origin point marker.'
    )
    
    pdf.section_title('3.7 Thread Safety')
    pdf.body_text(
        'Since Tkinter is not thread-safe, the project uses a queue-based architecture. '
        'The Telegram bot runs in a separate thread and places draw requests into a queue. '
        'The main thread (which owns Tkinter) drains the queue and executes drawing operations. '
        'This ensures all GUI operations happen in the main thread.'
    )
    
    pdf.code_block(
        '# Main thread owns Tkinter - drain draw queue forever\n'
        'while True:\n'
        '    try:\n'
        '        data = _draw_queue.get(timeout=1)\n'
        '        # Execute drawing in main thread\n'
        '        new.solution(xc, yc, t, title)\n'
        '    except queue.Empty:\n'
        '        pass'
    )
    
    # ============================================
    # CHAPTER 4: TELEGRAM BOT INTEGRATION
    # ============================================
    pdf.add_page()
    pdf.chapter_title(4, 'Telegram Bot Integration')
    
    pdf.section_title('4.1 Telegram Bot API')
    pdf.body_text(
        'Telegram provides a powerful Bot API that allows developers to create automated '
        'chatbots. The pyTelegramBotAPI library (telebot) provides a Python wrapper for this '
        'API, making it easy to handle messages, commands, and media.'
    )
    
    pdf.section_title('4.2 Bot Configuration')
    pdf.body_text(
        'The bot is configured with three key parameters:\n\n'
        '1. API Token - Obtained from BotFather on Telegram\n'
        '2. ALLOWED_USERS - List of authorized Telegram user IDs\n'
        '3. CONNECT_TIMEOUT - Network timeout (30 seconds)'
    )
    
    pdf.code_block(
        'API = "8690254124:AAG4hFS89yHbsEcNT3Wsfoa6io1jlVUAGgI"\n'
        'bot = telebot.TeleBot(token=API)\n'
        'apihelper.CONNECT_TIMEOUT = 30\n'
        'ALLOWED_USERS = [8058658801, 1667679794]'
    )
    
    pdf.section_title('4.3 Security & Authentication')
    pdf.body_text(
        'The system implements a simple but effective authentication mechanism. Each incoming '
        'message is checked against the ALLOWED_USERS list. Unauthorized users receive a message '
        'with their Telegram ID, which they can share with the admin to gain access.'
    )
    
    pdf.code_block(
        'def is_authorized(message):\n'
        '    uid = message.from_user.id\n'
        '    if uid not in ALLOWED_USERS:\n'
        '        bot.reply_to(message, f"Access denied. Send your ID to admin: {uid}")\n'
        '        return False\n'
        '    return True'
    )
    
    pdf.section_title('4.4 Message Handlers')
    pdf.body_text(
        'The bot uses decorator-based message handlers to process different types of input:\n\n'
        '1. /start, /help - Display welcome message and available commands\n'
        '2. /myid - Return user\'s Telegram ID\n'
        '3. /demo - Run sequence of 5 preset shapes\n'
        '4. /draw x|y|pts - Manual parametric drawing mode\n'
        '5. /<shape_name> - Draw specific preset shape\n'
        '6. Photo messages - Convert image to CNC paths\n'
        '7. Text messages - Parse with NLP pipeline'
    )
    
    pdf.section_title('4.5 Command Registration')
    pdf.body_text(
        'Bot commands are registered both via decorators and via the set_my_commands API. '
        'This provides autocomplete suggestions in the Telegram interface.'
    )
    
    pdf.code_block(
        'bot.set_my_commands([\n'
        '    telebot.types.BotCommand("myid", "Get your Telegram ID"),\n'
        '    telebot.types.BotCommand("start", "Show help & commands"),\n'
        '    telebot.types.BotCommand("demo", "Run 5 preset shapes"),\n'
        '    telebot.types.BotCommand("heart", "Heart curve"),\n'
        '    telebot.types.BotCommand("circle", "Circle"),\n'
        '    # ... more commands\n'
        '])'
    )
    
    pdf.section_title('4.6 Photo Handling')
    pdf.body_text(
        'When a user sends a photo, the bot:\n\n'
        '1. Downloads the photo using bot.get_file() and bot.download_file()\n'
        '2. Saves it as input_image.jpg\n'
        '3. Creates a Draw instance and calls draw_cartoon()\n'
        '4. OpenCV processes the image and generates CNC paths\n'
        '5. The paths are visualized in the Tkinter simulator'
    )
    
    pdf.section_title('4.7 Polling vs Webhooks')
    pdf.body_text(
        'This project uses long polling instead of webhooks. Polling is simpler to set up '
        'and doesn\'t require a public server or HTTPS certificate. The bot runs in a daemon '
        'thread with a 60-second timeout.'
    )
    
    pdf.code_block(
        'threading.Thread(\n'
        '    target=lambda: bot.polling(\n'
        '        none_stop=True,\n'
        '        timeout=60,\n'
        '        long_polling_timeout=60\n'
        '    ),\n'
        '    daemon=True\n'
        ').start()'
    )
    
    # ============================================
    # CHAPTER 5: MATH EXPRESSION PARSER
    # ============================================
    pdf.add_page()
    pdf.chapter_title(5, 'Mathematical Expression Parser')
    
    pdf.section_title('5.1 Overview')
    pdf.body_text(
        'The mathematical expression parser is a robust regex-based system that converts '
        'human-friendly math expressions into NumPy-evaluable strings. It handles implicit '
        'multiplication, trigonometric functions, and various notation styles.'
    )
    
    pdf.section_title('5.2 Supported Syntax')
    pdf.body_text('The parser supports various input formats:')
    
    pdf.bullet_point('Standard notation: y = sin(x), y = x^2 + 5')
    pdf.bullet_point('Implicit multiplication: 2x becomes 2*x')
    pdf.bullet_point('Function calls: sinx becomes sin(x), sqrt(x) works')
    pdf.bullet_point('Parentheses groups: (x+1)(x-1) becomes (x+1)*(x-1)')
    pdf.bullet_point('Power notation: x^2 becomes x**2')
    pdf.bullet_point('Both x and y as dependent variables')
    
    pdf.section_title('5.3 Parsing Pipeline')
    pdf.body_text('The regex parser follows these steps:')
    
    pdf.code_block(
        '1. Match equation pattern: y = ... or x = ...\n'
        '2. Infer dependent variable if no = sign\n'
        '3. Replace ^ with ** (power operator)\n'
        '4. Add parentheses to trig functions: sin x -> sin(x)\n'
        '5. Add implicit multiplication: 2x -> 2*x\n'
        '6. Replace dependent variable with t (parameter)\n'
        '7. Replace unknown constants with 1\n'
        '8. Auto-detect range based on function type\n'
        '9. Validate by test evaluation'
    )
    
    pdf.section_title('5.4 Range Detection')
    pdf.body_text(
        'The parser automatically determines the parameter range based on the functions present:\n\n'
        '1. Trigonometric functions (sin, cos, tan): -2pi to 2pi\n'
        '2. Logarithmic/Square root: 0.1 to 10\n'
        '3. Polynomial/Linear: -4 to 4'
    )
    
    pdf.section_title('5.5 Safe Evaluation')
    pdf.body_text(
        'All mathematical expressions are evaluated in a restricted environment to prevent '
        'code injection. The eval() function is called with __builtins__: {} and a whitelist '
        'of safe functions and constants.'
    )
    
    pdf.code_block(
        '_SAFE_MATH = {\n'
        '    "sin": np.sin, "cos": np.cos, "tan": np.tan,\n'
        '    "sqrt": np.sqrt, "exp": np.exp, "log": np.log,\n'
        '    "abs": np.abs, "pi": np.pi, "e": np.e,\n'
        '}\n\n'
        'def _eval_expr(expr, t, r=10.0):\n'
        '    safe = {"t": t, "r": r, "np": np, **_SAFE_MATH}\n'
        '    val = eval(expr, {"__builtins__": {}}, safe)\n'
        '    return val'
    )
    
    pdf.section_title('5.6 Preset Lookup System')
    pdf.body_text(
        'Before attempting regex parsing, the system checks if the input matches any preset '
        'shape names or NLP keywords. This provides instant response for common shapes without '
        'needing the LLM.'
    )
    
    # ============================================
    # CHAPTER 6: COMPUTER VISION
    # ============================================
    pdf.add_page()
    pdf.chapter_title(6, 'Computer Vision & Image Tracing')
    
    pdf.section_title('6.1 OpenCV Integration')
    pdf.body_text(
        'OpenCV (Open Source Computer Vision Library) is used to convert user-provided images '
        'into CNC toolpaths. The image_to_cnc_coords() function implements a pipeline that '
        'extracts contours and simplifies them for CNC machining.'
    )
    
    pdf.section_title('6.2 Image Processing Pipeline')
    pdf.body_text('The image tracing follows these steps:')
    
    pdf.code_block(
        '1. Load image in grayscale mode\n'
        '2. Apply Gaussian Blur to remove noise\n'
        '3. Apply binary threshold (127) to create B&W image\n'
        '4. Find external contours using cv2.findContours()\n'
        '5. Simplify each contour using Douglas-Peucker algorithm\n'
        '6. Scale coordinates to CNC range (-scale to +scale)\n'
        '7. Return list of simplified paths'
    )
    
    pdf.section_title('6.3 Contour Simplification')
    pdf.body_text(
        'The Douglas-Peucker algorithm (cv2.approxPolyDP) is key to the "cartoon" effect. '
        'The epsilon parameter controls simplification:\n\n'
        '- Higher epsilon = more simplified/blocky\n'
        '- Lower epsilon = more detailed/smooth\n\n'
        'In this project, epsilon = 0.02 * arcLength provides good balance.'
    )
    
    pdf.code_block(
        '# THE CARTOON TRICK\n'
        'epsilon = 0.02 * cv2.arcLength(cnt, True)\n'
        'approx = cv2.approxPolyDP(cnt, epsilon, True)\n\n'
        '# Only keep shapes with more than 2 points\n'
        'if len(approx) > 2:\n'
        '    points = approx.reshape(-1, 2).astype(float)\n'
        '    # Scale to CNC range\n'
        '    points[:, 0] = (points[:, 0] / img.shape[1] - 0.5) * (scale * 2)\n'
        '    points[:, 1] = (0.5 - points[:, 1] / img.shape[0]) * (scale * 2)'
    )
    
    pdf.section_title('6.4 Coordinate Scaling')
    pdf.body_text(
        'Image pixel coordinates are converted to CNC coordinates with origin at center. '
        'The X-axis is centered horizontally and the Y-axis is inverted (image Y increases '
        'downward, CNC Y increases upward).'
    )
    
    # ============================================
    # CHAPTER 7: HARDWARE INTEGRATION
    # ============================================
    pdf.add_page()
    pdf.chapter_title(7, 'AVR/Arduino Hardware Integration')
    
    pdf.section_title('7.1 C Header File Export')
    pdf.body_text(
        'The create_c_array.py module converts Python/NumPy arrays into C header files '
        'suitable for AVR/Arduino projects. The export includes:\n\n'
        '- NUM_POINTS constant (number of path points)\n'
        '- path_x[] float array (X coordinates)\n'
        '- path_y[] float array (Y coordinates)\n'
        '- path_z[] float array (Z coordinates)'
    )
    
    pdf.section_title('7.2 Export Format')
    pdf.code_block(
        '#define NUM_POINTS 300\n\n'
        'float path_x[] = {\n'
        '    0.500000f,\n'
        '    0.503775f,\n'
        '    0.506681f,\n'
        '    // ... more points\n'
        '};\n\n'
        'float path_y[] = {\n'
        '    0.000000f,\n'
        '    0.021185f,\n'
        '    // ... more points\n'
        '};'
    )
    
    pdf.section_title('7.3 Arduino Integration Example')
    pdf.body_text('To use the generated header in an Arduino project:')
    
    pdf.code_block(
        '#include "Custom.h"\n\n'
        'void executePath() {\n'
        '    for(int i = 0; i < NUM_POINTS; i++) {\n'
        '        moveTo(path_x[i], path_y[i]);\n'
        '        // Optionally control Z-axis:\n'
        '        // setZ(path_z[i]);\n'
        '    }\n'
        '}\n\n'
        'void setup() {\n'
        '    // Initialize stepper motors\n'
        '    // Set microstepping, speed, etc.\n'
        '}\n\n'
        'void loop() {\n'
        '    executePath();\n'
        '    delay(5000); // Wait 5 seconds\n'
        '}'
    )
    
    pdf.section_title('7.4 float Precision')
    pdf.body_text(
        'Coordinates are exported as float with 6 decimal places (e.g., 0.500000f). '
        'This provides sufficient precision for most CNC applications while keeping '
        'file sizes reasonable.'
    )
    
    # ============================================
    # CHAPTER 8: CODE DEEP DIVE
    # ============================================
    pdf.add_page()
    pdf.chapter_title(8, 'Code Deep Dive - File by File')
    
    pdf.section_title('8.1 main_auto.py - Entry Point')
    pdf.body_text(
        'This is the main entry point that orchestrates all components. Key sections:\n\n'
        '1. Configuration (lines 1-16) - API tokens, model selection, user whitelist\n'
        '2. Preset Shapes (lines 18-47) - Dictionary of 23+ mathematical curves\n'
        '3. NLP Keywords (lines 49-71) - Keyword-to-preset mapping\n'
        '4. Safe Math Eval (lines 73-89) - Restricted evaluation environment\n'
        '5. Render Queue (lines 91-95) - Thread-safe drawing interface\n'
        '6. NLP Pipeline (lines 97-223) - Ollama + regex parsing\n'
        '7. Security (lines 272-279) - User authentication\n'
        '8. Handlers (lines 281-461) - Telegram message processing\n'
        '9. Main Loop (lines 442-462) - Tkinter queue processor'
    )
    
    pdf.section_title('8.2 new.py - Core Engine')
    pdf.body_text(
        'Contains the Draw class and curve generation logic:\n\n'
        '1. image_to_cnc_coords() - OpenCV image processing\n'
        '2. solution() - Renders curves and exports to C header\n'
        '3. Draw class - 20+ curve generation methods\n\n'
        'Each curve method follows the pattern:\n'
        '- Generate parameter t using np.linspace\n'
        '- Calculate x and y coordinates using NumPy\n'
        '  operations\n'
        '- Call solution() to render and export'
    )
    
    pdf.section_title('8.3 CNC_simulation.py - Visualizer')
    pdf.body_text(
        'Complete Tkinter-based visualization system:\n\n'
        '1. CNC class - Main simulation engine\n'
        '2. Coordinate transformation - Real to canvas coords\n'
        '3. Animation system - Frame-based interpolation\n'
        '4. Drawing primitives - point, segment, line_to, move_to\n'
        '5. Grid/axes rendering - Visual reference\n'
        '6. Helper function - plot_path() for multi-point paths'
    )
    
    pdf.section_title('8.4 create_c_array.py - Exporter')
    pdf.body_text(
        'Simple but effective C header generator:\n\n'
        '1. Takes x, y, z numpy arrays as input\n'
        '2. Writes #define NUM_POINTS\n'
        '3. Writes path_x[], path_y[], path_z[] float arrays\n'
        '4. Uses 6 decimal place precision'
    )
    
    # ============================================
    # CHAPTER 9: DOCKER DEPLOYMENT
    # ============================================
    pdf.add_page()
    pdf.chapter_title(9, 'Docker Deployment Guide')
    
    pdf.section_title('9.1 Dockerfile Overview')
    pdf.body_text(
        'The Dockerfile creates a self-contained environment with all dependencies. '
        'Key components:\n\n'
        '1. Base image: Python 3.11-slim\n'
        '2. System packages: tk-dev, OpenCV dependencies\n'
        '3. Ollama installation and model download\n'
        '4. Python dependencies from requirements.txt\n'
        '5. Startup script that runs both Ollama and the bot'
    )
    
    pdf.section_title('9.2 Building the Image')
    pdf.code_block(
        '# Build the Docker image\n'
        'docker build -t cnc-controller .\n\n'
        '# This will:\n'
        '# 1. Pull Python 3.11-slim base image\n'
        '# 2. Install system dependencies\n'
        '# 3. Install Python packages\n'
        '# 4. Install Ollama\n'
        '# 5. Download qwen2.5:0.5b model\n'
        '# 6. Copy application files'
    )
    
    pdf.section_title('9.3 Running the Container')
    pdf.code_block(
        '# Run with Telegram bot token\n'
        'docker run -d --name cnc-bot \\\n'
        '    -e TELEGRAM_TOKEN="your_token_here" \\\n'
        '    cnc-controller\n\n'
        '# Run with GPU support (for faster Ollama)\n'
        'docker run -d --gpus all --name cnc-bot cnc-controller\n\n'
        '# View logs\n'
        'docker logs -f cnc-bot'
    )
    
    pdf.section_title('9.4 Docker Compose')
    pdf.body_text('For production deployment, consider using docker-compose:')
    
    pdf.code_block(
        'version: "3.8"\n'
        'services:\n'
        '  cnc-bot:\n'
        '    build: .\n'
        '    container_name: cnc-controller\n'
        '    restart: unless-stopped\n'
        '    environment:\n'
        '      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}\n'
        '    volumes:\n'
        '      - ./data:/app/data\n'
        '    ports:\n'
        '      - "11434:11434"'
    )
    
    pdf.section_title('9.5 Environment Variables')
    pdf.body_text(
        'Important environment variables:\n\n'
        '- TELEGRAM_TOKEN: Bot API token\n'
        '- ALLOWED_USERS: Comma-separated user IDs\n'
        '- OLLAMA_MODEL: Model to use (default: qwen2.5:0.5b)\n'
        '- DISPLAY: For headless systems (use Xvfb)'
    )
    
    # ============================================
    # CHAPTER 10: API REFERENCE
    # ============================================
    pdf.add_page()
    pdf.chapter_title(10, 'API Reference & Commands')
    
    pdf.section_title('10.1 Telegram Bot Commands')
    pdf.body_text('Available commands:')
    
    commands = [
        ('/start', 'Show welcome message and available commands'),
        ('/help', 'Display help information'),
        ('/myid', 'Return your Telegram user ID'),
        ('/demo', 'Run 5 preset shapes in sequence'),
        ('/draw x|y|pts|t0|t1', 'Draw custom parametric equation'),
        ('/circle [radius]', 'Draw circle (default r=10)'),
        ('/heart', 'Draw heart curve'),
        ('/butterfly', 'Draw butterfly curve'),
        ('/spiral', 'Draw Archimedean spiral'),
        ('/rose', 'Draw 5-petal rose'),
        ('/cardioid', 'Draw cardioid'),
        ('/lissajous', 'Draw Lissajous figure-8'),
        ('/astroid', 'Draw astroid'),
        ('/star', 'Draw 5-point star'),
        ('/infinity', 'Draw infinity symbol'),
        ('/parabola', 'Draw parabola y=x^2'),
        ('/sine', 'Draw sine wave'),
        ('/lemniscate', 'Draw lemniscate of Bernoulli'),
        ('/cycloid', 'Draw cycloid'),
        ('/deltoid', 'Draw deltoid'),
    ]
    
    for cmd, desc in commands:
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(45, 6, cmd, 0, 0)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 6, desc, 0, 1)
    
    pdf.section_title('10.2 Natural Language Examples')
    pdf.body_text('You can also type naturally:')
    
    pdf.bullet_point('"Draw a heart shape for my girlfriend"')
    pdf.bullet_point('"Make a circle with radius 15"')
    pdf.bullet_point('"Plot a butterfly curve"')
    pdf.bullet_point('"y = sin(x)" or "y = x^2 + 3x"')
    pdf.bullet_point('"x = cos(y)"')
    
    pdf.section_title('10.3 Image Mode')
    pdf.body_text(
        'Send any photo to the bot and it will:\n'
        '1. Trace the image contours\n'
        '2. Simplify to "cartoon" style\n'
        '3. Convert to CNC toolpaths\n'
        '4. Visualize in the simulator'
    )
    
    pdf.section_title('10.4 Draw Class Methods')
    pdf.body_text('The Draw class in new.py provides these curve methods:')
    
    methods = [
        'circle(radius)', 'heart_curve()', 'petal_rose(radius)',
        'lissajous(radius)', 'butterfly(radius)', 'spiral(radius)',
        'cardioid(radius)', 'astroid(radius)', 'epitrochoid(radius)',
        'hypotrochoid(radius)', 'rhodonea(radius, petals)',
        'limacon(radius)', 'cycloid(radius)', 'deltoid(radius)',
        'logarithmic_spiral(radius)', 'lemniscate(radius)',
        'sine_wave(amplitude, frequency, length)',
        'witch_of_agnesi(radius)', 'draw_image(image_path)'
    ]
    
    for method in methods:
        pdf.set_font('Courier', '', 9)
        pdf.cell(0, 5, f'  Draw.x, y, r.{method}', 0, 1)
    
    # ============================================
    # APPENDIX A: PRESET SHAPES
    # ============================================
    pdf.add_page()
    pdf.chapter_title('A', 'Complete Preset Shapes Library')
    
    pdf.body_text('All 23+ preset shapes with their parametric equations:')
    pdf.ln(3)
    
    presets = [
        ('circle', 'x = r*cos(t), y = r*sin(t)', '0 to 2pi'),
        ('heart', 'x = 16*sin^3(t), y = 13*cos(t)-5*cos(2t)-2*cos(3t)-cos(4t)', '0 to 2pi'),
        ('rose', 'x = r*cos(5t)*cos(t), y = r*cos(5t)*sin(t)', '0 to pi'),
        ('lissajous', 'x = r*sin(t), y = r*sin(2t)', '0 to 2pi'),
        ('butterfly', 'x = r*sin(t)*expr, y = r*cos(t)*expr', '0 to 10pi'),
        ('spiral', 'x = (r/10)*t*cos(t), y = (r/10)*t*sin(t)', '0 to 8pi'),
        ('cardioid', 'x = r*(1+cos(t))*cos(t), y = r*(1+cos(t))*sin(t)', '0 to 2pi'),
        ('astroid', 'x = r*cos^3(t), y = r*sin^3(t)', '0 to 2pi'),
        ('epitrochoid', 'x = (R+rs)*cos(t)-d*cos((R+rs)/rs*t)', '0 to 2pi'),
        ('hypotrochoid', 'x = (R-rs)*cos(t)+d*cos((R-rs)/rs*t)', '0 to 2pi'),
        ('rhodonea', 'x = r*cos(kt)*cos(t), y = r*cos(kt)*sin(t)', '0 to pi'),
        ('limacon', 'x = r*(1+0.5*cos(t))*cos(t)', '0 to 2pi'),
        ('cycloid', 'x = r*(t-sin(t)), y = r*(1-cos(t))', '0 to 4pi'),
        ('deltoid', 'x = r*(2*cos(t)+cos(2t))', '0 to 2pi'),
        ('lemniscate', 'x = r*cos(t)/(1+sin^2(t))', '0 to 2pi'),
        ('sine', 'x = t, y = r*sin(3t)', '-10 to 10'),
        ('parabola', 'x = t, y = t^2', '-4 to 4'),
        ('logspiral', 'x = (r/20)*e^(0.2t)*cos(t)', '0 to 4pi'),
        ('infinity', 'x = r*sin(t), y = r*sin(t)*cos(t)/(1+sin^2(t))', '0 to 2pi'),
        ('star', 'x = r*cos(t)*(1+0.3*cos(5t))', '0 to 2pi'),
        ('rainbow', 'x = (r/3)*t*cos(t), y = (r/3)*t*sin(t)', '0 to 12pi'),
    ]
    
    for name, eq, range_ in presets:
        pdf.set_font('Courier', 'B', 9)
        pdf.cell(30, 5, name, 0, 0)
        pdf.set_font('Courier', '', 8)
        pdf.cell(100, 5, eq, 0, 0)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.cell(0, 5, f'[{range_}]', 0, 1)
        pdf.ln(1)
    
    # ============================================
    # APPENDIX B: TROUBLESHOOTING
    # ============================================
    pdf.add_page()
    pdf.chapter_title('B', 'Troubleshooting Guide')
    
    pdf.section_title('Common Issues & Solutions')
    
    issues = [
        ('Ollama not starting', 
         'Ensure ollama serve is running. Check with: curl http://localhost:11434/api/tags'),
        ('Model not found',
         'Pull the model: ollama pull qwen2.5:0.5b'),
        ('Telegram bot not responding',
         'Check API token and network connection. Verify ALLOWED_USERS list.'),
        ('Tkinter error in Docker',
         'Install xvfb for headless display: apt-get install xvfb'),
        ('OpenCV import error',
         'Install system dependencies: apt-get install libgl1-mesa-glx'),
        ('Permission denied on Custom.h',
         'Check file permissions: chmod 644 Custom.h'),
        ('Memory issues with large images',
         'Resize images before sending to bot'),
        ('Animation too fast/slow',
         'Adjust draw_delay parameter in CNC class'),
    ]
    
    for issue, solution in issues:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(180, 0, 0)
        pdf.cell(0, 6, f'Issue: {issue}', 0, 1)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 100, 0)
        pdf.multi_cell(0, 5, f'Solution: {solution}')
        pdf.ln(3)
    
    pdf.section_title('Performance Tips')
    pdf.bullet_point('Use fewer points (100-200) for faster simulation')
    pdf.bullet_point('Increase draw_delay for slower, more visible animation')
    pdf.bullet_point('Run Ollama on GPU for faster NLP responses')
    pdf.bullet_point('Use Docker with --gpus all for GPU acceleration')
    pdf.bullet_point('Pre-download models in Docker build for faster startup')
    
    # Save the PDF
    output_path = 'Smart_CNC_Controller_Documentation.pdf'
    pdf.output(output_path)
    print(f'PDF book generated successfully: {output_path}')
    print(f'Total pages: {pdf.page_no()}')


if __name__ == '__main__':
    create_book()
