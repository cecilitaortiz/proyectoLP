using System;
using System.Collections.Generic;

public class CeciliaPrueba
{
    public int MiMetodo(int a, int b)
    {
        int resultado = a + b;
        if (resultado > 10)
        {
            return resultado;
        }
        else
        {
            return 0;
        }
    }

    public void Declaraciones()
    {
        int entero = 5;
        double doble = 3.14;
        float flotante = 2.5f;
        bool bandera = true;
        string texto = "Hola mundo";
        var variable = 100;
        List<int> lista = new List<int>();
    }
}
