import os
from PIL import Image

def boardpaint(frames):
    h = len(frames[0])
    w = len(frames[0][0])
    pic = Image.new(mode="RGBA", size=(w*100, h*100))
    os.chdir("Tiles")
    soccer = Image.open("soccer.png")
    basket = Image.open("basket.png")
    base = Image.open("base.png")
    beach = Image.open("beach.png")
    tennis = Image.open("tennis.png")
    white = Image.open("white.png")
    x = [soccer, basket, base, beach, tennis, white]
    num = 0
    os.chdir("..")
    os.chdir("source_images")
    for board in frames:
        for i in range(h):
            for j in range(w):
                pic.paste(x[board[i][j]],(100*j,100*i))
        pic.save(f"{num}.png",format="PNG")
        num += 1
    os.chdir("..")










