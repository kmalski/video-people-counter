
from abc import ABC, abstractmethod
from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2


class Detector(ABC):

    def __init__(self):
        self._hog = cv2.HOGDescriptor()
        self._hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    @abstractmethod
    def detect(self, path: str) -> None:
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

    def __init__(self):
        super().__init__()

    def detect(self, path: str) -> None:
        result = []
        image = cv2.imread(path)
        image = imutils.resize(image, width=min(720, image.shape[1]))

        if len(image) <= 0:
            return

        result = self.single_frame_detect(image)

        for (xA, yA, xB, yB) in result:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class VideoDetector(Detector):

    def __init__(self):
        super().__init__()

    def detect(self, path: str) -> None:
        cap = cv2.VideoCapture(path)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame = imutils.resize(frame, width=min(400, frame.shape[1]))
            result = self.single_frame_detect(frame.copy())

            for (xA, yA, xB, yB) in result:
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv2.imshow("Video", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
