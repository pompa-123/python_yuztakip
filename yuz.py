import cv2
import tkinter as tk
from tkinter import PhotoImage
import random

class FaceTrackingApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        
        self.canvas = tk.Canvas(window, width=self.vid.get(3), height=self.vid.get(4))
        self.canvas.pack()

        self.btn_start = tk.Button(window, text="Başlat", width=10, command=self.start)
        self.btn_start.pack(padx=20, pady=10, side=tk.LEFT)

        self.btn_stop = tk.Button(window, text="Durdur", width=10, command=self.stop)
        self.btn_stop.pack(padx=20, pady=10, side=tk.LEFT)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        self.is_tracking = False
        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(6)]
        self.text_glasses = "Gözlüklü Patates"
        self.text_no_glasses = "Enes Batur Gerçek Kaza"

        self.update()

    def start(self):
        self.is_tracking = True
        self.vid = cv2.VideoCapture(self.video_source)
        self.update()

    def stop(self):
        self.is_tracking = False
        if self.vid.isOpened():
            self.vid.release()
        self.canvas.delete("all")

    def update(self):
        if self.is_tracking:
            ret, frame = self.vid.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    color = self.colors[random.randint(0, 5)]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    eyes = self.eyes_cascade.detectMultiScale(gray[y:y+h, x:x+w])
                    glasses = self.glasses_cascade.detectMultiScale(gray[y:y+h, x:x+w])

                    if len(glasses) > 0:
                        text = self.text_glasses
                    else:
                        text = self.text_no_glasses

                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                self.photo = PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes().decode('iso-8859-1'))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)
        self.window.update_idletasks()

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

root = tk.Tk()
app = FaceTrackingApp(root, "Yüz Takip Uygulaması")
root.mainloop()
