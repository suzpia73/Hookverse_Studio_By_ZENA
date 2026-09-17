try:
    from fontTools.ttLib import TTFont
    font = TTFont("assets/fonts/KyoboHand.woff")
    font.flavor = None
    font.save("assets/fonts/KyoboHandwriting2019.ttf")
    print("Successfully converted KyoboHand.woff to TTF!")
except Exception as e:
    print("Error:", e)
