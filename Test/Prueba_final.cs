// Prueba_final.cs
// Prueba integral: variables, listas, var, funciones, control de flujo, errores

float f = 2.5;
List<double> listaDoubles = new List<double> { 1.1, 2.2 };

var autoVar;
autoVar = "auto";

// Error: uso de var antes de asignar
var sinAsignar;
Console.WriteLine(sinAsignar);

// Error: lista de listas
List<List<string>> listaDeListas;

// Función correcta y función con error de tipo
int Sumar(int a, int b) {
    return a + b;
}
bool Falso() {
    return 0;
}

// Control de flujo
if (f < 3.0) {
    Console.WriteLine("f es menor que 3");
} else {
    Console.WriteLine("f es mayor o igual que 3");
}
