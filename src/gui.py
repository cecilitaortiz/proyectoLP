import os
import gradio as gr
import subprocess
from lexer import lexer
from main import analizar_codigo, guardar_log


# Obtener nombre de usuario de Git
try:
    usuario_git = subprocess.check_output(["git", "config", "user.name"]).strip().decode('utf-8')
except subprocess.CalledProcessError:
    usuario_git = "desconocido"

def gr_analizar_codigo(entrada):
    try:
        resultado = analizar_codigo(entrada)
        log_path = guardar_log(resultado)
        mensaje = f"✅ Log guardado exitosamente en '{log_path}'"
        return gr.update(value="\n".join(resultado)), gr.update(value=mensaje, visible=True)
    except Exception as e:
        return gr.update(value=""), gr.update(value=f"❌ Error: {str(e)}", visible=True)

def listar_archivos_test():
    carpeta = "test"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    return [f for f in os.listdir(carpeta) if f.endswith(".cs")]

def cargar_archivo_test(nombre_archivo):
    ruta = os.path.join("test", nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

def gr_analizar_archivo_seleccionado(nombre_archivo):
    try:
        contenido = cargar_archivo_test(nombre_archivo)
        resultado = analizar_codigo(contenido)
        log_path = guardar_log(resultado)
        mensaje = f"✅ Log guardado exitosamente en '{log_path}'"
        return contenido, "\n".join(resultado), mensaje
    except Exception as e:
        return "", "", f"❌ Error: {str(e)}"

def gr_subir_archivo(archivo):
    if archivo is not None:
        ruta_destino = os.path.join("test", os.path.basename(archivo.name))
        with open(ruta_destino, "wb") as f:
            f.write(archivo.read())
    return gr.Dropdown.update(choices=listar_archivos_test())

custom_css = """
#editor {
    font-size: 14px;
    min-height: 350px;
    max-height: 350px;
    height: 350px;
}
.svelte-1ipelgc > .gr-box {
    margin: 0 !important;
    padding: 0 !important;
}
.gr-row {
    gap: 0 !important;
}
"""

with gr.Blocks(title="Analizador Léxico de C#", css=custom_css) as demo:
    gr.Markdown("# Analizador Léxico de C#")

    with gr.Row():
        editor = gr.Code(
            language="python",  # Cambia 'csharp' por 'python' o 'text' para evitar el error
            lines=15,
            elem_id="editor",
            value="",
            show_label=False
        )
        with gr.Column():
            with gr.Row():
                boton_tokens = gr.Button("Tokens", elem_id="btn_tokens")
                boton_semantico = gr.Button("Semántico", elem_id="btn_semantico")
                boton_sintactico = gr.Button("Sintáctico", elem_id="btn_sintactico")
            resultado_tokens = gr.Textbox(lines=15, label="Tokens", elem_id="resultado_tokens", visible=True, max_lines=15, min_width=400)
            resultado_semantico = gr.Textbox(lines=15, label="Semántico", elem_id="resultado_semantico", visible=False, max_lines=15, min_width=400)
            resultado_sintactico = gr.Textbox(lines=15, label="Sintáctico", elem_id="resultado_sintactico", visible=False, max_lines=15, min_width=400)

    mensaje_log = gr.Markdown(visible=False)

    with gr.Row():
        boton_analizar = gr.Button("Analizar")
        boton_archivo = gr.Button("Analizar archivo de prueba")
        boton_limpiar = gr.Button("Limpiar")

    # Modal para seleccionar y subir archivos
    with gr.Row(visible=False) as modal:
        gr.Markdown("### Selecciona o sube un archivo de prueba (.cs)")
        archivos_dropdown = gr.Dropdown(choices=listar_archivos_test(), label="Archivos en test/")
        boton_cargar = gr.Button("Cargar archivo seleccionado")
        subir_archivo = gr.File(label="Subir archivo .cs", file_types=[".cs"])
        boton_cerrar = gr.Button("Cerrar")

    def mostrar_modal():
        return gr.Row.update(visible=True)

    def ocultar_modal():
        return gr.Row.update(visible=False)

    boton_archivo.click(
        fn=mostrar_modal,
        inputs=None,
        outputs=modal
    )

    boton_cerrar.click(
        fn=ocultar_modal,
        inputs=None,
        outputs=modal
    )

    # Cargar archivo seleccionado de la lista
    def gr_analizar_archivo_seleccionado(nombre_archivo):
        try:
            contenido = cargar_archivo_test(nombre_archivo)
            resultado = analizar_codigo(contenido)
            log_path = guardar_log(resultado)
            mensaje = f"✅ Log guardado exitosamente en '{log_path}'"
            return contenido, "\n".join(resultado), mensaje
        except Exception as e:
            return "", "", f"❌ Error: {str(e)}"

    boton_cargar.click(
        fn=gr_analizar_archivo_seleccionado,
        inputs=archivos_dropdown,
        outputs=[editor, resultado_tokens, mensaje_log]
    )

    # Subir archivo .cs desde el sistema de archivos
    subir_archivo.upload(
        fn=gr_subir_archivo,
        inputs=subir_archivo,
        outputs=archivos_dropdown
    )

    # Analizar código ingresado manualmente
    boton_analizar.click(
        fn=gr_analizar_codigo,
        inputs=editor,
        outputs=[resultado_tokens, mensaje_log]
    )

    # Limpiar todos los campos y resultados
    boton_limpiar.click(
        fn=lambda: ("", "", "", "", gr.update(value="", visible=False)),
        inputs=None,
        outputs=[editor, resultado_tokens, resultado_semantico, resultado_sintactico, mensaje_log]
    )

    # Lógica para mostrar solo el recuadro seleccionado
    def mostrar_tokens():
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    def mostrar_semantico():
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    def mostrar_sintactico():
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

    boton_tokens.click(
        fn=mostrar_tokens,
        inputs=None,
        outputs=[resultado_tokens, resultado_semantico, resultado_sintactico]
    )
    boton_semantico.click(
        fn=mostrar_semantico,
        inputs=None,
        outputs=[resultado_tokens, resultado_semantico, resultado_sintactico]
    )
    boton_sintactico.click(
        fn=mostrar_sintactico,
        inputs=None,
        outputs=[resultado_tokens, resultado_semantico, resultado_sintactico]
    )

if __name__ == "__main__":
    demo.launch()
 

# Nota:
# El componente gr.Code ya incluye scroll automático y numeración de líneas por defecto.
# No es necesario ni posible agregar 'autoscroll=True' como argumento.
