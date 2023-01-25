import argparse
import os
import tkinter as tk
from PIL import Image, ImageTk

#parsing arguments
parser = argparse.ArgumentParser(
    usage='SimpleRenamer.py directory_path [-f filter]',
    description='A Python tool to easily rename images')
parser.add_argument('path', 
    metavar='directory_path',
    help='path to folder/directory where images are located')
parser.add_argument('-f', type=str,
    metavar='filter',
    help='only rename files that include given string')
args = parser.parse_args()

#filter imagelist
imagelist = []
templist = []
if args.filter is not None:
    for file in os.listdir(args.path):
        if args.filter.lower() in file.lower():
            templist.append(file)
else:
    templist = os.listdir(args.path)
for file in templist:
    if file.endswith('.png') or file.endswith('.jpg'):
        imagelist.append(file)

#handles pressing enter
def enterpress(event):
    global index
    extension = imagelist[index][imagelist[index].rindex('.'):]
    if namer.get() != '':
        try:
            os.rename(
                args.path + '/' + imagelist[index],
                args.path + '/' + namer.get() + extension)
        except:
            print('file already exists')
            return
    if index == len(imagelist) - 1:
        window.destroy()
    else:
        index = index + 1
        image = Image.open(args.path + '/' + imagelist[index])
        global dispimage
        dispimage = ImageTk.PhotoImage(
            image.resize((int(image.width * 500 / image.height), 500)))
        imagelabel.configure(image=dispimage)
        prevlabel.configure(text=imagelist[index])
        namer.delete(0, tk.END)

#handles pressing esc by closing window
def escpress(event):
    window.destroy()

#starting the GUI
index = 0
window = tk.Tk(className='Renamer')
prevlabel = tk.Label(text=imagelist[index], font='Courier 20')
image = Image.open(args.path + '/' + imagelist[index])
dispimage = ImageTk.PhotoImage(
    image.resize((int(image.width * 500 / image.height), 500)))
imagelabel = tk.Label(image=dispimage)
namer = tk.Entry(window, width=20, font='Courier 20')
prevlabel.pack()
imagelabel.pack()
namer.pack()
namer.focus()
window.bind('<Return>', enterpress)
window.bind('<Escape>', escpress)
window.mainloop()
