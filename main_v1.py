# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 12:47:13 2021

@author: deep.g
"""
#deep Gupta


from tkinter import Entry
from tkinter import Button
from tkinter import Checkbutton
from numpy import asarray
from tkinter import Tk
from tkinter import BooleanVar
from cv2 import imread
from cv2 import imwrite
from cv2 import split as cv2_split
from cv2 import merge
from os.path import split as os_split
from os.path import join
from os.path import basename
from os import listdir
from pickle import dump
from pickle import load

from glob import glob
from tkinter.messagebox import showerror



root = Tk()
root.title("Image lock")
root.geometry("300x200")  # Size of the window
enc_check_status = BooleanVar()
dec_check_status = BooleanVar()

folder_path_input = Entry(root, font=("Calibri",12), bd=2)
folder_path_input.configure(width=20)
folder_path_input.pack()
enc_checkbox = Checkbutton(root, 
                           text="Image Encryption", 
                           variable = enc_check_status,
                           onvalue=True,
                           offvalue=False)
enc_checkbox.pack()

dec_checkbox = Checkbutton(root, 
                           text="Image Decode", 
                           variable = dec_check_status,
                           onvalue=True,
                           offvalue=False)
dec_checkbox.pack()





def enc_image(image_file_path, enc_file_path):
    img = imread(image_file_path)
    rgb_dic = {}
    #cv2.imshow("img",img)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #cv2.imshow("img_BGR2RGB",img)
    #numpyarray = asarray(img)
    b,g,r = cv2_split(img)
    rgb_dic["b"] = b
    rgb_dic["g"] = g
    rgb_dic["r"] = r
    with open(enc_file_path, "wb") as image_file:
        dump(rgb_dic, image_file)
        
def dec_image(enc_file_path, image_file_path):
    rgb_load_dic ={}
    with open(enc_file_path, "rb") as image_file:
        rgb_load_dic = load(image_file)
    marge_img = merge((asarray(rgb_load_dic["b"]),asarray(rgb_load_dic["g"]),asarray(rgb_load_dic["r"])))
    imwrite(image_file_path, marge_img)
    
def get_folder_path(filepath):
    return os_split(filepath)[0]

def submit():
    img_root_folder = folder_path_input.get()
    if enc_check_status.get() == True and dec_check_status.get() == False:
        img_list = listdir(img_root_folder)
        for image in img_list:
            image_name_list = image.split(".")
            image_name = image_name_list[0]
            image_ext = image_name_list[1]
            print(image_name)
            print(image_ext)
            if image_ext != "wnc":
                image_file_path = join(img_root_folder, (image_name+(".")+image_ext))
                enc_file_path = join(img_root_folder, (image_name+".wnc"))
                print(image_file_path, enc_file_path)
                enc_image(image_file_path , enc_file_path)
            else:
                pass
    
    elif enc_check_status.get() == False and dec_check_status.get() == True:
        wnc_file_file_path = glob(join(img_root_folder,"*.wnc"))
        for wnc_file in wnc_file_file_path:
            wnc_name_list = basename(wnc_file).split(".")
            wnc_name = wnc_name_list[0]
            #wnc_ext = wnc_name_list[1]
            #print(wnc_name)
            #print(image_ext)
            img_file_path = join(get_folder_path(wnc_file), (wnc_name+".jpeg"))
            #print(image_file_path, enc_file_path)
            dec_image(wnc_file, img_file_path)
            
    elif enc_check_status.get() == False and dec_check_status.get() == False:
        showerror("Error", "Select enc or dec option")
    elif enc_check_status.get() == True and dec_check_status.get() == True:
        showerror("Error", "Select only one option")


submit_button = Button(root, text="Submit", command=submit)
submit_button.pack()
root.mainloop()
