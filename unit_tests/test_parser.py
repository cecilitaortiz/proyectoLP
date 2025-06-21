import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from lexer import lexer
from syntax import parser

class TestParser(unittest.TestCase):
    def parse(self, code):
        # Reinicia el lexer y parser para cada prueba
        lexer.lineno = 1
        result = []
        def custom_error(p):
            if p:
                result.append(f"Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'")
            else:
                result.append("Error de sintaxis: Fin de entrada inesperado.")
        parser.errorfunc = custom_error
        parser.parse(code, lexer=lexer)
        return result

    def test_class_with_method(self):
        code = """
        public class Test {
            public void Foo(int x) {
                int y = x + 1;
            }
        }
        """
        result = self.parse(code)
        self.assertIn("Análisis sintáctico exitoso.", result or ["Análisis sintáctico exitoso."])

    def test_assignment_and_increment(self):
        code = """
        class A {
            void Main() {
                int x = 5;
                x++;
            }
        }
        """
        result = self.parse(code)
        self.assertIn("Análisis sintáctico exitoso.", result or ["Análisis sintáctico exitoso."])

    def test_if_else(self):
        code = """
        class B {
            void Main() {
                int x = 0;
                if (x > 0) {
                    x = x - 1;
                } else {
                    x = x + 1;
                }
            }
        }
        """
        result = self.parse(code)
        self.assertIn("Análisis sintáctico exitoso.", result or ["Análisis sintáctico exitoso."])

    def test_for_and_while(self):
        code = """
        class C {
            void Main() {
                for (int i = 0; i < 10; i++) {
                    while (i > 0) {
                        i--;
                    }
                }
            }
        }
        """
        result = self.parse(code)
        self.assertIn("Análisis sintáctico exitoso.", result or ["Análisis sintáctico exitoso."])

    def test_syntax_error(self):
        code = """
        class D {
            void Main() {
                int x = ;
            }
        }
        """
        result = self.parse(code)
        self.assertTrue(any("Error de sintaxis" in r for r in result))

if __name__ == "__main__":
    unittest.main()