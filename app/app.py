from tkinter.constants import N
from detection import ImageDetector, VideoDetector, Detector
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import tkinter as tk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Video People Counter')
        self.geometry('830x600')
        self.resizable(width=False, height=False)
        self.grid()
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.add_widgets()
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self._detector: Detector = None

    def add_widgets(self):
        self._panel = ttk.Label(master=self)
        self._panel.grid(row=0, column=0)
        self._count_var = tk.StringVar()

        counter_frame = ttk.Frame(master=self)
        counter_frame.grid(row=1, column=0)
        ttk.Label(counter_frame, text="Count:", font='Helvetica 12 bold')\
            .grid(row=0, column=0)
        ttk.Label(counter_frame, textvariable=self._count_var, font='Helvetica 12')\
            .grid(row=0, column=1)

        button_frame = ttk.Frame(master=self)
        button_frame.grid(row=2, column=0, pady=15)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(master=button_frame, text='Select a video', width=70, command=self.load_video)\
            .grid(row=0, column=0, padx=21, pady=(0, 20))
        ttk.Button(master=button_frame, text='Select an image', width=70, command=self.load_image)\
            .grid(row=0, column=1, padx=21, pady=(0, 20))
        ttk.Button(master=button_frame, text='Start detection', width=70, command=self.start_detection)\
            .grid(row=1, column=0, padx=21)
        ttk.Button(master=button_frame, text='Stop detection', width=70, command=self.stop_detection)\
            .grid(row=1, column=1, padx=21)

    def load_video(self):
        video_path = askopenfilename(filetypes=[('Video Files', '.mp4 .mov .avi')])
        if video_path is not None and len(video_path) > 0:
            self._count_var.set("")
            self._detector = VideoDetector(video_path)
            frame = self._detector.get_tk_image()
            self._panel.configure(image=frame)
            self._panel.image = frame

    def load_image(self):
        image_path = askopenfilename(filetypes=[('Image Files', '.jpg .jpeg .png')])
        if image_path is not None and len(image_path) > 0:
            self._count_var.set("")
            self._detector = ImageDetector(image_path)
            image = self._detector.get_tk_image()
            self._panel.configure(image=image)
            self._panel.image = image

    def start_detection(self):
        if self._detector is not None and self._detector.stop:
            self._detector.detect(self._panel, self._count_var)

    def stop_detection(self):
        if self._detector is not None:
            self._detector.stop = True

    def on_close(self):
        if self._detector is not None:
            self._detector.stop = True
            try:
                self._detector.close()
            except:
                pass
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
