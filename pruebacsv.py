import csv
import os

# Archivo de persistencia
ARCHIVO_CSV = 'clientes_gimnasio.csv'
CAMPOS = ['id', 'nombre', 'edad', 'plan', 'estado']

def cargar_datos():
    """Carga los datos del archivo CSV al iniciar el programa."""
    clientes = []
    if os.path.exists(ARCHIVO_CSV):
        try:
            with open(ARCHIVO_CSV, mode='r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    # Convertir la edad a entero para mantener el tipo de dato correcto
                    fila['edad'] = int(fila['edad'])
                    clientes.append(fila)
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
    return clientes

def guardar_datos(clientes):
    """Guarda la lista de diccionarios en el archivo CSV para mantener los datos entre ejecuciones."""
    try:
        with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(clientes)
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def crear_cliente(clientes):
    """Registra un nuevo cliente validando tipos de datos."""
    print("\n--- Registrar Nuevo Cliente ---")
    try:
        id_cliente = input("Ingrese el ID (único) del cliente: ").strip()

        # Validar que el ID no exista en la lista actual
        for c in clientes:
            if c['id'] == id_cliente:
                print("Error: Ya existe un cliente con ese ID.")
                return

        nombre = input("Ingrese el nombre del cliente: ").strip()
        edad = int(input("Ingrese la edad del cliente: "))
        plan = input("Ingrese el tipo de plan (mensual, trimestral, anual): ").strip().lower()
        estado = input("Ingrese el estado (activo/inactivo): ").strip().lower()

        nuevo_cliente = {
            'id': id_cliente,
            'nombre': nombre,
            'edad': edad,
            'plan': plan,
            'estado': estado
        }

        clientes.append(nuevo_cliente)
        guardar_datos(clientes)
        print("¡Cliente registrado con éxito!")

    except ValueError:
        print("Error: La edad debe ser un número entero válido.")

def listar_clientes(clientes):
    """Lista todos los clientes registrados en consola."""
    print("\n--- Lista de Clientes ---")
    if not clientes:
        print("No hay clientes registrados en el sistema.")
        return

    for c in clientes:
        print(f"ID: {c['id']} | Nombre: {c['nombre']} | Edad: {c['edad']} | Plan: {c['plan'].capitalize()} | Estado: {c['estado'].capitalize()}")

def buscar_cliente(clientes):
    """Busca un cliente por coincidencia de ID o nombre."""
    print("\n--- Buscar Cliente ---")
    termino = input("Ingrese el ID o el nombre del cliente a buscar: ").strip().lower()

    encontrados = []
    for c in clientes:
        if termino == c['id'].lower() or termino in c['nombre'].lower():
            encontrados.append(c)

    if encontrados:
        for c in encontrados:
            print(f"ID: {c['id']} | Nombre: {c['nombre']} | Edad: {c['edad']} | Plan: {c['plan']} | Estado: {c['estado']}")
    else:
        print("No se encontró ningún cliente con esos datos.")

def actualizar_cliente(clientes):
    """Actualiza la información de un cliente existente pidiendo los nuevos datos."""
    print("\n--- Actualizar Cliente ---")
    id_buscar = input("Ingrese el ID del cliente que desea actualizar: ").strip()

    for c in clientes:
        if c['id'] == id_buscar:
            print(f"Cliente encontrado: {c['nombre']}. Deje en blanco si no desea cambiar el campo.")
            try:
                nuevo_nombre = input(f"Nuevo nombre ({c['nombre']}): ").strip()
                nueva_edad_str = input(f"Nueva edad ({c['edad']}): ").strip()
                nuevo_plan = input(f"Nuevo plan ({c['plan']}): ").strip()
                nuevo_estado = input(f"Nuevo estado ({c['estado']}): ").strip()

                if nuevo_nombre: c['nombre'] = nuevo_nombre
                if nueva_edad_str: c['edad'] = int(nueva_edad_str)
                if nuevo_plan: c['plan'] = nuevo_plan.lower()
                if nuevo_estado: c['estado'] = nuevo_estado.lower()

                guardar_datos(clientes)
                print("¡Información del cliente actualizada con éxito!")
                return
            except ValueError:
                print("Error: Valor inválido ingresado durante la actualización.")
                return

    print("No se encontró un cliente con ese ID.")

def eliminar_cliente(clientes):
    """Elimina un cliente del sistema mediante su ID."""
    print("\n--- Eliminar Cliente ---")
    id_buscar = input("Ingrese el ID del cliente a eliminar: ").strip()

    for i in range(len(clientes)):
        if clientes[i]['id'] == id_buscar:
            confirmacion = input(f"¿Está seguro de que desea eliminar a {clientes[i]['nombre']}? (s/n): ").strip().lower()
            if confirmacion == 's':
                eliminado = clientes.pop(i)
                guardar_datos(clientes)
                print(f"Cliente '{eliminado['nombre']}' eliminado del sistema.")
            else:
                print("Operación cancelada.")
            return

    print("No se encontró un cliente con ese ID.")

def menu():
    """Función principal que despliega el menú en consola y gestiona la interacción."""
    clientes = cargar_datos()

    while True:
        print("\n" + "="*30)
        print(" GESTIÓN DE CLIENTES - GIMNASIO")
        print("="*30)
        print("1. Crear cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente")
        print("4. Actualizar cliente")
        print("5. Eliminar cliente")
        print("6. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            crear_cliente(clientes)
        elif opcion == '2':
            listar_clientes(clientes)
        elif opcion == '3':
            buscar_cliente(clientes)
        elif opcion == '4':
            actualizar_cliente(clientes)
        elif opcion == '5':
            eliminar_cliente(clientes)
        elif opcion == '6':
            print("Guardando datos y saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

# Punto de ejecución
if __name__ == "__main__":
    menu()