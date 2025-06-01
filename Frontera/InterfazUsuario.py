from Control.ControlViaje import ControlViaje
from Control.ControlGasto import ControlGasto
from Control.ControlReporte import ControlReporte

class InterfazUsuario:
    """
    Gestiona la interacción entre el usuario y el sistema de registro de gastos 
    de viajes.
    
    Esta clase actúa como frontera entre la lógica de negocio y el usuario, 
    recibiendo entradas, mostrando mensajes y coordinando la ejecución de las 
    operaciones principales del sistema a través de los controladores.
    """
    def __init__(self):
        """
        Inicializa la interfaz de usuario y los controladores de viaje, gasto 
        y reporte.
        """
        self.control_viaje = ControlViaje()
        self.control_gasto = ControlGasto()
        self.control_reporte = ControlReporte()

    def iniciar_viaje(self, destino, fecha_inicio, fecha_fin, presupuesto_diario, es_exterior):
        """
        Inicia un nuevo viaje con los parámetros especificados.

        Args:
            destino (str): Destino del viaje.
            fecha_inicio (date): Fecha de inicio.
            fecha_fin (date): Fecha de fin.
            presupuesto_diario (float): Presupuesto diario asignado.
            es_exterior (bool): Indica si el viaje es al exterior.

        Returns:
            Viaje: Objeto Viaje creado.
        """
        viaje = self.control_viaje.crear_viaje(destino, fecha_inicio, fecha_fin, presupuesto_diario, es_exterior)
        print(f"\033[32mViaje creado exitosamente: {viaje.get_id()}\n\033[0m")
        return viaje

    def registrar_gasto(self, fecha, valor, metodo_pago, tipo_gasto, moneda_origen='COP'):
        """
        Registra un gasto en el viaje activo y muestra la diferencia con el 
        presupuesto diario.

        Args:
            fecha (date): Fecha del gasto.
            valor (float): Valor original del gasto.
            metodo_pago (MetodoPago): Método de pago utilizado.
            tipo_gasto (TipoGasto): Tipo de gasto realizado.
            moneda_origen (str, opcional): Moneda de origen, por defecto 'COP'.

        Returns:
            Gasto or None: Objeto Gasto registrado o None si no hay viaje activo.
        """
        viaje = self.control_viaje.obtener_viaje_activo()
        if not viaje:
            print("\033[31mNo hay viaje activo.\033[0m\n")
            return None
        gasto = self.control_gasto.registrar_gasto(viaje, fecha, valor, metodo_pago, tipo_gasto, moneda_origen)
        # Calcular diferencia sumando todos los gastos del día
        gastos = self.control_gasto.obtener_gastos_por_viaje(viaje)
        monto_gastado = sum(g.get_valor_en_pesos() for g in gastos if g.get_fecha() == fecha)
        presupuesto_diario = viaje.get_presupuesto_diario()
        diferencia = presupuesto_diario - monto_gastado
        print(f"\033[32mGasto registrado. Diferencia con presupuesto del día: {diferencia:.2f} COP\n\033[0m")
        return gasto

    def consultar_presupuesto(self, fecha):
        """
        Consulta la diferencia entre el presupuesto diario y el gasto realizado 
        en una fecha específica.

        Args:
            fecha (date): Fecha a consultar.

        Returns:
            float or None: Diferencia con el presupuesto diario o None si no hay 
            viaje activo o la fecha es inválida.
        """
        viaje = self.control_viaje.obtener_viaje_activo()
        if not viaje:
            print("\033[31mNo hay viaje activo.\033[0m\n")
            return None
        if fecha < viaje.get_fecha_inicio() or fecha > viaje.get_fecha_fin():
            print(f"\033[31mLa fecha {fecha} no está dentro del rango del viaje ({viaje.get_fecha_inicio()} a {viaje.get_fecha_fin()}).\033[0m\n")
            return None
        # Recalcular el monto gastado ese día usando los gastos almacenados
        gastos = self.control_gasto.obtener_gastos_por_viaje(viaje)
        monto_gastado = sum(g.get_valor_en_pesos() for g in gastos if g.get_fecha() == fecha)
        presupuesto_diario = viaje.get_presupuesto_diario()
        diferencia = presupuesto_diario - monto_gastado
        print(f"\033[32mDiferencia con presupuesto del {fecha}: {diferencia:.2f} COP\n\033[0m")
        return diferencia

    def generar_reporte_diario(self):
        """
        Genera y muestra un reporte diario de gastos del viaje activo.

        Returns:
            dict or None: Reporte diario generado o None si no hay viaje activo.
        """
        viaje = self.control_viaje.obtener_viaje_activo()
        if not viaje:
            print("\033[31mNo hay viaje activo.\033[0m\n")
            return None
        gastos = self.control_gasto.obtener_gastos_por_viaje(viaje)
        reporte = self.control_reporte.generar_reporte_diario(gastos)
        for fecha, datos in sorted(reporte.items()):
            print(f"{fecha}: Efectivo: {datos['EFECTIVO']:.2f} COP, Tarjeta: {datos['TARJETA']:.2f} COP, Total: {datos['TOTAL']:.2f} COP")
        print("\033[32mReporte diario generado exitosamente.\033[0m\n")
        return reporte

    def generar_reporte_por_tipo(self):
        """
        Genera y muestra un reporte de gastos agrupados por tipo del viaje activo.

        Returns:
            dict or None: Reporte por tipo generado o None si no hay viaje activo.
        """
        viaje = self.control_viaje.obtener_viaje_activo()
        if not viaje:
            print("\033[31mNo hay viaje activo.\033[0m\n")
            return None
        gastos = self.control_gasto.obtener_gastos_por_viaje(viaje)
        reporte = self.control_reporte.generar_reporte_por_tipo(gastos)
        for tipo, datos in reporte.items():
            print(f"{tipo}: Efectivo: {datos['EFECTIVO']:.2f} COP, Tarjeta: {datos['TARJETA']:.2f} COP, Total: {datos['TOTAL']:.2f} COP")
        print("\033[32mReporte por tipo de gasto generado exitosamente.\033[0m\n")
        return reporte

    def finalizar_viaje(self):
        """
        Finaliza el viaje activo si existe y muestra un mensaje de confirmación.

        Returns:
            bool: True si el viaje fue finalizado, False si no había viaje activo.
        """
        exito = self.control_viaje.finalizar_viaje()
        if exito:
            print("\033[32mViaje finalizado.\033[0m\n")
        else:
            print("\033[31mNo hay viaje activo para finalizar.\033[0m\n")
        return exito
