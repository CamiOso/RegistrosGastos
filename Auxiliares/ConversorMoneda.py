import requests
import time

class ConversorMoneda:
    """
    Proporciona utilidades para convertir Dólar estado unidense (USD) a pesos
    colombianos (COP).
    
    Esta clase abstrae la lógica de obtención y almacenamiento en caché de tasas
    de cambio, permitiendo la conversión automática de valores monetarios en 
    diferentes monedas al registrar gastos. Es fundamental para la 
    interoperabilidad y el análisis financiero en viajes internacionales.
    """
    API_KEY = '379438f42d1f889ad7797aaf'
    API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

    _cache = {}
    _cache_time = 0
    _cache_ttl = 3600  # 1 hora

    def convertir_a_pesos(self, valor, moneda_origen):
        """
        Convierte un monto en una moneda origen a pesos colombianos (COP).

        Args:
            valor (float): Monto a convertir.
            moneda_origen (str): Moneda de origen (por defecto 'COP').

        Returns:
            float: Monto convertido a pesos colombianos.
        """
        moneda = moneda_origen.upper()
        if moneda == 'COP':
            return valor
        tasa = self.obtener_tasa_cambio(moneda)
        if tasa == 1 and moneda == 'USD':
            print("\033[31mADVERTENCIA: La tasa de cambio USD->COP fue 1. Puede haber un error de conexión con la API.\033[0m")
        return valor * tasa

    def obtener_tasa_cambio(self, moneda_origen):
        """
        Obtiene la tasa de cambio entre la moneda de origen y el peso colombiano 
        (COP).

        Args:
            moneda_origen (str): Moneda de origen (por defecto 'COP').

        Returns:
            float: Tasa de cambio entre la moneda de origen y el peso colombiano.
        """
        moneda = moneda_origen.upper()
        if moneda == 'COP':
            return 1
        if moneda != 'USD':
            return 1
        ahora = time.time()
        if ('USD' in self._cache and (ahora - self._cache_time < self._cache_ttl)):
            return self._cache['USD']
        # Solo soportamos USD->COP en este ejemplo
        try:
            resp = requests.get(self.API_URL)
            data = resp.json()
            if 'conversion_rates' in data:
                tasa = data['conversion_rates'].get('COP', 1)
                self._cache['USD'] = tasa
                self._cache_time = ahora
                return tasa
        except Exception as e:
            print(f"\033[31mError al obtener tasa de cambio: {e}\033[0m")
        return 1

