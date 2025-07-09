import easyocr
reader = easyocr.Reader(['en'])

def read_multipliers_from_image(path):
    result = reader.readtext(path)
    values = []
    for (_, text, _) in result:
        try:
            if 'x' in text.lower():
                text = text.lower().replace('x', '')
            values.append(float(text.strip()))
        except:
            continue
    return values[-10:]
