import uuid
from Auxiliares.ManejadorJSON import ManejadorJSON
from Auxiliares.ConversorMoneda import ConversorMoneda
from Entidad.Gasto import Gasto
from Entidad.Viaje import Viaje
from typing import List
from datetime import date

class ControlGasto:
    """
    Controlador responsable de la gestión de gastos dentro de un viaje.
    
    Encapsula la lógica para registrar, validar y calcular diferencias 
    presupuestarias de los gastos, utilizando persistencia y conversión 
    de moneda cuando es necesario. Centraliza las operaciones relacionadas 
    con los gastos para mantener la separación de responsabilidades y 
    facilitar el mantenimiento del sistema.
    """
    def __init__(self):
        """
        Inicializa el controlador de gastos, configurando la persistencia y 
        el conversor_moneda de moneda.
        """
        self.persistencia = ManejadorJSON()
        self.conversor_moneda = ConversorMoneda()

    def registrar_gasto(self, viaje, fecha, valor, metodo_pago, tipo_gasto, moneda_origen='COP'):
        """
        Registra un nuevo gasto en el viaje, actualizando la persistencia y 
        el presupuesto diario.

        Args:
            viaje (Viaje): Objeto viaje donde se registra el gasto.
            fecha (date): Fecha del gasto.
            valor (float): Valor original del gasto.
            metodo_pago (MetodoPago): Método de pago utilizado.
            tipo_gasto (TipoGasto): Tipo de gasto realizado.
            moneda_origen (str, opcional): Moneda de origen, por defecto es 'COP'.

        Returns:
            Gasto: Objeto Gasto registrado.

        Raises:
            Exception: Si el viaje no está activo o la fecha es inválida 
            para el viaje.
        """
        if not viaje.is_activo():
            raise Exception('No se puede registrar gasto: el viaje no está activo.')
        if not self._validar_gasto(viaje, fecha):
            raise Exception('La fecha del gasto no corresponde a los días del viaje.')
        valor_en_pesos = self.conversor_moneda.convertir_a_pesos(valor, moneda_origen)
        gasto = Gasto(str(uuid.uuid4()), fecha, valor, valor_en_pesos, metodo_pago, tipo_gasto)
        gastos = self.persistencia.cargar_gastos()
        gastos.append(gasto)
        self.persistencia.guardar_gastos(gastos)
        # Actualiza el presupuesto del día correspondiente en el viaje
        for presupuesto in viaje.presupuestos:
            if presupuesto.get_fecha() == fecha:
                presupuesto.set_monto_gastado(presupuesto.get_monto_gastado() + valor_en_pesos)
        self.persistencia.guardar_viaje(viaje)
        return gasto

    def _validar_gasto(self, viaje, fecha):
        """
        Valida si una fecha corresponde a los días del viaje.

        Args:
            viaje (Viaje): Objeto viaje a validar.
            fecha (date): Fecha a validar.

        Returns:
            bool: True si la fecha está dentro del rango del viaje, 
            False en caso contrario.
        """
        return viaje.get_fecha_inicio() <= fecha <= viaje.get_fecha_fin()

    def obtener_gastos_por_viaje(self, viaje):
        """
        Obtiene todos los gastos registrados durante el periodo del viaje.

        Args:
            viaje (Viaje): Objeto viaje a consultar.

        Returns:
            list[Gasto]: Lista de objetos Gasto correspondientes al viaje.
        """
        gastos = self.persistencia.cargar_gastos()
        return [g for g in gastos if viaje.get_fecha_inicio() <= g.get_fecha() <= viaje.get_fecha_fin()]

