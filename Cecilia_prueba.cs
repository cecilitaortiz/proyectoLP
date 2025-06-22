using System;

public class CeciliaDemo {
    // Estructura de datos: lista de enteros
    public List<int> numeros;

    // Propiedad
    public int PropiedadEjemplo { get; set; }

    // Constructor
    public CeciliaDemo() {
        numeros = new List<int>();
        PropiedadEjemplo = 0;
    }

    // Método: función que retorna un string
    public string Saludar(string nombre) {
        // Impresión
        Console.WriteLine("Hola, " + nombre);
        return "Saludo enviado";
    }

    // Método: función que no retorna nada
    public void LeerYSumar() {
        // Ingreso de datos
        Console.WriteLine("Ingrese un número:");
        int a = int.Parse(Console.ReadLine());
        Console.WriteLine("Ingrese otro número:");
        int b = int.Parse(Console.ReadLine());

        // Expresión aritmética
        int suma = a + b * 2 - (a / 2);

        // Asignación de variable
        PropiedadEjemplo = suma;

        // Estructura de control: if-else con conectores lógicos
        if ((a > 0 && b > 0) || suma > 10) {
            Console.WriteLine("La suma es positiva o mayor a 10");
        } else {
            Console.WriteLine("La suma no cumple la condición");
        }

        // Estructura de control: for
        for (int i = 0; i < 5; i = i + 1) {
            numeros.Add(i);
        }
    }
}
