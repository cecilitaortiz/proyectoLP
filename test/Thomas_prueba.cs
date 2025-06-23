using System;

class ThomasPrueba
{
    public void LogicaYIncremento()
    {
        int x = 10;
        int y = 5;
        bool a = true;
        bool b = false;
        string s = "texto";
        char c = 'z';
        var lista = new List<int>();
        double d = 3.14;
        float f = 2.5f;

        // Operadores lógicos
        bool resultado1 = a && b;
        bool resultado2 = a || b;
        bool resultado3 = !a;
        bool resultado4 = (x < y);
        bool resultado5 = (x == y);
        bool resultado6 = (x != y);
        bool resultado7 = (x >= y);
        bool resultado8 = (x <= y);

        // Operadores aritméticos
        int suma = x + y;
        int resta = x - y;
        int mult = x * y;
        int div = x / y;
        int mod = x % y;
        int neg = -x;

        // Incremento y decremento
        x++;
        y--;
        ++x;
        --y;

        // Asignaciones compuestas
        x += 2;
        y -= 2;

        // Llamada a función
        Saludar();
        Console.WriteLine("Hola mundo");
        Console.WriteLine(x);

        // Estructura for
        for (int i = 0; i < 5; i++)
        {
            Console.WriteLine(i);
        }

        // Estructura if-else
        if (a)
        {
            Console.WriteLine("Verdadero");
        }
        else
        {
            Console.WriteLine("Falso");
        }

        // Lectura
        string entrada = Console.ReadLine();
        int num = int.Parse(Console.ReadLine());

        // Retorno
        return;
    }

    public void Saludar()
    {
        Console.WriteLine("¡Hola desde Saludar!");
    }

    private int Sumar(int a, int b)
    {
        return a + b;
    }

    protected void MetodoProtegido()
    {
        // Método protegido vacío
    }

    class Interna
    {
        public int valor;
    }
}
