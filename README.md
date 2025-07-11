#  Analizador de Código C# en Python

Este proyecto es un **analizador de código fuente en C#**, desarrollado en Python. Implementa un **análisis léxico, sintáctico y semántico** de programas escritos en C#, mostrando posibles errores y generando logs detallados. También incluye una **interfaz gráfica** en PyQt5 para facilitar su uso.

---

##  Características

- ✅ **Análisis Léxico** con `PLY` para identificar tokens de C#
- ✅ **Análisis Sintáctico** mediante reglas gramaticales definidas en `syntax.py`
- ✅ **Análisis Semántico** básico para validación de tipos y declaraciones
- ✅ **Interfaz gráfica** amigable con PyQt5
- ✅ **Generación de logs automáticos** con nombre de usuario Git y timestamp
- ✅ **Lectura de archivos de prueba** (`Thomas_prueba.cs`, `Cecilia_prueba.cs`,´Prueba_final.cs´.)

---

##  Requisitos

Tener Python 3.7 o superior.

### Instalar dependencias

```bash
pip install ply PyQt5 QScintilla

