import unittest
import time
from Auxiliares.ConversorMoneda import ConversorMoneda

class TestConversorMoneda(unittest.TestCase):
    def setUp(self):
        self.conversor = ConversorMoneda()

    def test_tasa_usd_correcta(self):
        """
        Prueba obtener_tasa_cambio para USD (simula tasa 4100).
        Entrada: moneda='USD'
        Salida esperada: 4100
        """
        self.conversor._cache['USD'] = 4100
        self.conversor._cache_time = time.time()
        tasa = self.conversor.obtener_tasa_cambio('USD')
        self.assertEqual(tasa, 4100)

    def test_tasa_cache(self):
        """
        Prueba que el cache se use si no ha expirado.
        Entrada: cache['USD']=4200, cache_time=now
        Salida esperada: 4200
        """
        
        self.conversor._cache['USD'] = 4200
        self.conversor._cache_time = time.time()
        tasa = self.conversor.obtener_tasa_cambio('USD')
        self.assertEqual(tasa, 4200)

    def test_tasa_fallback(self):
        """
        Prueba obtener_tasa_cambio para moneda no soportada.
        Entrada: moneda='CHF'
        Salida esperada: 1 (fallback)
        """
        tasa = self.conversor.obtener_tasa_cambio('CHF')
        self.assertEqual(tasa, 1)

    def test_tasa_api_error(self):
        """
        Prueba manejo de error si la API falla (simula excepción).
        Entrada: moneda='USD', requests.get lanza excepción
        Salida esperada: 1
        """
        original_get = self.conversor.API_URL
        self.conversor.API_URL = 'http://noexiste.localhost'
        tasa = self.conversor.obtener_tasa_cambio('USD')
        print(tasa)
        self.assertEqual(tasa, 1)
        self.conversor.API_URL = original_get

if __name__ == "__main__":
    unittest.main()
