from datetime import date
from datetime import timedelta
from typing import List
from Entidad.Presupuesto import Presupuesto

class Viaje:
    """
    Representa un viaje con su rango de fechas, presupuesto y estado.
    
    Gestiona la información esencial de un viaje, incluyendo si es al exterior, 
    fechas, presupuesto diario y su estado (activo o finalizado). Además, 
    organiza los presupuestos diarios asociados, facilitando el seguimiento 
    y control financiero del viaje.
    """
    def __init__(self, id, es_exterior, fecha_inicio, fecha_fin, presupuesto_diario):
        """
        Inicializa un objeto Viaje con la información principal y los 
        presupuestos diarios.

        Args:
            id (str): Identificador único del viaje.
            es_exterior (bool): Indica si el viaje es al exterior.
            fecha_inicio (date): Fecha de inicio del viaje.
            fecha_fin (date): Fecha de fin del viaje.
            presupuesto_diario (float): Presupuesto diario asignado.
        """
        self.id = id
        self.es_exterior = es_exterior
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.activo = True
        self.presupuestos = []
        # Crear presupuesto por cada día del viaje        
        dia = fecha_inicio
        while dia <= fecha_fin:
            self.presupuestos.append(Presupuesto(dia, presupuesto_diario))
            dia += timedelta(days=1)

    def is_activo(self):
        """
        Indica si el viaje está activo.

        Returns:
            bool: True si el viaje está activo, False si está finalizado.
        """
        return self.activo

    def es_exterior(self):
        """
        Indica si el viaje es al exterior.

        Returns:
            bool: True si el viaje es al exterior, False si es nacional.
        """
        return self.es_exterior

    def get_id(self):
        """
        Obtiene el identificador único del viaje.

        Returns:
            str: ID del viaje.
        """
        return self.id

    def get_fecha_inicio(self):
        """
        Obtiene la fecha de inicio del viaje.

        Returns:
            date: Fecha de inicio.
        """
        return self.fecha_inicio

    def get_fecha_fin(self):
        """
        Obtiene la fecha de fin del viaje.

        Returns:
            date: Fecha de fin.
        """
        return self.fecha_fin

    def get_presupuesto_diario(self):
        """
        Obtiene el presupuesto diario asignado al viaje.

        Returns:
            float: Presupuesto diario.
        """
        return self.presupuesto_diario

    def set_activo(self, activo):
        """
        Cambia el estado de actividad del viaje.

        Args:
            activo (bool): Nuevo estado del viaje (True para activo, 
            False para finalizado).
        """
        self.activo = activo
