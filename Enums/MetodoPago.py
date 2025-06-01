from enum import Enum

class MetodoPago(Enum):
    """
    Enumera los métodos de pago permitidos para un gasto.
    
    Proporciona una forma estructurada de validar y registrar cómo se efectuó 
    cada gasto (efectivo o tarjeta), permitiendo análisis y reportes 
    diferenciados según el método de pago.
    """
    EFECTIVO = 1
    TARJETA = 2
