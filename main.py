from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import time

class App(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_file_button = Button(self, text="Dosya Seç", command=self.select_file, width=15, height=2,)
        self.select_file_button.pack(side="top", pady=10)

        self.analyze_button = Button(self, text="Analiz Et", state=DISABLED, command=self.analyze_image, width=15, height=2)
        self.analyze_button.pack(side="top", pady=10)

        self.loading_label = Label(self, text="Yükleniyor...")
        self.loading_label.pack_forget()

        self.quit_button = Button(self, text="Çık", command=self.master.destroy, width=15, height=2)
        self.quit_button.pack(side="top", pady=10)

        self.select_file_button.pack(anchor="n")
        self.analyze_button.pack(anchor="n")
        self.quit_button.pack(anchor="n")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.convert("RGB")
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_label = Label(image=self.image_tk)
            self.image_label.pack()
            self.analyze_button["state"] = NORMAL

    def analyze_image(self):
        self.loading_label.pack()
        self.select_file_button["state"] = DISABLED
        self.analyze_button["state"] = DISABLED

        t = threading.Thread(target=self.analyze_image_thread)
        t.start()

    def analyze_image_thread(self):
        width, height = self.image.size
        green_threshold = 0
        for x in range(width):
            for y in range(height):
                r, g, b = self.image.getpixel((x, y))
                if g > r + green_threshold and g > b + green_threshold:
                    self.image.putpixel((x, y), (255, 0, 0))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.image_tk)

        self.loading_label.pack_forget()
        self.select_file_button["state"] = NORMAL
        self.analyze_button["state"] = NORMAL

    def run(self):
        self.master.mainloop()

app = App(master=Tk())
app.run()
