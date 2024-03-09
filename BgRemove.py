import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Label
from tkinter import Button
from PIL import Image, ImageTk
import os
from rembg import remove
import time
import winreg
import sys
class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry('300x300')
        self.root.resizable(False, False)
        if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader extends the sys module by a flag frozen=True and sets the app path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(application_path, 'icon.ico')
        self.root.iconbitmap(icon_path)

        # Button to choose image
        self.info = tk.Label(root, text='Select image to background remove')
        self.info.pack(side='top', pady='1',fill = 'x')
        self.file_path = None
        self.filename = 'bg-remove_1.png'
        # Frame for Buttons 
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(side='top', fill='x', expand=True)

        self.close_button = tk.Button(self.buttons_frame, text="x",command = self.del_in)
        self.close_button.pack(side='left', padx=(10, 0))

        self.select_button = tk.Button(self.buttons_frame, text="Select image", command=self.load_image)
        self.select_button.pack(side='left')  

        self.removebg_button = tk.Button(self.buttons_frame, text="Delete background", command=self.remove_bg)
        self.removebg_button.pack(side='right')

        # Label of file
        self.image_label = tk.Label(root, width=300, height=300,bg='light grey', borderwidth=2, relief='solid')
        self.image_label.pack(side = 'bottom')

    def load_image(self):
        # Choose file
        self.file_path = filedialog.askopenfilename(filetypes=[("Pliki obrazów", "*.jpg *.png *.webp")])
    
        # Display File i file path isnt empty
        if self.file_path:
            self.image = Image.open(self.file_path)

            # Create thumbnail of file
            self.image.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(self.image)

            # Update photo view
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

            # Restart label to blank
            self.info.config(text='')
            self.info.update_idletasks()

    def del_in(self):
        # Delete currently file
        self.file_path = None
        self.image_label.config(image = '')
        # Restart label to defoult
        self.info.config(text='Select image to background remove')

    def get_desktop_path_from_registry(self):
        # Get desktop path from reg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:
            desktop_path, _ = winreg.QueryValueEx(key, "Desktop")
        return desktop_path
    
    def remove_bg(self):
        if self.file_path:
            # Call proggress countdown
            self.root.after(1000, self.update_progress, 1)

            # Custom path and name config to each image
            desktop_path = self.get_desktop_path_from_registry()
            input_path = self.file_path
            base_filename = 'bg-removed'
            extension = '.png'
            self.output_path = self.generate_filename(desktop_path, base_filename, extension)

            # Removing background process
            input = Image.open(input_path)
            output = remove(input)
            output.save(self.output_path)
            time.sleep(1)
        else:
            # Updating info label when file_path is empty
            self.info.config(text= 'Select image to background remove')
            self.info.update_idletasks()

    

    def generate_filename(self, directory, base_filename, extension):
        # Start prefix value
        i = 1
        
        filename = f"{base_filename}_{i}{extension}"
        filepath = os.path.join(directory, filename)
        
        # Check if file already exists
        while os.path.exists(filepath):
            # If is add + 1 value to filename
            i += 1
            self.filename = f"{base_filename}_{i}{extension}"

            # Set filepath with generated name 
            filepath = os.path.join(directory, self.filename)
            
        return filepath
    
    def update_progress(self, step):
        # Fake loading list
        progress_texts = ['Progress', 'Progress.', 'Progress..', 'Progress...','Progress....']
        self.info.config(text=progress_texts[step])
        self.info.update_idletasks()

        # Counting from progress_texts
        if step < len(progress_texts) - 1:
            self.root.after(1000, self.update_progress, step + 1)
        else:

            # After counting show results and info label
            self.info.config(text='Done')
            time.sleep(0.3)
            image = Image.open(self.output_path)
            image.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
        
            messagebox.showinfo("information", f"The image has been saved to desktop as {self.filename}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()