# coding: utf-8
import os
import re
import base64
import platform
import subprocess
import threading
import tempfile
import tkinter as tk
from io import BytesIO
from pathlib import Path
from tkinter import filedialog, ttk, messagebox

from PIL import Image


ICON_BASE64 = '''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R/8AAAD/TUM5/6WPev+lj3r/pY96/6WPev+lj3r/pY96/6WPev+lj3r/pY96/6WPev+lj3r/pY96/0xCOP8AAAD/nIaH//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb/6qSk/8AAAD/QDd//4Bu//82Lmv/AAAA/wAAAEsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEsAAAD/Ni5r/4Bu//9AN3//AAAA/6uIiP/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv+YeXn/AAAA/0Y9NP+lj3r/pY96/6WPev+lj3r/pY96/6WPev+lj3r/pY96/6WPev+lj3r/pY96/6WPev9FOzP/AAAA/6KLjP/92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2/+qkpP/AAAA/0A3f/+Abv//Ni5r/wAAAP8AAABLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABLAAAA/zYua/+Abv//QDd//wAAAP+siYn//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr/5be3/w0KCv8BAQH/LCYh/zcwKf83MCn/NzAp/zcwKf83MCn/NzAp/zcwKf83MCn/NzAp/zcwKf8sJiH/AQEB/xEODv/ry8z//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv/q5OU/wAAAP9AN3//gG7//zYua/8AAAD/AAAASwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASwAAAP82Lmv/gG7//0A3gP8AAAD/rImJ//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv8pICD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8qJCT//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb/6uTlP8AAAD/QDeA/4Bu//82Lmv/AAAA/wAAAEsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEsAAAD/NS5q/4Bu//9AN4D/AAAA/6qHh//9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/OpaX/AAAA/xMlLf9YqtL/VqbM/1amzP9Wpsz/VqbM/1amzP9Wpsz/VKPJ/1amuv9Yrbn/XbbD/2XH1P8VKiz/AAAA/9G0tf/92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2/+pkZL/AAAA/0A3gP+Abv//NS5q/wAAAP8AAABLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA5AAAA/yQfSP+Abv//QTiB/wAAAP+jgoL//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr/TT4+/wAAAP89d5L/a8///2vP//9rz///a8///2vP//9rz///a8///23T//946/z/eOz8/3js/P947Pz/RIWO/wAAAP9PREX//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv/oouM/wAAAP9BOIH/gG7//yMeRv8AAAD/AAAAOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABgAAAeQAAAH/TEKY/z82ff8AAAD/nHx8//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr/l3h4/wAAAP8PHCP/aMn4/2vP//9rz///a8///2vP//9rz///a8///2vP//905f3/eOz8/3js/P947Pz/eOz8/3Tl9P8QHyL/AAAA/5mEhP/92tv//drb//3a2//92tv//drb//3a2//92tv//drb//3a2//92tv//drb/5uFhv8AAAD/PjV8/0xBl/8AAAH/AAAB4gAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABGAAAB+gAAAP8AAAH/AAAA/1hGRv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr//crK//3Kyv/9ysr/mHl5/wMCAv8DBgf/U6LH/2vP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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZgAAAOMAAABUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkAAABcAAAAnQAAAMYAAADlAAAA/gABAe8AAADsAAAAzQAAAKYAAABrAAAAHgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAAAA4wAAAGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////4Af////+Af4AAH+Af/wAAAAAAAAf+AAAAAAAAB/wAAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/wAAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/wAAAAAAAAD/AAAAAAAAAP+AAAAAAAAA/4AAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/wAAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/wAAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/wAAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/wAAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/wAAAAAAAAD/AAAAAAAAAP8AAAAAAAAA/4AAAAAAAAH/wAAAAAAAA//4AAAAAAAf//wAAAAAAD///8AAAAAD////8AAAAA/////wAAAAD////+AAAAAH////4AAAAAf////AAAAAA////8AAAAAD////wAAAAAP////AAAAAA////8AAAAAD//+HwAAAAAPh/4DAAAAAAwH/wEAAAAACA//wQAAAAAIP///AAAAAA////8AAAAAD////wAAAAAP////gAAAAB///+OAAAAAHH/+AYAAAAA4B/4BwAAAADgH/h/gAAAAf4f//+AAAAB/////8AAAA/////44AAADx////DwAAAPD///4PwAAD8H///B/gAAf4P//8f/wAP/4/8='''


