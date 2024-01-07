from tkinter import Toplevel, Button, RIGHT
import numpy as np
import cv2
from PIL import Image
from PIL.ImageFilter import (
    CONTOUR, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES
)


class FilteringTopLevel(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None
        self.title("Фільтри")
        self.geometry("250x400")

        self.negative_button = Button(self, text="Negative", width=12, font="ariel 11 bold")
        self.black_white_button = Button(self, text="Black White", width=12, font="ariel 11 bold")
        self.sepia_button = Button(self, text="Sepia", width=12, font="ariel 11 bold")
        self.emboss_button = Button(self, text="Emboss", width=12, font="ariel 11 bold")
        self.median_blur_button = Button(self, text="Blur", width=12, font="ariel 11 bold")
        self.edges_button = Button(self, text="Edges of Photo", width=12, font="ariel 11 bold")
        self.foilPic_button = Button(self, text="Foil Art", width=12, font="ariel 11 bold")
        self.pencilPic_button = Button(self, text="Sharp Paint", width=12, font="ariel 11 bold")
        self.oilPic_button = Button(self, text="Oil Paint", width=12, font="ariel 11 bold")
        self.sketchPic_button = Button(self, text="Sketch Light", width=12, font="ariel 11 bold")
        self.cancel_button = Button(self, text="Скасувати", width=7, font="ariel 8 bold")
        self.apply_button = Button(self, text="Зберегти", width=7, font="ariel 8 bold")

        self.negative_button.bind("<ButtonRelease>", self.negative_button_released)
        self.black_white_button.bind("<ButtonRelease>", self.black_white_released)
        self.sepia_button.bind("<ButtonRelease>", self.sepia_button_released)
        self.emboss_button.bind("<ButtonRelease>", self.emboss_button_released)
        self.median_blur_button.bind("<ButtonRelease>", self.median_blur_button_released)
        self.edges_button.bind("<ButtonRelease>", self.edges_button_released)
        self.foilPic_button.bind("<ButtonRelease>", self.foilPic_button_released)
        self.pencilPic_button.bind("<ButtonRelease>", self.pencilPic_button_released)
        self.oilPic_button.bind("<ButtonRelease>", self.oilPic_button_released)
        self.sketchPic_button.bind("<ButtonRelease>", self.sketchPic_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.negative_button.place(x=60, y=0)
        self.black_white_button.place(x=60, y=35)
        self.sepia_button.place(x=60, y=70)
        self.emboss_button.place(x=60, y=105)
        self.median_blur_button.place(x=60, y=140)
        self.edges_button.place(x=60, y=175)
        self.foilPic_button.place(x=60, y=210)
        self.pencilPic_button.place(x=60, y=245)
        self.oilPic_button.place(x=60, y=280)
        self.sketchPic_button.place(x=60, y=315)
        self.cancel_button.place(x=0, y=375)
        self.apply_button.place(x=193, y=375)

    def negative_button_released(self, event):
        self.negative()
        self.show_image()

    def black_white_released(self, event):
        self.black_white()
        self.show_image()

    def sepia_button_released(self, event):
        self.sepia()
        self.show_image()

    def emboss_button_released(self, event):
        self.emboss()
        self.show_image()

    def median_blur_button_released(self, event):
        self.median_blur()
        self.show_image()

    def edges_button_released(self, event):
        self.edges()
        self.show_image()

    def foilPic_button_released(self, event):
        self.foilPic()
        self.show_image()

    def pencilPic_button_released(self, event):
        self.pencilPic()
        self.show_image()

    def oilPic_button_released(self, event):
        self.oilPic()
        self.show_image()

    def sketchPic_button_released(self, event):
        self.sketchPic()
        self.show_image()

    def apply_button_released(self, event):
        self.master.image_cache.append(self.master.processed_image.copy())
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.interface_functions.show_image()
        self.close()

    def show_image(self):
        self.master.interface_functions.show_image(image=self.filtered_image)

    def negative(self):
        self.filtered_image = cv2.bitwise_not(self.original_image)

    def black_white(self):
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2RGB)

    def sepia(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def emboss(self):
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def median_blur(self):
        self.filtered_image = cv2.medianBlur(self.original_image, 41)

     
    def foilPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(EMBOSS))

    def pencilPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(EDGE_ENHANCE_MORE))

    def oilPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(EDGE_ENHANCE))

    def sketchPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(CONTOUR))

    def close(self):
        self.destroy()
