def predict_from_list(data):
    high_count = sum(1 for x in data if x >= 10)
    low_streak = all(x < 2 for x in data[-3:])
    last = data[-1]

    if high_count >= 2 and not low_streak:
        return {"tag": "safe", "message": "✅ Safe Lagao! (High rounds दिखे हैं)"}
    elif low_streak:
        return {"tag": "avoid", "message": "🛑 3 बार लगातार low आया – Avoid करो!"}
    elif last >= 10:
        return {"tag": "neutral", "message": "⚠️ अभी 10x आया – अगला risky हो सकता है"}
    elif all(x < 2 for x in data):
        return {"tag": "avoid", "message": "🔴 सारे round low थे – Avoid!"}
    elif all(2 <= x < 5 for x in data):
        return {"tag": "medium", "message": "🟡 Medium trend चल रहा है – थोड़ा सावधान!"}
    else:
        return {"tag": "neutral", "message": "🟡 Pattern clear नहीं – Wait करो"}
