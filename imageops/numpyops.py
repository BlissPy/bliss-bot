
from io import BytesIO

import skimage
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
