import os
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
import pyttsx3
import speech_recognition as sr

#File functions

def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)

def openfile():
    global file
    file = askopenfilename(defaulttextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])

    if file:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        with open(file, "r") as f:
            TextArea.insert(1.0, f.read())

def savefile():
    global file
    file = askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if not file:
        file = asksaveasfilename(initialfile="Untitiled.txt", defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    
    if file:
        with open(file, "w") as f:
            f.write(TextArea.get(1.0, END))
        root.title(os.path.basename(file) + " - Notepad")
        showinfo("Saved", "File saved successfully")

def quitApp():
    root.destroy()

# Edit functions

def cut():
    TextArea.event_generate("<<Cut>>")

def copy():
    TextArea.event_generate("<<Copy>>")

def paste():
    TextArea.event_generate("<<Paste>>")

def about():
    showinfo("Notepad", "Voice Enabled Notepad\nCreated using Python & Tkinter")

def tta():
    text = TextArea.get(1.0, END).strip()
    if text:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    else:
        showinfo("Empty", "No text to read")

def att():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            showinfo("Listening", "Speak now...")
            audio = r.listen(source)
            text = r.recognize_google(audio, language='en-IN')
            TextArea.insert(END, text + " ")
    except:
        showinfo("Error", "Could not recognize your voice")

# Main Application
root = Tk()
root.title("Untitled - Notepad")
root.geometry("700x600")

TextArea = Text(root, font="lucida 13")
TextArea.pack(expand=True, fill=BOTH)

file = None

# Menu Bar
MenuBar = Menu(root)

# File Menu
FileMenu = Menu(MenuBar, tearoff=0)
FileMenu.add_command(label="New", command=newFile)
FileMenu.add_command(label="Open", command=openfile)
FileMenu.add_command(label="Save", command=savefile)
FileMenu.add_separator()
FileMenu.add_command(label="Exit", command=quitApp)
MenuBar.add_cascade(label="File", menu=FileMenu)

# Edit Menu
EditMenu = Menu(MenuBar, tearoff=0)
EditMenu.add_command(label="Cut", command=cut)
EditMenu.add_command(label="Copy", command=copy)
EditMenu.add_command(label="Paste", command=paste)
MenuBar.add_cascade(label="Edit", menu=EditMenu)

# Voice Menu
VoiceMenu = Menu(MenuBar, tearoff=0)
VoiceMenu.add_command(label="Text to Speech", command=tta)
VoiceMenu.add_command(label="Speech to Text", command=att)
MenuBar.add_cascade(label="Voice", menu=VoiceMenu)

# Help Menu
HelpMenu = Menu(MenuBar, tearoff=0)
HelpMenu.add_command(label="About", command=about)
MenuBar.add_cascade(label="Help", menu=HelpMenu)
root.config(menu=MenuBar)

# Scrollbar
Scroll = Scrollbar(TextArea)
Scroll.pack(side=RIGHT, fill=Y)
Scroll.config(command=TextArea.yview)
TextArea.config(yscrollcommand=Scroll.set)

root.mainloop()

