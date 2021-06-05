from detection import ImageDetector, VideoDetector, Detector
from utils import read_ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import tkinter as tk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Video People Counter')
        self.geometry('1024x768')
        self.resizable(width=False, height=False)
        self.grid()
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.add_widgets()

        self._detector: Detector = None

    def add_widgets(self):
        self._panel = ttk.Label(master=self)
        self._panel.grid(row=0, column=0)

        button_frame = ttk.Frame(master=self)
        button_frame.grid(row=1, column=0, pady=15)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(master=button_frame, text='Select a video', width=70, command=self.load_video)\
            .grid(row=0, column=0, padx=19, pady=20)
        ttk.Button(master=button_frame, text='Select an image', width=70, command=self.load_image)\
            .grid(row=0, column=1, padx=19, pady=20)
        ttk.Button(master=button_frame, text='Detect people', width=148, command=self.start_detection)\
            .grid(row=1, column=0, columnspan=2)

    def load_video(self):
        video_path = askopenfilename(filetypes=[('Video Files', '.mp4')])
        if video_path is not None and len(video_path) > 0:
            self._detector = VideoDetector(video_path)

    def load_image(self):
        image_path = askopenfilename(filetypes=[('Image Files', '.jpg .jpeg .png')])
        if image_path is not None and len(image_path) > 0:
            image = read_ImageTk(image_path)
            self._detector = ImageDetector(image_path)
            self._panel.configure(image=image)
            self._panel.image = image

    def start_detection(self):
        if self._detector is not None:
            self._detector.detect(self._panel)


if __name__ == '__main__':
    app = App()
    app.mainloop()
