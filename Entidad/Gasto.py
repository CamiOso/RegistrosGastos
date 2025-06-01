from datetime import date
from Enums.MetodoPago import MetodoPago
from Enums.TipoGasto import TipoGasto

class Gasto:
    """
    Modela un gasto realizado durante un viaje.
    
    Cada instancia almacena los detalles de un gasto individual, incluyendo 
    fecha, valor, método de pago y tipo de gasto. Es fundamental para el registro
    y posterior análisis de los gastos efectuados en los viajes.
    """
    def __init__(self, id, fecha, valor, valor_en_pesos, metodo_pago, tipo_gasto):
        """
        Inicializa un objeto Gasto con los detalles del gasto realizado.

        Args:
            id (str): Identificador único del gasto.
            fecha (date): Fecha en que se realizó el gasto.
            valor (float): Valor original del gasto en la moneda de origen.
            valor_en_pesos (float): Valor convertido a pesos colombianos.
            metodo_pago (MetodoPago): Método de pago utilizado.
            tipo_gasto (TipoGasto): Tipo de gasto realizado.
        """
        self.id = id
        self.fecha = fecha
        self.valor = valor
        self.valor_en_pesos = valor_en_pesos
        self.metodo_pago = metodo_pago
        self.tipo_gasto = tipo_gasto

    def get_id(self):
        """
        Obtiene el identificador único del gasto.

        Returns:
            str: ID del gasto.
        """
        return self.id

    def get_fecha(self):
        """
        Obtiene la fecha en que se realizó el gasto.

        Returns:
            date: Fecha del gasto.
        """
        return self.fecha

    def get_valor(self):
        """
        Obtiene el valor original del gasto en la moneda de origen.

        Returns:
            float: Valor original del gasto.
        """
        return self.valor

    def get_valor_en_pesos(self):
        """
        Obtiene el valor del gasto convertido a pesos colombianos.

        Returns:
            float: Valor en pesos colombianos.
        """
        return self.valor_en_pesos

    def get_metodo_pago(self):
        """
        Obtiene el método de pago utilizado para el gasto.

        Returns:
            MetodoPago: Método de pago del gasto.
        """
        return self.metodo_pago

    def get_tipo_gasto(self):
        """
        Obtiene el tipo de gasto realizado.

        Returns:
            TipoGasto: Tipo de gasto.
        """
        return self.tipo_gasto
