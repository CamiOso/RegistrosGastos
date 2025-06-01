import os
from Frontera.InterfazUsuario import InterfazUsuario
from datetime import datetime
from Enums.MetodoPago import MetodoPago
from Enums.TipoGasto import TipoGasto

def main():
    interfaz_usuario = InterfazUsuario()
    print("\033[35mBienvenido al sistema de registro de gastos de viajes\n\033[0m")
    while True:
        print("\033[34mMenú principal:\033[0m")
        print("")
        print("\033[33m1. Iniciar nuevo viaje\033[0m")
        print("\033[33m2. Registrar gasto\033[0m")
        print("\033[33m3. Consultar diferencia de presupuesto por fecha\033[0m")
        print("\033[33m4. Generar reporte diario\033[0m")
        print("\033[33m5. Generar reporte por tipo de gasto\033[0m")
        print("\033[33m6. Eliminar todos los viajes y gastos\033[0m")
        print("\033[33m7. Finalizar viaje\033[0m")
        print("\033[33m0. Salir\033[0m")
        print("")
        opcion = input("Seleccione una opción: ")
        try:
            if opcion == '1':
                destino = input("Destino del viaje: ")
                exterior = input("¿El viaje es al exterior? (s/n): ").strip().lower() == 's'
                fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), "%Y-%m-%d").date()
                fecha_fin = datetime.strptime(input("Fecha de fin (YYYY-MM-DD): "), "%Y-%m-%d").date()
                presupuesto_diario = float(input("Presupuesto diario (en COP): "))
                interfaz_usuario.iniciar_viaje(destino, fecha_inicio, fecha_fin, presupuesto_diario, exterior)
            elif opcion == '2':
                fecha = datetime.strptime(input("Fecha del gasto (YYYY-MM-DD): "), "%Y-%m-%d").date()
                viaje = interfaz_usuario.control_viaje.obtener_viaje_activo()
                if not viaje:
                    print("\033[31mNo hay viaje activo.\033[0m\n")
                    continue
                if fecha < viaje.get_fecha_inicio() or fecha > viaje.get_fecha_fin():
                    print("\033[31mLa fecha del gasto no corresponde a los días del viaje.\033[0m\n")
                    continue
                valor = float(input("Valor del gasto: "))
                moneda = input("Moneda del gasto (COP/USD): ").strip().upper()
                print("Método de pago:")
                for metodo in MetodoPago:
                    print(f"{metodo.value}. {metodo.name}")
                metodo_pago = MetodoPago(int(input("Seleccione método de pago: ")))
                print("Tipo de gasto:")
                for tipo in TipoGasto:
                    print(f"{tipo.value}. {tipo.name}")
                tipo_gasto = TipoGasto(int(input("Seleccione tipo de gasto: ")))
                interfaz_usuario.registrar_gasto(fecha, valor, metodo_pago, tipo_gasto, moneda)
            elif opcion == '3':
                fecha = datetime.strptime(input("Fecha a consultar (YYYY-MM-DD): "), "%Y-%m-%d").date()
                interfaz_usuario.consultar_presupuesto(fecha)
            elif opcion == '4':
                interfaz_usuario.generar_reporte_diario()
            elif opcion == '5':
                interfaz_usuario.generar_reporte_por_tipo()
            elif opcion == '6':
                # Eliminar todos los viajes y gastos en JSONSaveFiles                
                base_dir = 'JSONSaveFiles'
                viajes_path = os.path.join(base_dir, 'viajes.json')
                gastos_path = os.path.join(base_dir, 'gastos.json')
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir)
                with open(viajes_path, 'w', encoding='utf-8') as f:
                    f.write('[]')
                with open(gastos_path, 'w', encoding='utf-8') as f:
                    f.write('[]')
                print("\033[31mTodos los viajes y gastos han sido eliminados.\033[0m\n")
            elif opcion == '7':
                interfaz_usuario.finalizar_viaje()
            elif opcion == '0':
                print("¡Hasta luego!")
                break
            else:
                print("\033[31mOpción no válida.\033[0m\n")
        except Exception as e:
            print(f"\033[31mError: {e}\033[0m\n")

if __name__ == "__main__":
    main()
