# test_hello.py — prueba básica para verificar el entorno Python

def add(a: int, b: int) -> int:
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

def test_bitcoin_import():
    """Verifica que embit (lib Bitcoin) está disponible."""
    import embit
    assert embit is not None
