// Thomas_test.cs
// Prueba de variables, listas, var, funciones y control de flujo

int a = 5;
double b = 3.14;
bool flag = true;
string texto = "Hola";
char c = 'x';

List<int> listaEnteros;
listaEnteros = new List<int>();
listaEnteros = new List<int> { 1, 2, 3 };

var x = 10;
var y = "cadena";
var z;
z = 2.5;

if (a > 3) {
    Console.WriteLine("a es mayor que 3");
} else {
    Console.WriteLine("a no es mayor que 3");
}

// Función simple
double Sumar(double p1, double p2) {
    return p1 + p2;
}
double resultado = Sumar(2.0, 3.0);
