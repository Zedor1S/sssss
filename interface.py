from tkinter import Frame, Button, Label, Entry, filedialog, Scale, HORIZONTAL
from filteringTopLevel import FilteringTopLevel
from adjustingTopLevel import AdjustingTopLevel
from PIL import Image
import numpy as np
import cv2


class Interface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg='gray', width=1280, height=100)

        self.music_label = Label(self, text="Гучність музики", bg='gray', font="ariel 11 bold")
        self.music_scale = Scale(self, from_=0.0, to_=1.0, length=100, resolution=0.01,
                                 orient=HORIZONTAL)
        self.music_scale.set(0.7)
        self.music_scale.bind("<ButtonRelease-1>", self.music_volume)

        self.new_button = Button(self, text="Відкрити", bg='gold', fg='black', width=10, font="ariel 13 bold")
        self.save_button = Button(self, text="Зберегти", bg='black', fg='gold', width=10, font="ariel 13 bold")
        self.save_as_button = Button(self, text="Зберегти як", bg="black", fg='yellow', width=10, font="ariel 13 bold")
        self.clear_button = Button(self, text="Очистити", bg="black", fg='yellow', width=10, font="ariel 13 bold")
        self.filter_button = Button(self, text="Фільтри", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.adjust_button = Button(self, text="Налаштувати", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.draw_button = Button(self, text="Малювати", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.crop_button = Button(self, text="Обрізати", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.rotate_button = Button(self, text="Оборот", bg="black", fg='white', width=5, font="ariel 8 bold")
        self.saveRotation_button = Button(self, text="Зберегти\nобертання", bg="black", fg='white', width=8,font="ariel 8 bold")
        self.rotate_label = Label(text="Кут повороту", font="Arial 8 bold")
        self.rotate_entry = Entry(width=15)
        self.addMoreImage_button = Button(self, text="Більше зображень\nдля вставлення",
                                          bg='red', fg='blue', width=15, font="ariel 12 bold")
        self.undo_button = Button(self, text="Назад", bg="blue", fg='white', width=6, font="ariel 13 bold")
        self.forward_button = Button(self, text="Вперед", bg="blue", fg='white', width=7, font="ariel 13 bold")
        self.flip_button = Button(self, text="Віддзеркал.", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.contrast_button = Button(self, text="Збільшити\nКонтраст", bg="black", fg='white', width=10,
                                      font="ariel 13 bold")

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.filter_button.bind("<ButtonRelease>", self.filter_button_released)
        self.adjust_button.bind("<ButtonRelease>", self.adjust_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)
        self.draw_button.bind("<ButtonRelease>", self.draw_button_released)
        self.undo_button.bind("<ButtonRelease>", self.undo_button_released)
        self.forward_button.bind("<ButtonRelease>", self.forward_button_released)
        self.crop_button.bind("<ButtonRelease>", self.crop_button_released)
        self.rotate_button.bind("<ButtonRelease>", self.rotate_button_released)
        self.saveRotation_button.bind("<ButtonRelease>", self.saveRotation_button_released)
        self.addMoreImage_button.bind("<ButtonRelease>", self.addMoreImage_button_released)
        self.flip_button.bind("<ButtonRelease>", self.flip_button_released)
        self.contrast_button.bind("<ButtonRelease>", self.contrast_button_released)

        self.new_button.place(x=0, y=0)
        self.save_button.place(x=0, y=45)
        self.save_as_button.place(x=120, y=45)
        self.music_label.place(x=1092, y=30)
        self.music_scale.place(x=1100, y=60)
        self.clear_button.place(x=120, y=0)
        self.filter_button.place(x=340, y=0)
        self.adjust_button.place(x=340, y=45)
        self.draw_button.place(x=460)
        self.crop_button.place(x=460, y=45)
        self.rotate_label.place(x=627)
        self.rotate_entry.place(x=620, y=25)
        self.rotate_button.place(x=605, y=45)
        self.saveRotation_button.place(x=660, y=45)
        self.addMoreImage_button.place(x=765)
        self.undo_button.place(x=765, y=55)
        self.forward_button.place(x=845, y=55)
        self.flip_button.place(x=960)
        self.contrast_button.place(x=960, y=45)

    def music_volume(self, event):
        self.master.mixer.music.set_volume(float(self.music_scale.get()))

    def check_status(self):
        if self.master.is_image_selected:
            if self.master.is_crop_state:
                self.master.interface_functions.deactivate_crop()
            if self.master.is_draw_state:
                self.master.interface_functions.deactivate_draw()
            if self.master.is_paste_state:
                self.master.interface_functions.deactivate_paste()
            return True
        return False

    def new_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            if self.master.is_draw_state:
                self.master.interface_functions.deactivate_draw()
            if self.master.is_crop_state:
                self.master.interface_functions.deactivate_crop()
            if self.master.is_paste_state:
                self.master.interface_functions.deactivate_paste()

            filename = filedialog.askopenfilename()
            image = cv2.cvtColor(np.array(Image.open(filename)), cv2.COLOR_BGR2RGB)

            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.interface_functions.show_image()
                self.master.is_image_selected = True
                self.master.num_rows, self.master.num_cols = self.master.processed_image.shape[:2]
                self.master.image_cache.append(self.master.processed_image.copy())

    def save_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            if self.check_status():
                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)

    def save_as_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            if self.check_status():
                original_file_type = self.master.filename.split('.')[-1]
                filename = filedialog.asksaveasfilename()
                filename = filename + "." + original_file_type

                save_image = self.master.processed_image
                cv2.imwrite(filename, save_image)

                self.master.filename = filename

    def filter_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            if self.check_status():
                self.master.filtering_frame = FilteringTopLevel(master=self.master)
                self.master.filtering_frame.grab_set()

    def adjust_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            if self.check_status():
                self.master.adjusting_frame = AdjustingTopLevel(master=self.master)
                self.master.adjusting_frame.grab_set()

    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            if self.check_status():
                self.master.image_cache.clear()
                self.master.interface_functions.forward_cache.clear()
                self.master.processed_image = self.master.original_image.copy()
                self.master.interface_functions.show_image()

    def draw_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.draw_button:
            if self.check_status():
                self.master.interface_functions.activate_draw()

    def undo_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.undo_button:
            self.master.interface_functions.undo_image()

    def forward_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.forward_button:
            self.master.interface_functions.forward_image()

    def crop_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button:
            if self.check_status():
                self.master.interface_functions.activate_crop()

    def rotate_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.rotate_button:
            if self.check_status():
                self.master.interface_functions.rotate(self.rotate_entry.get())

    def saveRotation_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.saveRotation_button:
            if self.check_status():
                self.master.processed_image = self.master.rotating_image

    def addMoreImage_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.addMoreImage_button:
            if self.check_status():
                filename = filedialog.askopenfilename()
                image = cv2.cvtColor(np.array(Image.open(filename)), cv2.COLOR_BGRA2RGBA)

                if image is not None:
                    self.master.more_imageFilename = filename
                    self.master.more_image = image.copy()
                    self.master.interface_functions.activate_paste()

    def flip_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.flip_button:
            if self.check_status():
                self.master.interface_functions.flipping()

    def contrast_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.contrast_button:
            if self.check_status():
                self.master.interface_functions.contrast()
