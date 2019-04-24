# Wildcard imports (from x import *) are discouraged in production code because they usually pollute global namespaces
# In this code wildcard import is used because it requires a lot of

from tkinter.filedialog import *


class Notepad:
    root = Tk()

    # Default window variables
    Width = 800
    Height = 600
    TextArea = Text(root)
    MenuBar = Menu(root)
    FileMenu = Menu(MenuBar, tearoff=0)
    EditMenu = Menu(MenuBar, tearoff=0)

    # Scrollbar
    ScrollBar = Scrollbar(TextArea)
    file = None

# "self" variable represents the instance of the object itself. "__init__" is the constructor for a class.
# "**" to group kwargs into a dictionary, where args are keys and their values are dictionary values.
    def __init__(self, **kwargs):

        # Setting size of window. Default is 400x700. You can change default by changing variables in lines 17-18
        try:
            self.Width = kwargs['width']
        except KeyError:
            pass

        try:
            self.Height = kwargs['height']
        except KeyError:
            pass

        # Setting window title
        self.root.title("Untitled - Notepad")

        # Changing icon. The file must be in the same directory as .py file of notepad
        self.root.iconbitmap(bitmap="@Noteicon.xbm")

        # Centering window
        screen_width = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()

        # Left, right, top and bottom align
        left = (screen_width / 2) - (self.Width / 2)
        right = (screen_height / 2) - (self.Height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.Width, self.Height, left, right))
        # {width} * {height} + {offset_x} + {offset_y}

        # Auto resize of text area
        # grid_columnconfigure(index, **options) column with the weight 2 will grow 2x faster than column with weight 1
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Scrollbar adjustment
        self.ScrollBar.config(command=self.TextArea.yview())
        self.TextArea.config(yscrollcommand=self.ScrollBar.set)

        # Functions of File Menu
        self.TextArea.grid(sticky=N + E + S + W)  # North, East, South, West

        # New file. "add_command (options)" adds a menu item to the menu.
        self.FileMenu.add_command(label="New file", command=self.new_file)

        # Open file
        self.FileMenu.add_command(label="Open file", command=self.open_file)

        # Save file
        self.FileMenu.add_command(label="Save file", command=self.save_file)

        # Separation in window dialog
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Exit", command=self.exit_notepad)
        # "add_cascade(options)" Creates a new hierarchical menu by associating a given menu to a parent menu
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        self.root.config(menu=self.MenuBar)
        self.ScrollBar.pack(side=RIGHT, fill=Y)

        # Functions of Edit Menu
        # Cut
        self.EditMenu.add_command(label="Cut", command=self.cut)

        # Copy
        self.EditMenu.add_command(label="Copy", command=self.copy)

        # Paste
        self.EditMenu.add_command(label="Paste", command=self.paste)

        # Edit
        self.MenuBar.add_cascade(label="Edit", menu=self.EditMenu)

    # New file
    def new_file(self):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.TextArea.delete(1.0, END)

    # Save file
    def save_file(self):
        # New file to save
        if self.file is None:  # If you are windows user delete or change /home to desired path
            self.file = asksaveasfilename(initialdir="/home", title="Save file",
                                          initialfile="Untitled.txt", defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"),  ("Text Documents", "*.txt")])

            if self.file == "":
                self.file = None
            else:   # Try to save
                file = open(self.file, "w")
                file.write(self.TextArea.get(1.0, END))
                file.close()

                # Change window title after save
                self.root.title(os.path.basename(self.file) + " - Notepad")

        else:
            file = open(self.file, "w")
            file.write(self.TextArea.get(1.0, END))
            file.close()

    # Open file
    def open_file(self):  # If you are windows user delete or change /home to desired path
        self.file = askopenfilename(initialdir="/home", title="Select file", defaultextension=".txt",
                                    filetypes=[("All Files", "*.*"),  ("Text Documents", "*.txt")])

        if self.file == "":  # If no file to open
            self.file = None
        else:  # Open file and set title to the window
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.TextArea.delete(1.0, END)
            file = open(self.file, "r")
            self.TextArea.insert(1.0, file.read())
            file.close()

    # Cut function
    def cut(self):
        self.TextArea.event_generate("<<Cut>>")

    # Copy function
    def copy(self):
        self.TextArea.event_generate("<<Copy>>")

    # Paste function
    def paste(self):
        self.TextArea.event_generate("<<Paste>>")

    # Notepad exit
    def exit_notepad(self):
        self.root.destroy()

    # Running main app
    def run(self):
        self.root.mainloop()


# Running main
notepad = Notepad(Width=800, Height=500)
notepad.run()
