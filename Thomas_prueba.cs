using System;

public class ThomasDemo {
    // Estructura de datos: lista de strings
    public List<string> palabras;

    // Propiedad
    public string Mensaje { get; set; }

    // Constructor
    public ThomasDemo() {
        palabras = new List<string>();
        Mensaje = "";
    }

    // Método: función que retorna un bool
    public bool EsPalindromo(string palabra) {
        // Expresión aritmética y condición
        int n = palabra.Length;
        for (int i = 0; i < n / 2; i = i + 1) {
            if (palabra[i] != palabra[n - i - 1]) {
                return false;
            }
        }
        return true;
    }

    // Método: función void con ingreso de datos y asignación
    public void ProcesarPalabra() {
        // Ingreso de datos
        Console.WriteLine("Ingrese una palabra:");
        string palabra = Console.ReadLine();

        // Asignación
        Mensaje = "Procesando: " + palabra;

        // Impresión
        Console.WriteLine(Mensaje);

        // Estructura de control: if con conector lógico
        if (palabra.Length > 5 && EsPalindromo(palabra)) {
            Console.WriteLine("La palabra es larga y palíndroma");
        } else {
            Console.WriteLine("No cumple ambas condiciones");
        }

        // Estructura de datos: agregar a lista
        palabras.Add(palabra);
    }
}
