import PySimpleGUI as sg
import os.path
from PIL import Image
import io
import base64


def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


# First the window layout in 2 columns
# sg.theme('Green Tan')
sg.theme('Dark Blue 14')
file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

prgress_text = sg.Text(f"0/0")
# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose a folder with images")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [prgress_text],
    [sg.Button("Has burst"), sg.Button("No burst"), sg.Button("Decide later")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout, font=("Helvetica",14))

# Run the Event Loop
idx = 0
num_of_images = 0

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".jpg"))
        ]
        num_of_images = len(fnames)
        window["-FILE LIST-"].update(fnames)

        filename = os.path.join(
            values["-FOLDER-"], fnames[idx]
        )
    window["-TOUT-"].update(filename)
    window["-IMAGE-"].update(data=convert_to_bytes(filename))

    prgress_text(f"{idx+1}/{num_of_images}")

    """
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=convert_to_bytes(filename))
        except Exception as E:
            print(f'** Error {E} **')
    """  
    # User pressed a button
    if event in ["Has burst", "No burst", "Decide later"]:
        if event == "Has burst":
            print("Labeled image = 1")

        if event == "No burst":
            print("Labeled image = 0")

        if event == "Decide later":
            print("Labeled image = -1")
        
        idx += 1
        filename = os.path.join(
            values["-FOLDER-"], fnames[idx]
        )
        #window["-TOUT-"].update(filename)
        #window["-IMAGE-"].update(data=convert_to_bytes(filename))

window.close()