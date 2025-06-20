# prueba.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.Qsci import QsciScintilla, QsciLexerCSharp

class EditorCSharp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor C# con PyQt5 + QScintilla")
        self.setGeometry(100, 100, 900, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Editor Scintilla
        self.editor = QsciScintilla()
        self.editor.setUtf8(True)
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")  # Ajusta según el número de líneas esperado

        # Lexer para C#
        lexer = QsciLexerCSharp()
        lexer.setDefaultFont(self.editor.font())
        self.editor.setLexer(lexer)

        layout.addWidget(self.editor)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = EditorCSharp()
    ventana.show()
    sys.exit(app.exec_())