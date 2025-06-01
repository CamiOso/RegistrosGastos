import json
import os
from typing import List
from datetime import date, datetime
from Entidad.Viaje import Viaje
from Entidad.Gasto import Gasto
from Entidad.Presupuesto import Presupuesto
from Enums.MetodoPago import MetodoPago
from Enums.TipoGasto import TipoGasto

class ManejadorJSON:
    """
    Clase encargada de la persistencia y recuperación de datos de viajes y gastos en archivos JSON.
    Proporciona métodos para guardar y cargar objetos de dominio desde archivos, serializando y deserializando las entidades del sistema.
    """
    BASE_DIR = 'JSONSaveFiles'
    VIAJES_FILE = os.path.join(BASE_DIR, 'viajes.json')
    GASTOS_FILE = os.path.join(BASE_DIR, 'gastos.json')

    def guardar_viaje(self, viaje):
        """
        Guarda o actualiza un viaje en el archivo JSON de viajes.

        Si existe un viaje con el mismo ID, lo reemplaza. Si no existe, lo agrega.

        Args:
            viaje (Viaje): Objeto Viaje a guardar.
        """
        if not os.path.exists(self.BASE_DIR):
            os.makedirs(self.BASE_DIR)
        viajes = self.cargar_viajes()
        # Reemplaza si ya existe uno con el mismo id
        viajes = [v for v in viajes if v.get_id() != viaje.get_id()]
        viajes.append(viaje)
        with open(self.VIAJES_FILE, 'w', encoding='utf-8') as f:
            json.dump([self._viaje_to_dict(v) for v in viajes], f, ensure_ascii=False, indent=2)

    def cargar_viajes(self):
        """
        Carga todos los viajes almacenados en el archivo JSON.

        Returns:
            list[Viaje]: Lista de objetos Viaje recuperados del archivo. Si el archivo no existe, retorna una lista vacía.
        """
        if not os.path.exists(self.VIAJES_FILE):
            return []
        with open(self.VIAJES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [self._dict_to_viaje(d) for d in data]

    def guardar_gastos(self, gastos):
        """
        Guarda la lista de gastos en el archivo JSON correspondiente.

        Args:
            gastos (list[Gasto]): Lista de objetos Gasto a guardar.
        """
        if not os.path.exists(self.BASE_DIR):
            os.makedirs(self.BASE_DIR)
        with open(self.GASTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump([self._gasto_to_dict(g) for g in gastos], f, ensure_ascii=False, indent=2)

    def cargar_gastos(self):
        """
        Carga todos los gastos almacenados en el archivo JSON.

        Returns:
            list[Gasto]: Lista de objetos Gasto recuperados del archivo. Si el archivo no existe, retorna una lista vacía.
        """
        if not os.path.exists(self.GASTOS_FILE):
            return []
        with open(self.GASTOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [self._dict_to_gasto(d) for d in data]

    def _viaje_to_dict(self, viaje):
        """
        Convierte un objeto Viaje a un diccionario serializable para JSON.

        Args:
            viaje (Viaje): Objeto Viaje a convertir.

        Returns:
            dict: Representación serializable del viaje.
        """
        return {
            'id': viaje.get_id(),
            'esExterior': viaje.es_exterior,
            'fechaInicio': viaje.get_fecha_inicio().isoformat(),
            'fechaFin': viaje.get_fecha_fin().isoformat(),
            'presupuestoDiario': viaje.get_presupuesto_diario(),
            'activo': viaje.is_activo(),
            'presupuestos': [self._presupuesto_to_dict(p) for p in viaje.presupuestos]
        }

    def _dict_to_viaje(self, d):
        """
        Convierte un diccionario a un objeto Viaje.

        Args:
            d (dict): Diccionario con los datos del viaje.

        Returns:
            Viaje: Objeto Viaje reconstruido.
        """
        v = Viaje(
            id=d['id'],
            es_exterior=d['esExterior'],
            fecha_inicio=datetime.strptime(d['fechaInicio'], '%Y-%m-%d').date(),
            fecha_fin=datetime.strptime(d['fechaFin'], '%Y-%m-%d').date(),
            presupuesto_diario=d['presupuestoDiario']
        )
        v.activo = d.get('activo', True)
        v.presupuestos = [self._dict_to_presupuesto(p) for p in d.get('presupuestos',[])]
        return v

    def _presupuesto_to_dict(self, p):
        """
        Convierte un objeto Presupuesto a un diccionario serializable para JSON.

        Args:
            p (Presupuesto): Objeto Presupuesto a convertir.

        Returns:
            dict: Representación serializable del presupuesto.
        """
        return {
            'fecha': p.get_fecha().isoformat(),
            'montoAsignado': p.get_monto_asignado(),
            'montoGastado': p.get_monto_gastado()
        }

    def _dict_to_presupuesto(self, d):
        """
        Convierte un diccionario a un objeto Presupuesto.

        Args:
            d (dict): Diccionario con los datos del presupuesto.

        Returns:
            Presupuesto: Objeto Presupuesto reconstruido.
        """
        return Presupuesto(
            datetime.strptime(d['fecha'], '%Y-%m-%d').date(),
            d['montoAsignado']
        )

    def _gasto_to_dict(self, gasto):
        """
        Convierte un objeto Gasto a un diccionario serializable para JSON.

        Args:
            gasto (Gasto): Objeto Gasto a convertir.

        Returns:
            dict: Representación serializable del gasto.
        """
        return {
            'id': gasto.get_id(),
            'fecha': gasto.get_fecha().isoformat(),
            'valor': gasto.get_valor(),
            'valorEnPesos': gasto.get_valor_en_pesos(),
            'metodoPago': gasto.get_metodo_pago().name,
            'tipoGasto': gasto.get_tipo_gasto().name
        }

    def _dict_to_gasto(self, d):
        """
        Convierte un diccionario a un objeto Gasto.

        Args:
            d (dict): Diccionario con los datos del gasto.

        Returns:
            Gasto: Objeto Gasto reconstruido.
        """
        return Gasto(
            d['id'],
            datetime.strptime(d['fecha'], '%Y-%m-%d').date(),
            d['valor'],
            d['valorEnPesos'],
            MetodoPago[d['metodoPago']],
            TipoGasto[d['tipoGasto']]
        )

