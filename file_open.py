import sys
import tkinter as tk
from tkinter import Canvas, Label, Menu, PhotoImage, ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.messagebox import showerror, showwarning, showinfo
import os
from PyPDF2 import PdfReader, PdfWriter


def pdf_splitter(path):
    pdf = PdfReader(path)
    dir_name = 'Gambrinus'
    if not os.path.exists(f'{os.getcwd()}/{dir_name}'):
        os.mkdir(dir_name)
    for page_number in range(len(pdf.pages)):
        id = None
        date = None
        name = None
        writer = PdfWriter()
        writer.add_page(pdf.pages[page_number])
        page = pdf.pages[page_number].extract_text()
        lines = page.split('\n')
        lines = iter(lines)
        for line in lines:
            if "לכבוד" in line:
                name = next(lines)
            if "חופשה ללא תשלום לחודש" in line:
                date = (line.replace('/', '_')).split(" ")[0]
            if "תלוש שכר לחודש" in line:
                date = (line.replace('/', '_')).split(" ")[0]
            if "מספר זהות" in line:
                id = line.split(" ")[0]
        if date != None and id != None:
            if not os.path.exists(f'{os.getcwd()}/{dir_name}/{name}'):
                os.mkdir(f'{dir_name}/{name}')
            filename = f'{dir_name}/{name}/{id}_{date}.pdf'
            writer.encrypt(id)
            with open(filename, 'wb') as output:
                writer.write(output)
                writer.close()
        else:
            showerror('Gambrinus', 'cannot create PDF files.')
            sys.exit()


def is_pdf():
    global file_path
    file_path = filedialog.askopenfilename()
    file = file_path.lower().endswith(".pdf")
    if file:
        pdf_splitter(file_path)
        showinfo('Gambrinus', 'PDF split complete.')
        sys.exit()
    else:
        showerror("Gambrinus", "The selected file is not a PDF.")


file_path = ''
# create the root window
root = tk.Tk()
root.title('Gambrinus')
root.geometry("400x300")
root.resizable(False, False)
options = {'fill': 'both', 'padx': 10, 'pady': 10, 'ipadx': 5}

button = ttk.Button(root,
                    text='Open file',
                    command=is_pdf
                    ).pack(**options)
# run the app
root.mainloop()