def select_input_directory():
    directory_path = filedialog.askdirectory(title="Select Directory")
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        input_directory_var.set(directory_path)
        input_directory_label.config(foreground='#41b52d')
    else:
        show_message('Error', 'Please select a valid input directory with images.')


def select_output_directory():
    directory_path = filedialog.askdirectory(title="Select Directory")
    output_directory_var.set(directory_path)
    output_directory_label.config(foreground='#41b52d')


def select_settings_file():
    file_path = filedialog.askopenfilename(title="Select TXT File", filetypes=[("Text files", "*.txt")])
    if os.path.exists(file_path) and os.path.isfile(file_path):
        txt_file_var.set(file_path)
        txt_file_label.config(foreground='#41b52d')
    else:
        show_message('Error', 'Please select a valid text file')


def generate_settings():
    cwd = Path.cwd()
    input_dir = Path(input_directory_var.get())
    if input_dir.exists() and input_dir.is_dir():
        images = list(input_dir.glob('*.png')) + list(input_dir.glob('*.jpg')) + list(input_dir.glob('*.jpeg'))

        if len(images) == 0:
            show_message("Error", "Please select input directory that contain at least 1 image")
            return

        with open('settings.txt', 'w') as settings_file:
            for img_path in images:
                settings_file.write(f'{img_path.name}: 0\n')

        notepad_process = subprocess.Popen(['notepad.exe', 'settings.txt'])

        txt_file_var.set('settings.txt')
        txt_file_label.config(foreground='#41b52d')
    else:
        messagebox.showerror("Error", "Please select a valid directory first")


def create_image(img1_path, img2_path, rot1, rot2, result_path):
    # Define result image path
    result_image_path = f'{result_path}/{Path(img1_path).stem}_{Path(img2_path).stem}.png'

    # Open images
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Rotate images
    img1_rotated = img1.rotate(rot1, expand=True)
    img2_rotated = img2.rotate(rot2, expand=True)

    # Calculate the size of the new image
    width = max(img1_rotated.size[0], img2_rotated.size[0])
    height = img1_rotated.size[1] + img2_rotated.size[1]

    # Create a new image with the calculated size
    result_image = Image.new("RGB", (width, height), (32, 34, 37))  # Dark background

    # Paste the rotated images onto the new image
    result_image.paste(img1_rotated, (0, 0))
    result_image.paste(img2_rotated, (0, img1_rotated.height))

    # Remove previous image version if exists
    if os.path.exists(result_image_path):
        os.remove(result_image_path)

    # Save or display the result
    result_image.save(result_image_path)


