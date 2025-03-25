import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image
import os


def image_to_ascii(img, width=100, fg_chars="@%#*+=-:. ", bg_char=" "):
    img = img.convert("L")
    aspect_ratio = img.height / img.width
    new_height = int(width * aspect_ratio * 0.55)
    img = img.resize((width, new_height))

    pixels = img.getdata()
    ascii_chars = [fg_chars[pixel * (len(fg_chars) - 1) // 255] for pixel in pixels]

    ascii_str = "".join(ascii_chars).replace(" ", bg_char)
    ascii_str = "\n".join(ascii_str[i:i + width] for i in range(0, len(ascii_str), width))

    return ascii_str


def print_plot_as_ascii(fig, width=100, fg_chars="@%#*+=-:. ", bg_char=" "):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor='none', dpi=100)
    buf.seek(0)

    img = Image.open(buf)
    ascii_art = image_to_ascii(img, width, fg_chars, bg_char)

    print(ascii_art)


if __name__ == "__main__":
    # plotting a heart for Terezka
    os.system("cls")
    os.system("title I Love You Terezkaaa")
    t = np.linspace(0, 2 * np.pi, 1000)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

    fig, ax = plt.subplots()
    ax.plot(x, y, color='black', linewidth=2)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_frame_on(False)
    ax.axis("off")

    print_plot_as_ascii(fig, width=80, fg_chars="▓▒░ ", bg_char=" ")

    # keep running without exiting
    # use ctrl+c to exit
    while True:
        pass