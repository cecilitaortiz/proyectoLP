# test_lexer.py

import unittest
from lexer import Lexer  # Asegúrate de que la ruta de importación sea correcta

class TestLexer(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()

    def test_single_token(self):
        self.lexer.input("a")
        token = self.lexer.token()
        self.assertEqual(token.type, "IDENTIFIER")
        self.assertEqual(token.value, "a")

    def test_number_token(self):
        self.lexer.input("123")
        token = self.lexer.token()
        self.assertEqual(token.type, "NUMBER")
        self.assertEqual(token.value, 123)

    def test_plus_token(self):
        self.lexer.input("+")
        token = self.lexer.token()
        self.assertEqual(token.type, "PLUS")
        self.assertEqual(token.value, "+")

    # Agrega más pruebas según sea necesario

if __name__ == "__main__":
    unittest.main()