def image_combine_task(input_directory_path, output_directory_path, txt_file_path):

    errors = []
    # Check if input path is existing directory
    if (
            input_directory_path == ''
            or not os.path.isdir(input_directory_path)
            or not os.path.exists(input_directory_path)
    ):
        errors.append('input folder')
    if output_directory_path == '' or not os.path.isdir(output_directory_path):
        errors.append('output folder')
    if txt_file_path == '' or not os.path.isfile(txt_file_path):
        errors.append('txt file with settings')

    if len(errors) > 0:
        root.after(50, show_message, 'Error', f'Please select correct: {", ".join(errors)}')
        return

    # Create output directory if not exists
    if not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)

    # Perform your task here, for example, counting lines in the text file
    with open(txt_file_path, 'r') as f:
        lines = f.readlines()
        lines = [l for l in lines if ':' in l]
        settings = []
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                settings.append(parts)

        # Check if the number of lines in the text file is odd
        if len(settings) % 2 != 0:
            # Create an additional image with the same size as 1.png
            odd_image_path = f'{input_directory_path}/{len(settings) + 1}.png'
            img1_path = f'{input_directory_path}/1.png'

            # Create a new white image with the size of img1
            img1_size = Image.open(img1_path).size
            odd_image = Image.new("RGB", img1_size, (255, 255, 255))
            odd_image.save(odd_image_path)

            settings.append([f'{len(settings) + 1}.png', settings[0][1]])

        total_steps = len(settings) // 2
        root.after(50, update_max_progress, total_steps)

        created_imgs = 0
        for idx in range(total_steps):
            files_ok = True
            setting1 = settings[idx]
            setting2 = settings[-1 - idx]
            if len(setting1) == 2 and len(setting2) == 2:
                fn1, rot1 = setting1
                rot1 = re.findall(r'\d+', rot1)

                fn2, rot2 = setting2
                rot2 = re.findall(r'\d+', rot2)

                if len(fn1) >= 1 and len(rot1) >= 1 and len(fn2) >= 1 and len(rot2) >= 1:
                    fn1 = f'{input_directory_path}/{fn1}'
                    rot1 = int(rot1[0])
                    fn2 = f'{input_directory_path}/{fn2}'
                    rot2 = int(rot2[0])

                    if not os.path.exists(fn1) or not os.path.isfile(fn1):
                        errors.append(
                            f'{fn1} from a settings file is not a real existing file, thus {fn1} & {fn2} were skipped'
                        )
                        files_ok = False
                    if not os.path.exists(fn2) or not os.path.isfile(fn2):
                        errors.append(
                            f'{fn2} from a settings file is not a real existing file, thus {fn1} & {fn2} were skipped'
                        )
                        files_ok = False

                    if files_ok:
                        create_image(
                            img1_path=fn1, img2_path=fn2, rot1=rot1, rot2=rot2, result_path=output_directory_path
                        )
                        created_imgs += 1

            root.after(50, update_progress, idx + 1)
        msg = f'{total_steps * 2} images were combined into {created_imgs} images\n'

        if len(errors) > 0:
            msg += '\n'.join(errors)

        root.after(
            50,
            show_message,
            'Task completed',
            msg
        )
        root.after(50, set_task_completed, 'image_combination')


def perform_task():

    # Check if task is not already running
    if is_image_combination_running.get():
        show_message('Error', 'Please wait for previous image combination task to complete')
        return

    input_directory_path = input_directory_var.get()
    output_directory_path = output_directory_var.get()
    txt_file_path = txt_file_var.get()

    image_combine_task_thread = threading.Thread(
        target=image_combine_task,
        args=(input_directory_path, output_directory_path, txt_file_path)
    )

    is_image_combination_running.set(True)

    image_combine_task_thread.start()


def update_max_progress(value):
    progress_bar['maximum'] = value


def update_progress(value):
    # Update the progress bar value
    progress_var.set(value)
    progress_label_var.set(f'{value/progress_bar["maximum"] :.2%}')
    root.update_idletasks()


def show_message(title, msg):

    popup = tk.Toplevel(root)
    popup.title(title)

    label = tk.Label(popup, text=msg)
    label.pack(padx=10, pady=10)

    # Adding a button to close the pop-up
    close_button = tk.Button(popup, text="Close", command= lambda: close_message(popup))
    close_button.pack(pady=10)

    # Wait until the pop-up is destroyed
    popup.wait_window()


def close_message(popup):
    closed_message_title = popup.title()

    # Destroy the pop-up
    popup.destroy()

    if closed_message_title == 'Task completed':
        system = platform.system()
        directory_path = output_directory_var.get()

        if system == "Windows":
            subprocess.run(["start",  directory_path], shell=True)
        elif system == "Darwin":
            subprocess.run(["open", directory_path])
        elif system == "Linux":
            subprocess.run(["xdg-open", directory_path])
        else:
            print("Unsupported operating system")


