with open("assets/fonts/KyoboHandwriting2019.ttf", "rb") as f:
    data = f.read()

for term in [b"Kyobo", b"KyoboHandwriting", b"Handwriting"]:
    pos = 0
    while True:
        idx = data.find(term, pos)
        if idx == -1 or pos > 100000: break
        print(f"Found {term} at {idx}:", data[idx:idx+40])
        pos = idx + len(term)
        if pos > 20000: break
