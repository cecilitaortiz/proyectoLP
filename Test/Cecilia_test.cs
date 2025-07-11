// Cecilia_test.cs
// Prueba de listas, var, tipos, asignaciones y errores

List<string> listaCadenas;
listaCadenas = new List<string> { "uno", "dos", "tres" };

var listaVar;
listaVar = new List<int> { 4, 5, 6 };

int n;
n = 7;
bool ok = false;

// Error: lista de listas no permitida
List<List<int>> listaDeListas;

// Error: asignación de tipo incorrecto
int x = "texto";

// Uso de var sin inicialización y luego con asignación
var sinTipo;
sinTipo = true;

// Función con return incorrecto
string F() {
    return 123;
}
