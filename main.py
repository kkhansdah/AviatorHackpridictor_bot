import os
import json
import pytesseract
from dotenv import load_dotenv
from PIL import Image
import cv2
import numpy as np
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ACCURACY_FILE = "accuracy.json"

# ===== Accuracy Tracker =====
def load_accuracy():
    if not os.path.exists(ACCURACY_FILE):
        with open(ACCURACY_FILE, "w") as f:
            json.dump({"correct": 0, "wrong": 0}, f)
    with open(ACCURACY_FILE, "r") as f:
        return json.load(f)

def save_accuracy(data):
    with open(ACCURACY_FILE, "w") as f:
        json.dump(data, f)

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🙏 नमस्ते! Aviator Predictor Bot चालू है!\n/predict या /ocr भेजो!")

# ===== /predict manually =====
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 5:
        await update.message.reply_text("❌ कम से कम 5 multipliers भेजो!\nउदाहरण: /predict 1.2 2.4 1.5 0.9 2.1")
        return
    try:
        nums = [float(x) for x in context.args]
        avg = sum(nums) / len(nums)
        if avg < 2:
            msg = "🔴 Pattern Weak लग रहा है!\n🚫 Avoid Betting"
        elif avg < 3:
            msg = "🟡 Medium Pattern\n⏳ Wait or Low Bet"
        else:
            msg = "✅ Strong Pattern!\n🟢 Safe Bet कर सकते हो"
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text("❌ Invalid input! सभी multipliers नंबर में होने चाहिए")

# ===== /ocr =====
async def ocr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("📷 कृपया Aviator screenshot भेजो OCR के लिए।")
        return

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_path = "screenshot.jpg"
    await file.download_to_drive(image_path)

    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

        # Filter only numbers (with decimal point)
        multipliers = [float(x) for x in text.replace('x', '').split() if x.replace('.', '', 1).isdigit()]
        if len(multipliers) < 5:
            await update.message.reply_text("❌ कम से कम 5 multipliers चाहिए OCR से!\nस्पष्ट screenshot भेजो.")
            return

        avg = sum(multipliers[:10]) / min(10, len(multipliers))
        if avg < 2:
            msg = "🔴 Weak Pattern (OCR)\n🚫 Avoid Betting"
        elif avg < 3:
            msg = "🟡 Medium Pattern (OCR)\n⏳ Wait or Small Bet"
        else:
            msg = "✅ Strong Pattern (OCR)\n🟢 Safe Bet Based on Screenshot!"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ OCR Failed: {str(e)}")

# ===== /accuracy =====
async def accuracy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_accuracy()
    total = data['correct'] + data['wrong']
    percent = (data['correct'] / total * 100) if total > 0 else 0
    await update.message.reply_text(f"📊 Accuracy:\n✅ सही: {data['correct']}\n❌ गलत: {data['wrong']}\n🎯 Percent: {percent:.2f}%")

# ===== Run Bot =====
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))
app.add_handler(CommandHandler("ocr", ocr))
app.add_handler(CommandHandler("accuracy", accuracy))
app.run_polling()
