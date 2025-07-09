import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from predictor import predict_from_multipliers
from ocr_reader import extract_multipliers_from_image
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ACCURACY_FILE = "accuracy.json"

def load_accuracy():
    if not os.path.exists(ACCURACY_FILE):
        with open(ACCURACY_FILE, "w") as f:
            json.dump({"correct": 0, "wrong": 0}, f)
    with open(ACCURACY_FILE, "r") as f:
        return json.load(f)

def save_accuracy(data):
    with open(ACCURACY_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context):
    await update.message.reply_text("✈️ Aviator Predictor Bot चालू हो गया!")

async def predict(update: Update, context):
    multipliers = context.args
    if len(multipliers) < 5:
        await update.message.reply_text("कम से कम 5 multipliers दो! जैसे: `/predict 1.5 2.3 1.2 0.9 3.4`", parse_mode="Markdown")
        return
    result = predict_from_multipliers(multipliers)
    await update.message.reply_text(f"🔍 Prediction: {result}")

async def ocr(update: Update, context):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = "screenshot.jpg"
    await file.download_to_drive(file_path)
    multipliers = extract_multipliers_from_image(file_path)
    if not multipliers:
        await update.message.reply_text("❌ OCR से multipliers नहीं मिल पाए!")
        return
    result = predict_from_multipliers(multipliers)
    await update.message.reply_text(f"📸 OCR Prediction: {result}\n\nMultipliers: {multipliers}")

async def accuracy(update: Update, context):
    acc = load_accuracy()
    total = acc['correct'] + acc['wrong']
    if total == 0:
        percent = 0
    else:
        percent = round((acc['correct'] / total) * 100, 2)
    await update.message.reply_text(f"✅ Accuracy: {percent}%\n\nCorrect: {acc['correct']}, Wrong: {acc['wrong']}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))
app.add_handler(CommandHandler("accuracy", accuracy))
app.add_handler(MessageHandler(filters.PHOTO, ocr))

if __name__ == "__main__":
    print("✅ Bot चल रहा है...")
    app.run_polling()
