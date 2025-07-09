def predict_from_multipliers(multipliers):
    last = multipliers[-1]
    if float(last) < 2 and multipliers.count('✈️ Safe') < 2:
        return '🟢✈️ Safe - 3x तक जा सकता है!'
    elif float(last) < 1.5:
        return '🟡⚠️ Medium - संभल कर!'
    else:
        return '🔴🚫 Avoid - Crash जल्दी होगा!'
