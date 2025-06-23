using System;

int a = 5;
double b = 3.14;
bool flag = true;
string mensaje = "Hola";
char c = 'x';
var lista = new List<int>();

void Saludar() {
    Console.WriteLine(mensaje);
}

a++;
b--;

for (int i = 0; i < 10; i++) {
    Console.WriteLine(i);
}

if (flag) {
    Saludar();
} else {
    Console.WriteLine("No saludo");
}
