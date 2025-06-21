import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox, QTextEdit
)
from PyQt5.Qsci import QsciScintilla, QsciLexerCSharp
from lexer import lexer
from syntax import parser
from main import (
    analizar_lexico,
    guardar_log_lexico,
    analizar_sintactico,
    guardar_log_sintactico,
)

def listar_archivos_test():
    carpeta = "test"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    return [f for f in os.listdir(carpeta) if f.endswith(".cs")]

def cargar_archivo_test(nombre_archivo):
    ruta = os.path.join("test", nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

class AnalizadorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador Léxico de C#")
        self.setGeometry(100, 100, 1100, 600)

        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel izquierdo: Editor
        editor_layout = QVBoxLayout()
        main_layout.addLayout(editor_layout, 2)

        label = QLabel("Código fuente:")
        editor_layout.addWidget(label)

        self.editor = QsciScintilla()
        self.editor.setUtf8(True)
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")
        lexer = QsciLexerCSharp()
        lexer.setDefaultFont(self.editor.font())
        self.editor.setLexer(lexer)
        editor_layout.addWidget(self.editor)

        # Panel derecho: Resultados y controles
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, 1)

        # Botones de resultado
        botones_layout = QHBoxLayout()
        self.btn_tokens = QPushButton("Tokens")
        self.btn_tokens.clicked.connect(self.mostrar_tokens)
        self.btn_semantico = QPushButton("Semántico")
        self.btn_semantico.clicked.connect(self.mostrar_semantico)
        self.btn_sintactico = QPushButton("Sintáctico")
        self.btn_sintactico.clicked.connect(self.mostrar_sintactico)
        botones_layout.addWidget(self.btn_tokens)
        botones_layout.addWidget(self.btn_semantico)
        botones_layout.addWidget(self.btn_sintactico)
        right_layout.addLayout(botones_layout)

        # Áreas de resultados
        self.resultado_tokens = QTextEdit()
        self.resultado_tokens.setReadOnly(True)
        self.resultado_semantico = QTextEdit()
        self.resultado_semantico.setReadOnly(True)
        self.resultado_sintactico = QTextEdit()
        self.resultado_sintactico.setReadOnly(True)
        right_layout.addWidget(self.resultado_tokens)
        right_layout.addWidget(self.resultado_semantico)
        right_layout.addWidget(self.resultado_sintactico)
        self.resultado_semantico.hide()
        self.resultado_sintactico.hide()

        # Mensaje de log
        self.mensaje_log = QLabel("")
        right_layout.addWidget(self.mensaje_log)

        # Botones de acción
        acciones_layout = QHBoxLayout()
        btn_analizar = QPushButton("Analizar")
        btn_analizar.clicked.connect(self.analizar)
        btn_archivo = QPushButton("Analizar archivo de prueba")
        btn_archivo.clicked.connect(self.abrir_modal_archivos)
        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar)
        acciones_layout.addWidget(btn_analizar)
        acciones_layout.addWidget(btn_archivo)
        acciones_layout.addWidget(btn_limpiar)
        right_layout.addLayout(acciones_layout)

    def mostrar_tokens(self):
        self.resultado_tokens.show()
        self.resultado_semantico.hide()
        self.resultado_sintactico.hide()

    def mostrar_semantico(self):
        self.resultado_tokens.hide()
        self.resultado_semantico.show()
        self.resultado_sintactico.hide()

    def mostrar_sintactico(self):
        self.resultado_tokens.hide()
        self.resultado_semantico.hide()
        self.resultado_sintactico.show()
        # Analiza sintácticamente el código y muestra el resultado
        entrada = self.editor.text()
        resultado_sintactico = analizar_sintactico(entrada)
        self.resultado_sintactico.setPlainText("\n".join(resultado_sintactico))
        # Guarda el log sintáctico
        guardar_log_sintactico(resultado_sintactico)

    def analizar(self):
        entrada = self.editor.text()
        try:
            # Análisis léxico
            resultado_lexico = analizar_lexico(entrada)
            self.resultado_tokens.setPlainText("\n".join(resultado_lexico))
            log_path_lexico = guardar_log_lexico(resultado_lexico)
            # Análisis sintáctico
            resultado_sintactico = analizar_sintactico(entrada)
            self.resultado_sintactico.setPlainText("\n".join(resultado_sintactico))
            log_path_sintactico = guardar_log_sintactico(resultado_sintactico)
            self.mensaje_log.setText(
                f"✅ Logs guardados:\nLéxico: '{log_path_lexico}'\nSintáctico: '{log_path_sintactico}'"
            )
            self.mostrar_tokens()
        except Exception as e:
            self.mensaje_log.setText(f"❌ Error: {str(e)}")

    def limpiar(self):
        self.editor.setText("")
        self.resultado_tokens.clear()
        self.resultado_semantico.clear()
        self.resultado_sintactico.clear()
        self.mensaje_log.setText("")
        self.mostrar_tokens()

    def abrir_modal_archivos(self):
        archivos = listar_archivos_test()
        if not archivos:
            QMessageBox.warning(self, "Sin archivos", "No hay archivos de prueba en la carpeta 'test'.")
            return
        archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo de prueba (.cs)", "test", "Archivos C# (*.cs)")
        if archivo:
            self.cargar_archivo_test(os.path.basename(archivo))

    def cargar_archivo_test(self, nombre_archivo):
        try:
            contenido = cargar_archivo_test(nombre_archivo)
            self.editor.setText(contenido)
            self.analizar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {e}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = AnalizadorApp()
    ventana.show()
    sys.exit(app.exec_())
