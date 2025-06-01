from enum import Enum

class TipoGasto(Enum):
    """
    Enumera los tipos de gasto permitidos en el sistema.
    
    Esta enumeración clasifica los gastos registrados en categorías predefinidas,
    lo que permite segmentar y analizar el destino del dinero durante un viaje.
    Facilita la generación de reportes y la validación de datos.
    """
    TRANSPORTE = 1
    ALOJAMIENTO = 2
    ALIMENTACION = 3
    ENTRETENIMIENTO = 4
    COMPRAS = 5
