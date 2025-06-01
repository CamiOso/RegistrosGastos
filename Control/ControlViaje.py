import uuid
from Auxiliares.ManejadorJSON import ManejadorJSON
from Entidad.Viaje import Viaje
from datetime import date

class ControlViaje:
    def __init__(self):
        """
        Inicializa el controlador de viajes, configurando la persistencia.
        """
        self.persistencia = ManejadorJSON()

    def crear_viaje(self, destino, fecha_inicio, fecha_fin, presupuesto_diario, es_exterior):
        """
        Crea un nuevo viaje, validando las fechas y finalizando cualquier viaje activo.

        Args:
            destino (str): Destino del viaje.
            fecha_inicio (date): Fecha de inicio del viaje.
            fecha_fin (date): Fecha de fin del viaje.
            presupuesto_diario (float): Presupuesto diario del viaje.
            esExterior (bool): Indica si el viaje es al exterior.

        Returns:
            Viaje: Objeto viaje creado.
        """
        if not self._validar_fechas(fecha_inicio, fecha_fin):
            raise ValueError("Fechas inválidas: la fecha de inicio debe ser anterior o igual a la de fin.")
        # Finaliza cualquier viaje activo
        viajes = self.persistencia.cargar_viajes()
        for v in viajes:
            if v.is_activo():
                v.set_activo(False)
        # Crea nuevo viaje
        viaje = Viaje(str(uuid.uuid4()), es_exterior, fecha_inicio, fecha_fin, presupuesto_diario)
        self.persistencia.guardar_viaje(viaje)
        return viaje

    def obtener_viaje_activo(self):
        """
        Obtiene el viaje activo (el último viaje creado que no ha sido finalizado).

        Returns:
            Viaje or None: Objeto viaje activo, o None si no hay viaje activo.
        """
        viajes = self.persistencia.cargar_viajes()
        for v in viajes:
            if v.is_activo():
                return v
        return None

    def finalizar_viaje(self):
        """
        Finaliza el viaje activo, marcándolo como no activo.

        Returns:
            bool: True si se finalizó el viaje, False si no había viaje activo.
        """
        viaje = self.obtener_viaje_activo()
        if viaje:
            viaje.set_activo(False)
            self.persistencia.guardar_viaje(viaje)
            return True
        return False

    def _validar_fechas(self, fecha_inicio, fecha_fin):
        """
        Valida que la fecha de inicio sea anterior o igual a la fecha de fin.

        Args:
            fecha_inicio (date): Fecha de inicio del viaje.
            fecha_fin (date): Fecha de fin del viaje.

        Returns:
            bool: True si la fecha de inicio es anterior o igual a la fecha de fin, False en caso contrario.
        """
        return fecha_inicio <= fecha_fin

