from Entidad.Gasto import Gasto
from typing import List, Dict, Any
from collections import defaultdict

class ControlReporte:
    """
    Controlador encargado de generar reportes financieros de los viajes.
    
    Proporciona métodos para calcular y agrupar gastos por fecha, tipo y método
    de pago, facilitando la presentación y el análisis de la información 
    financiera del viaje.
    """
    def generar_reporte_diario(self, gastos):
        """
        Genera un reporte diario de los gastos agrupados por fecha y método 
        de pago.

        Args:
            gastos (list[Gasto]): Lista de objetos Gasto a procesar.

        Returns:
            dict: Un diccionario donde cada clave es una fecha y el valor es 
            otro diccionario con los totales por método de pago ('EFECTIVO', 
            'TARJETA') y el total general ('TOTAL').
        """
        reporte = defaultdict(lambda: {'EFECTIVO': 0.0, 'TARJETA': 0.0, 'TOTAL': 0.0})
        for g in gastos:
            fecha = g.get_fecha()
            metodo = g.get_metodo_pago().name
            reporte[fecha][metodo] += g.get_valor_en_pesos()
            reporte[fecha]['TOTAL'] += g.get_valor_en_pesos()
        return dict(reporte)

    def generar_reporte_por_tipo(self, gastos):
        """
        Genera un reporte de los gastos agrupados por tipo de gasto y método 
        de pago.

        Args:
            gastos (list[Gasto]): Lista de objetos Gasto a procesar.

        Returns:
            dict: Un diccionario donde cada clave es el tipo de gasto y el 
            valor es otro diccionario con los totales por método de pago 
            ('EFECTIVO', 'TARJETA') y el total general ('TOTAL').
        """
        reporte = defaultdict(lambda: {'EFECTIVO': 0.0, 'TARJETA': 0.0, 'TOTAL': 0.0})
        for g in gastos:
            tipo = g.get_tipo_gasto().name
            metodo = g.get_metodo_pago().name
            reporte[tipo][metodo] += g.get_valor_en_pesos()
            reporte[tipo]['TOTAL'] += g.get_valor_en_pesos()
        return dict(reporte)

    def calcular_totales(self, gastos):
        """
        Calcula el total de gastos por método de pago y el total general.

        Args:
            gastos (list[Gasto]): Lista de objetos Gasto a procesar.

        Returns:
            dict: Un diccionario con los totales por método de pago 
            ('EFECTIVO', 'TARJETA') y el total general ('TOTAL').
        """
        totales = {'EFECTIVO': 0.0, 'TARJETA': 0.0, 'TOTAL': 0.0}
        for g in gastos:
            metodo = g.get_metodo_pago().name
            totales[metodo] += g.get_valor_en_pesos()
            totales['TOTAL'] += g.get_valor_en_pesos()
        return totales

