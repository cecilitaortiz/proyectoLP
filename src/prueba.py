from tkinter import Tk
from tkcode import CodeEditor

root = Tk()
editor = CodeEditor(root, language="csharp")
editor.pack(fill="both", expand=True)
root.mainloop()