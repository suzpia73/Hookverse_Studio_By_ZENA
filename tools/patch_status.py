with open("_STATUS.md", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("1.8)*22px", "2.0)*25px")
text = text.replace("7.05 MB", "7.03 MB")
text = text.replace("5.57 MB", "7.03 MB")

with open("_STATUS.md", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated _STATUS.md successfully")
