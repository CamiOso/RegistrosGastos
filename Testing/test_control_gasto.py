import unittest
from datetime import date
from Entidad.Viaje import Viaje
from Control.ControlGasto import ControlGasto
from Enums.MetodoPago import MetodoPago
from Enums.TipoGasto import TipoGasto

class TestControlGasto(unittest.TestCase):
    def setUp(self):
        self.control_gasto = ControlGasto()
        self.viaje = Viaje(
            id="test-id",
            es_exterior=False,
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 5),
            presupuesto_diario=100000
        )
        self.viaje.activo = True

    def test_registro_gasto_valido_cop(self):
        """
        Prueba registrar un gasto válido en COP dentro del rango del viaje.
        Entrada: valor=50000, moneda='COP', fecha=2025-01-02
        Salida esperada: Gasto creado, valor_en_pesos=50000
        """
        gasto = self.control_gasto.registrar_gasto(
            self.viaje, date(2025, 1, 2), 50000, MetodoPago.EFECTIVO, TipoGasto.TRANSPORTE, 'COP')
        self.assertEqual(gasto.get_valor_en_pesos(), 50000)
        self.assertEqual(gasto.get_fecha(), date(2025, 1, 2))

    def test_registro_gasto_valido_usd(self):
        """
        Prueba registrar un gasto válido en USD (simula tasa 4000).
        Entrada: valor=10, moneda='USD', fecha=2025-01-03
        Salida esperada: valor_en_pesos=40000
        """
        self.control_gasto.conversor_moneda.obtener_tasa_cambio = lambda m: 4000  # Mock tasa
        gasto = self.control_gasto.registrar_gasto(
            self.viaje, date(2025, 1, 3), 10, MetodoPago.TARJETA, TipoGasto.COMPRAS, 'USD')
        self.assertEqual(gasto.get_valor_en_pesos(), 40000)

    def test_registro_gasto_fuera_de_rango(self):
        """
        Prueba registrar gasto fuera del rango de fechas del viaje.
        Entrada: fecha=2025-01-10 (fuera de rango)
        Salida esperada: Exception
        """
        with self.assertRaises(Exception):
            self.control_gasto.registrar_gasto(
                self.viaje, date(2025, 1, 10), 50000, MetodoPago.EFECTIVO, TipoGasto.TRANSPORTE, 'COP')

    def test_registro_gasto_sin_viaje_activo(self):
        """
        Prueba registrar gasto cuando el viaje está inactivo.
        Entrada: viaje.activo=False
        Salida esperada: Exception
        """
        self.viaje.activo = False
        with self.assertRaises(Exception):
            self.control_gasto.registrar_gasto(
                self.viaje, date(2025, 1, 2), 50000, MetodoPago.EFECTIVO, TipoGasto.TRANSPORTE, 'COP')

if __name__ == "__main__":
    unittest.main()
