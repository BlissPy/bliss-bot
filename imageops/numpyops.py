
from io import BytesIO

import skimage
import skimage.transform
import numpy as np
from PIL import Image
from skimage import io


async def bytes_to_np(img_bytes: BytesIO):
    ret = skimage.io.imread(img_bytes)
    return ret


async def np_to_bytes(img_bytes: BytesIO):
    pil = Image.fromarray(img_bytes)
    b = BytesIO()
    pil.save(b, format="png")
    pil.close()
    b.seek(0)
    return b


def _sort(img: np.ndarray):
    shape = img.shape

    img = img.reshape((img.shape[0] * img.shape[1], img.shape[2]))
    img.sort(0)

    return img.reshape(shape)


_ascii_characters = {
    0: " ", 1: ".", 2: "'", 3: "`",
    4: "^", 5: "\"", 6: ",", 7: ":",
    8: ";", 9: "I", 10: "1", 11: "!",
    12: "i", 13: ">", 14: "<", 15: "~",
    16: "+", 17: "?", 18: "]", 19: "[",
    20: "}", 21: "{", 22: "]", 23: "[",
    24: "|", 25: "/", 26: "\\", 27: "t",
    28: "x", 29: "n", 30: "u", 31: "v",
    32: "z", 33: "X", 34: "Y", 35: "U",
    36: "J", 37: "C", 38: "L", 39: "Q",
    40: "0", 41: "O", 42: "Z", 43: "#",
    44: "M", 45: "W", 46: "&", 47: "8",
    48: "%", 49: "B", 50: "@", 51: "@"
}


def _ascii_art(img: np.ndarray):
    # this was normalization but idk if i like it
    # img += int(255 / img.max())

    print()

    ascii_art = ""

    for i_row in range(0, img.shape[0], 2):
        row = img[i_row]
        ascii_art += "\n"
        for col in row:
            avg = int(col[0] + col[1] + col[2])
            avg = int(avg / 3)
            ascii_art += _ascii_characters[int(avg / 5)]

    return ascii_art
