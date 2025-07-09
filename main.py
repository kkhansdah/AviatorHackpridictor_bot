import telebot
import time
from scraper import get_live_data
from predictor import predict_from_list
from ocr_reader import read_multipliers_from_image
from graph import generate_graph

BOT_TOKEN = "7832938380:AAFcNqOFR6uIcU9_Yfak4ijddMBxlj8_ScY"
bot = telebot.TeleBot(BOT_TOKEN)

ACTIVE_USERS = set()
correct = 0
total = 0

@bot.message_handler(commands=['start'])
def start(m):
    ACTIVE_USERS.add(m.chat.id)
    bot.reply_to(m, "✅ Prediction चालू कर दिया गया है!\nहर 15 सेकंड में आपको Signal मिलेगा।\n\n🛑 बंद करने के लिए /stop भेजें")

@bot.message_handler(commands=['stop'])
def stop(m):
    ACTIVE_USERS.discard(m.chat.id)
    bot.reply_to(m, "🛑 आपने Prediction बंद कर दिया है।")

@bot.message_handler(commands=['predict'])
def manual_predict(m):
    try:
        text = m.text.replace('/predict', '').strip()
        nums = [float(x) for x in text.replace(',', ' ').split()]
        if len(nums) < 5:
            return bot.reply_to(m, "⚠️ कम से कम 5 multipliers दो।\nउदाहरण: /predict 1.5 2.3 5.6 10.0 2.1")
        result = predict_from_list(nums)
        bot.reply_to(m, f"📉 Manual Data: {nums[-5:]}\n\n🧠 Prediction: {result['message']}")
    except Exception as e:
        bot.reply_to(m, f"⚠️ Format ऐसा भेजो:\n/predict 1.5 2.0 3.1 10.0 5.4\n\nError: {e}")

@bot.message_handler(content_types=['photo'])
def handle_ocr(m):
    try:
        file_id = m.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open("img.jpg", 'wb') as f:
            f.write(downloaded)
        multipliers = read_multipliers_from_image("img.jpg")
        result = predict_from_list(multipliers)
        bot.reply_to(m, f"📸 OCR Read: {multipliers}\n📊 Prediction: {result['message']}")
    except Exception as e:
        bot.reply_to(m, f"❌ OCR Error: {e}")

def run_bot():
    global correct, total
    while True:
        try:
            data = get_live_data()
            if len(data) >= 5:
                result = predict_from_list(data)
                generate_graph(data[-10:], "graph.png")
                msg = f"""
📊 *Aviator Signal*

📉 Last: {data[-5:]}

🧠 Prediction: {result['message']}

🕒 Next Round: ⏳ 15 sec
✅ Accuracy: {correct}/{total}
"""
                if result['tag'] == "safe":
                    correct += 1
                total += 1
                for user in ACTIVE_USERS:
                    bot.send_photo(user, open("graph.png", "rb"))
                    bot.send_message(user, msg, parse_mode="Markdown")
            time.sleep(15)
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

import threading
threading.Thread(target=run_bot).start()
bot.infinity_polling()
