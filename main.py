import telebot
from telebot import types
import new  # Your file containing the Draw class

# --- CONFIGURATION ---
API = "8690254124:AAG4hFS89yHbsEcNT3Wsfoa6io1jlVUAGgI"
bot = telebot.TeleBot(token=API)

# Add authorized Telegram IDs here (Get yours from @userinfobot)
ALLOWED_USERS = [8058658801] # my real tele id -_-

# --- SECURITY CHECK ---
def is_authorized(message):
    print(message.from_user.id)
    return message.from_user.id in ALLOWED_USERS

# --- UTILITY: PARSE ARGUMENTS ---
def get_params(text):
    parts = text.split()
    try:
        if len(parts) < 4:
            return None, "Format: `/shape X Y Radius`"
        vals = [float(i) for i in parts[1:4]]
        return vals, None
    except ValueError:
        return None, "Please use numbers for X, Y, and Radius."

# --- COMMAND: START / MANUAL ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Security Check
    if not is_authorized(message):
        bot.reply_to(message, "🚫 Access Denied. Your ID is not whitelisted.")
        return

    manual = (
        "🤖 **CNC Virtual Controller v3.0**\n\n"
        f"Welcome, {message.from_user.first_name}. You can control the CNC via commands or images.\n\n"
        "📜 **1. Command Mode (Parametric)**\n"
        "Format: `/shape X Y Radius` (e.g., `/circle 0 0 10`)\n"
        "• `/circle`, `/heart_curve`, `/petal_rose` \n"
        "• `/lissajous`, `/butterfly`, `/spiral` \n"
        "• `/cardioid`, `/astroid`, `/epitrochoid` \n"
        "• `/hypotrochoid`, `/rhodonea`, `/limacon` \n"
        "• `/cycloid`, `/deltoid`, `/logarithmic_spiral` \n\n"
        "🖼 **2. Image Mode (Auto-Trace)**\n"
        "Simply send a **Photo** to this chat. The bot will automatically:\n"
        "1. Detect edges\n"
        "2. Simplify lines into a 'Cartoon' style\n"
        "3. Generate CNC toolpaths and plot them.\n\n"
        "⚠️ *Ensure images are clear and have high contrast for best results.*"
    )
    bot.reply_to(message, manual, parse_mode='Markdown')

# --- DYNAMIC SHAPE HANDLER ---
ALL_SHAPES = [
    'circle', 'heart_curve', 'petal_rose', 'lissajous', 'butterfly', 
    'spiral', 'cardioid', 'astroid', 'epitrochoid', 'hypotrochoid', 
    'rhodonea', 'limacon', 'cycloid', 'deltoid', 'logarithmic_spiral'
]

@bot.message_handler(commands=ALL_SHAPES)
def handle_all_drawings(message):
    if not is_authorized(message): return

    cmd = message.text.split()[0].replace('/', '').lower()
    params, error = get_params(message.text)
    
    if error:
        bot.reply_to(message, f"❌ {error}", parse_mode='Markdown')
        return

    x, y, r = params
    bot.send_message(message.chat.id, f"⚙️ Simulating `{cmd}`...")

    try:
        worker = new.Draw(x, y, r)
        drawing_func = getattr(worker, cmd)
        drawing_func() 
        bot.send_message(message.chat.id, f"✅ `{cmd}` complete.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

# --- IMAGE HANDLER (CARTOON TRACE) ---
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not is_authorized(message): return

    bot.reply_to(message, "🎨 Image received! Converting to CNC paths...")
    
    try:
        # Download the photo
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_name = "input_image.jpg"
        with open(image_name, 'wb') as f:
            f.write(downloaded_file)

        # Run your cartoon drawing logic from new.py
        worker = new.Draw(0, 0, 15)
        # Using the simplified 'draw_cartoon' we discussed
        worker.draw_cartoon(image_name) 
        
        bot.send_message(message.chat.id, "✅ Image trace simulation complete!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error processing image: {e}")

# --- FALLBACK ---
@bot.message_handler(func=lambda message: True)
def unknown_chat(message):
    if not is_authorized(message): return
    bot.reply_to(message, "❓ Unknown command. Use /help for instructions.")

bot.polling()