def set_task_completed(task_name):
    if task_name == "image_combination":
        is_image_combination_running.set(False)


def base64_to_icon(base64_image):
    image_data = base64.b64decode(base64_image)
    img = Image.open(BytesIO(image_data))

    temp_dir = os.path.join(os.path.abspath(tempfile.gettempdir()), 'IronEvaBooKGen')
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    icon_path = os.path.join(temp_dir, 'icon.ico')
    img.save(icon_path, format="ICO")
    return icon_path


if __name__ == "__main__":

    # Create the main window
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry('1280x200')
    root.title("IronEva Book Creator")

    # Configure dark theme
    root.configure(bg='#282C34')  # Previous background color

    # Add window icon
    root.iconbitmap(base64_to_icon(ICON_BASE64))

    # Styles
    style = ttk.Style()

    # Button Style
    style.configure('TButton', padding=(5, 5, 5, 5), font=('Arial', 12), background='#202124', foreground='#000000')  # Previous tone

    # Entry Style
    style.configure('TEntry', padding=(5, 5, 5, 5), font=('Arial', 12), background='#2C3E50', foreground='#000000')  # Current color

    # Label Style
    style.configure('TLabel', padding=(5, 5, 5, 5), font=('Arial', 12), background='#121417', foreground='#ECF0F1')  # Previous background color

    # Progressbar Style
    style.configure('TProgressbar', thickness=45, troughcolor='#3a5e34', background='#282C34') #34495E  # Previous tone

    txt_file_var = tk.StringVar()
    input_directory_var = tk.StringVar()
    output_directory_var = tk.StringVar()
    progress_var = tk.DoubleVar()
    progress_label_var = tk.StringVar()
    # Variable to trek if image combination task is running
    is_image_combination_running = tk.BooleanVar()

    # ## GUI Elements ## #

    # Frame for a control elements
    controls_frame = tk.Frame(root, height=200, background='#121417')
    controls_frame.pack(side="top", fill="x", pady=10, padx=10)

    output_directory_label = ttk.Label(controls_frame, text="Output:", style='TLabel')
    output_directory_label.place(x=0, y=5)

    output_directory_entry = ttk.Entry(controls_frame, textvariable=output_directory_var, width=165, style='TEntry')
    output_directory_entry.place(x=100, y=7)

    output_directory_button = ttk.Button(controls_frame, text="Set Output", command=select_output_directory, style='TButton')
    output_directory_button.place(x=1130, y=5)

    input_directory_label = ttk.Label(controls_frame, text="Input:", style='TLabel')
    input_directory_label.place(x=0, y=53)

    input_directory_button = ttk.Button(controls_frame, text="Browse Images", command=select_input_directory, style='TButton')
    input_directory_button.place(x=100, y=50)

    txt_file_label = ttk.Label(controls_frame, text="Settings File:", style='TLabel')
    txt_file_label.place(x=300, y=53)

    txt_file_button = ttk.Button(controls_frame, text="Browse Settings", command=select_settings_file, style='TButton')
    txt_file_button.place(x=450, y=50)

    generate_settings_button = ttk.Button(controls_frame, text="Generate Settings", command=generate_settings, style='TButton')
    generate_settings_button.place(x=650, y=50)

    static_label = ttk.Label(controls_frame, text="Progress:", style='TLabel')
    static_label.place(x=0, y=105)

    progress_bar = ttk.Progressbar(controls_frame, variable=progress_var, length=900, mode='determinate', style='TProgressbar')
    progress_bar.place(x=100, y=110)

    progress_label = ttk.Label(controls_frame, textvariable=progress_label_var, style='TLabel')
    progress_label.place(x=1000, y=100)

    task_button = ttk.Button(controls_frame, text="Combine Images", command=perform_task, style='TButton')
    task_button.place(x=1120, y=100)


    # Start the Tkinter event loop
    root.mainloop()
