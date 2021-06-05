from PIL import Image, ImageTk
import cv2
import imutils


def read_ImageTk(image_path: str) -> ImageTk:
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = imutils.resize(image, width=min(800, image.shape[1]))
    image = Image.fromarray(image)
    return ImageTk.PhotoImage(image)
