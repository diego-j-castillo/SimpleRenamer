import argparse
import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# changes the name of the file in the path to the new one
def seqRename(path, prevname, newname):
    extension = prevname[prevname.rindex('.'):].lower()
    srcname = prevname[0:prevname.rindex('.')] + extension
    try:
        os.rename(
            path + '/' + srcname,
            path + '/' + newname + extension.lower())
    except:
    #name the copy with a number suffixed, from 1 going up
        copyindex = 1
        attempt = newname + str(copyindex) + extension
        while attempt != srcname:
            try:
                os.rename(
                    path + '/' + srcname,
                    path + '/' + attempt)
                break
            except:
                copyindex = copyindex + 1
                attempt = newname + str(copyindex) + extension                   

# Class for SimpleRenamer window 
class SimpleRenamer:

    def __init__(self, window, path, filter):
        self.window = window
        self.path = path
        self.filter = filter
        self.index = 0
        
        #filter self.imagelist
        self.imagelist = []
        templist = []
        if self.filter is not None:
            for file in os.listdir(self.path):
                if self.filter.lower() in file.lower():
                    templist.append(file)
        else:
            templist = os.listdir(self.path)
            for file in templist:
                if file.lower().endswith('.png') or file.lower().endswith('.jpg'):
                    self.imagelist.append(file)
                    
        #starting the GUI
        frame = ttk.Frame(self.window, padding='10')
        frame.grid(column=0, row=0)

        #label for displaying the previous name of the image
        self.prevname = StringVar(value=self.imagelist[self.index])
        prevlabel = ttk.Label(frame, font='Courier 20', textvariable=self.prevname)
        prevlabel.grid(column=1, row=1, columnspan=2, sticky=(N))
        
        #label for displaying the image itself
        image = Image.open(args.path + self.imagelist[self.index])
        self.dispimage = ImageTk.PhotoImage(
            image.resize((int(image.width * 500 / image.height), 500)))
        self.imagelabel = ttk.Label(frame, image=self.dispimage)
        self.imagelabel.grid(column=1, row=2, columnspan=2, sticky=(N))

        #entry and button for renaming
        self.newname = StringVar()
        namer = ttk.Entry(frame, font='Courier 20', textvariable=self.newname)
        namer.grid(column=1, row=3, sticky=(E, W))
        nextbutton = ttk.Button(frame, text='Rename', default='active', command=self.enterpress)
        nextbutton.grid(column=2, row=3, sticky=(N, S, E, W))
        namer.focus()
        self.window.bind('<Return>', lambda e: nextbutton.invoke())
        self.window.bind('<Escape>', self.escpress)       

    #handles pressing enter
    def enterpress(self, *args):
        extension = self.prevname.get()[self.prevname.get().rindex('.'):]
        #only rename if entry box not blank
        if self.newname.get() != '' and self.newname.get() != self.prevname.get():
            seqRename(self.path, self.prevname.get(), self.newname.get())
            '''try:
                os.rename(
                    self.path + '/' + self.imagelist[self.index],
                    self.path + '/' + self.newname.get() + extension)
            except:
                return    '''               
        #move on to the next image, if possible
        if self.index == len(self.imagelist) - 1:
            self.window.destroy()
        else:
            self.index = self.index + 1
            self.prevname.set(self.imagelist[self.index])
            image = Image.open(self.path + self.prevname.get())
            self.dispimage = ImageTk.PhotoImage(
                image.resize((int(image.width * 500 / image.height), 500)))
            self.imagelabel.configure(image=self.dispimage)
            self.newname.set('')

    #handles pressing esc by closing window
    def escpress(self, *args):
        self.window.destroy()

if __name__ == '__main__':
    #parsing arguments and show usage
    parser = argparse.ArgumentParser(
        usage='SimpleRenamer.py [-h] directory_path [-f filter]',
        description='A Python tool to easily rename images')
    parser.add_argument('path', 
        metavar='directory_path',
        help='path to folder/directory where images are located')
    parser.add_argument('-f', type=str,
        metavar='filter',
        dest='filter',
        help='only rename files that include given string')
    args = parser.parse_args()
    
    #starts up the tool
    window = Tk(className='Renamer')
    SimpleRenamer(window, args.path, args.filter)
    window.mainloop()
