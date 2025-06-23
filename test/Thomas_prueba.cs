int Sumar(int a, int b) {
    return a + b;
}

int resultado = Sumar(10, -3);
Console.WriteLine(resultado);

int otro = Sumar(Sumar(1, 2), 5);
Console.WriteLine(otro);

int a = 5;
if (a > 0) {
    Console.WriteLine(a);
}

int b = -1;
if (b > 0) {
    Console.WriteLine(b);
} else {
    Console.WriteLine(0);
}

int c = 0;
if (c > 0) {
    Console.WriteLine("positivo");
} else if (c == 0) {
    Console.WriteLine("cero");
} else if (c == -1) {
    Console.WriteLine("menos uno");
} else {
    Console.WriteLine("negativo");
}

for (int i = 0; i < 3; i = i + 1) {
    Console.WriteLine(i);
}

for (j = 10; j > 0; j = j - 1) {
    Console.WriteLine(j);
}

