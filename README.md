# SimpleRenamer
Python tool to easily rename images

## Python Dependencies
To run using python3, the folowing packages are used:
- Tkinter
- Pillow

## Usage
`SimpleRenamer.py directory_path [-f filter]`

`directory_path`: path to the directory/folder where the images are located			
`-f filter`: only rename files that include given string `filter`

### Interface
The interface is organized into 3 sections: the previous filename, the current image, and the new name entry. 

Entering a new name does not require entering the file extension. Pressing `Enter` will rename the current file, clear the name entry box, and open the next image to be renamed. If `Enter` is pressed when the name entry box is empty, the previous name will be kept. 

Once all images have been renamed, the program will close.