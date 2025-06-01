from datetime import date

class Presupuesto:
    """
    Representa el presupuesto asignado a un día específico de un viaje.
    
    Esta clase encapsula la información financiera diaria de un viaje, 
    permitiendo llevar el control de cuánto dinero fue asignado y gastado 
    en una fecha concreta. Facilita el cálculo de diferencias entre presupuesto 
    y gasto real, lo que es esencial para reportes y alertas de sobregiro.
    """
    def __init__(self, fecha, monto_asignado):
        """
        Inicializa un objeto Presupuesto para una fecha específica.

        Args:
            fecha (date): Fecha a la que corresponde el presupuesto.
            monto_asignado (float): Monto asignado para esa fecha.
        """
        self.fecha = fecha
        self.monto_asignado = monto_asignado
        self.monto_gastado = 0.0

    def get_fecha(self):
        """
        Obtiene la fecha asociada a este presupuesto.

        Returns:
            date: Fecha del presupuesto.
        """
        return self.fecha

    def get_monto_asignado(self):
        """
        Obtiene el monto asignado para la fecha de este presupuesto.

        Returns:
            float: Monto asignado.
        """
        return self.monto_asignado

    def get_monto_gastado(self):
        """
        Obtiene el monto gastado registrado para la fecha de este presupuesto.

        Returns:
            float: Monto gastado.
        """
        return self.monto_gastado

    def set_monto_gastado(self, monto):
        """
        Establece el monto gastado para la fecha de este presupuesto.

        Args:
            monto (float): Monto gastado a registrar.
        """
        self.monto_gastado = monto
