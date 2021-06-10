from abc import ABC, abstractmethod
from imutils.object_detection import non_max_suppression
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np
import imutils
import cv2


class Detector(ABC):

    def __init__(self, path: str):
        self._path = path
        self._hog = cv2.HOGDescriptor()
        self._hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.stop = True

    @abstractmethod
    def get_tk_image(self):
        pass

    @abstractmethod
    def detect(self, panel: ttk.Label, text: tk.StringVar) -> None:
        pass

    def _image_to_tk_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image)

    def _single_frame_detect(self, image) -> list:
        (rects, _) = self._hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        result = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        return result


class ImageDetector(Detector):

    def __init__(self, path: str):
        super().__init__(path)
        self._image = cv2.imread(path)
        self._image = imutils.resize(self._image, width=min(800, self._image.shape[1]))

    def get_tk_image(self):
        return self._image_to_tk_image(self._image)

    def detect(self, panel: ttk.Label, text: tk.StringVar) -> None:
        result = []
        image = self._image.copy()

        result = self._single_frame_detect(image)

        for (xA, yA, xB, yB) in result:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        image = self._image_to_tk_image(image)
        panel.configure(image=image)
        panel.image = image
        text.set(str(len(result)))


class VideoDetector(Detector):

    def __init__(self, path: str):
        super().__init__(path)
        self._cap = cv2.VideoCapture(path)

    def get_tk_image(self):
        _, frame = self._cap.read()
        frame = imutils.resize(frame, width=min(800, frame.shape[1]))
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return self._image_to_tk_image(frame)

    def detect(self, panel: ttk.Label, text: tk.StringVar, force=True) -> None:
        if force:
            self.stop = False

        if not self.stop and self._cap is not None and self._cap.isOpened:
            ok, frame = self._cap.read()
        else:
            return

        if ok:
            frame = imutils.resize(frame, width=min(800, frame.shape[1]))
            result = self._single_frame_detect(frame.copy())
            for (xA, yA, xB, yB) in result:
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 1)
            frame = self._image_to_tk_image(frame)

            panel.configure(image=frame)
            panel.image = frame
            text.set(str(len(result)))

        panel.after(15, lambda: self.detect(panel, text, force=False))

    def close(self):
        if self._cap is not None and self._cap.isOpened():
            self._cap.release()
