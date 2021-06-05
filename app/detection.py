
from abc import ABC, abstractmethod
from imutils.object_detection import non_max_suppression
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import imutils
import cv2


class Detector(ABC):

    def __init__(self, path: str):
        self._path = path
        self._hog = cv2.HOGDescriptor()
        self._hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    @abstractmethod
    def detect(self, panel: ttk.Label) -> None:
        pass

    def single_frame_detect(self, image):
        clone = image.copy()

        (rects, _) = self._hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        for (x, y, w, h) in rects:
            cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 0, 255), 2)

        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        result = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        return result


class ImageDetector(Detector):

    def __init__(self, path: str):
        super().__init__(path)

    def detect(self, panel: ttk.Label) -> None:
        result = []
        image = cv2.imread(self._path)
        image = imutils.resize(image, width=min(800, image.shape[1]))

        if len(image) <= 0:
            return

        result = self.single_frame_detect(image)

        for (xA, yA, xB, yB) in result:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panel.configure(image=image)
        panel.image = image


class VideoDetector(Detector):

    def __init__(self, path: str):
        super().__init__(path)

    def detect(self, panel: ttk.Label) -> None:
        cap = cv2.VideoCapture(self._path)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame = imutils.resize(frame, width=min(400, frame.shape[1]))
            result = self.single_frame_detect(frame.copy())

            for (xA, yA, xB, yB) in result:
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # TODO: add frame to passed panel arg
