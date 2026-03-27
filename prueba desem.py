import json
import os

# Archivo donde se guardarán los datos (Persistencia)
ARCHIVO_JSON = 'clientes_gimnasio.json'

# ==========================================
# FUNCIONES DE PERSISTENCIA (JSON)
# ==========================================
def cargar_datos():
    """Carga los datos de los clientes desde el archivo JSON al iniciar."""
    if os.path.exists(ARCHIVO_JSON):
        try:
            with open(ARCHIVO_JSON, 'r') as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"Error al cargar la base de datos: {e}")
            return []
    return [] # Retorna lista vacía si el archivo no existe

def guardar_datos(clientes):
    """Guarda la lista de clientes en el archivo JSON."""
    try:
        with open(ARCHIVO_JSON, 'w') as archivo:
            json.dump(clientes, archivo, indent=4)
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

# ==========================================
# FUNCIONES DEL CRUD (Crear, Leer, Actualizar, Borrar)
# ==========================================
def crear_cliente(clientes):
    print("\n--- REGISTRAR NUEVO CLIENTE ---")
    try:
        # Validamos que el ID sea un número entero
        id_cliente = int(input("Ingrese el ID (único y numérico): "))
        
        # Validamos que el ID no exista ya en la lista
        for c in clientes:
            if c['id'] == id_cliente:
                print("❌ Error: Ya existe un cliente con ese ID.")
                return

        nombre = input("Ingrese el nombre del cliente: ").strip()
        edad = int(input("Ingrese la edad del cliente: "))
        
        # Validamos el tipo de plan
        plan = input("Ingrese tipo de plan (mensual/trimestral/anual): ").strip().lower()
        if plan not in ['mensual', 'trimestral', 'anual']:
            print("❌ Error: Tipo de plan no válido. Se asignará 'mensual' por defecto.")
            plan = 'mensual'
            
        estado = input("Ingrese el estado (activo/inactivo): ").strip().lower()
        if estado not in ['activo', 'inactivo']:
            estado = 'activo'

        # Creamos el diccionario del cliente
        nuevo_cliente = {
            'id': id_cliente,
            'nombre': nombre,
            'edad': edad,
            'plan': plan,
            'estado': estado
        }
        
        clientes.append(nuevo_cliente)
        guardar_datos(clientes) # Guardamos el cambio en el JSON
        print(f"✅ Cliente {nombre} registrado con éxito.")
        
    except ValueError:
        print("❌ Error: Has ingresado un valor inválido (ej. letras donde van números). Intenta de nuevo.")

def listar_clientes(clientes):
    print("\n--- LISTA DE CLIENTES ---")
    if not clientes:
        print("No hay clientes registrados en el sistema.")
        return

    # Usamos un bucle for para mostrar los datos de la lista de diccionarios
    for c in clientes:
        print(f"ID: {c['id']} | Nombre: {c['nombre']} | Edad: {c['edad']} | Plan: {c['plan'].capitalize()} | Estado: {c['estado'].capitalize()}")

def buscar_cliente(clientes):
    print("\n--- BUSCAR CLIENTE ---")
    termino = input("Ingrese el ID o Nombre del cliente a buscar: ").strip().lower()
    
    encontrado = False
    for c in clientes:
        # Buscamos coincidencias convirtiendo el ID a string y el nombre a minúsculas
        if str(c['id']) == termino or c['nombre'].lower() == termino:
            print("\n✅ Cliente encontrado:")
            print(f"ID: {c['id']}")
            print(f"Nombre: {c['nombre']}")
            print(f"Edad: {c['edad']}")
            print(f"Plan: {c['plan'].capitalize()}")
            print(f"Estado: {c['estado'].capitalize()}")
            encontrado = True
            break
            
    if not encontrado:
        print("❌ Cliente no encontrado.")

def actualizar_cliente(clientes):
    print("\n--- ACTUALIZAR CLIENTE ---")
    try:
        id_buscar = int(input("Ingrese el ID del cliente que desea actualizar: "))
        
        for c in clientes:
            if c['id'] == id_buscar:
                print(f"Actualizando datos de: {c['nombre']} (Presiona Enter para dejar el valor actual)")
                
                # Pedimos nuevos datos, si el input está vacío, dejamos el valor anterior
                nuevo_nombre = input(f"Nuevo nombre ({c['nombre']}): ").strip()
                if nuevo_nombre:
                    c['nombre'] = nuevo_nombre
                
                nueva_edad = input(f"Nueva edad ({c['edad']}): ").strip()
                if nueva_edad:
                    c['edad'] = int(nueva_edad)
                
                nuevo_plan = input(f"Nuevo plan ({c['plan']}): ").strip().lower()
                if nuevo_plan in ['mensual', 'trimestral', 'anual']:
                    c['plan'] = nuevo_plan
                    
                nuevo_estado = input(f"Nuevo estado ({c['estado']}): ").strip().lower()
                if nuevo_estado in ['activo', 'inactivo']:
                    c['estado'] = nuevo_estado
                
                guardar_datos(clientes)
                print("✅ Información actualizada correctamente.")
                return
                
        print("❌ No se encontró ningún cliente con ese ID.")
    except ValueError:
        print("❌ Error: El ID y la edad deben ser números.")

def eliminar_cliente(clientes):
    print("\n--- ELIMINAR CLIENTE ---")
    try:
        id_buscar = int(input("Ingrese el ID del cliente que desea eliminar: "))
        
        for i in range(len(clientes)):
            if clientes[i]['id'] == id_buscar:
                # Usamos pop() para remover el elemento de la lista por su índice
                cliente_eliminado = clientes.pop(i)
                guardar_datos(clientes)
                print(f"✅ Cliente '{cliente_eliminado['nombre']}' eliminado del sistema.")
                return
                
        print("❌ No se encontró ningún cliente con ese ID.")
    except ValueError:
        print("❌ Error: El ID debe ser un número entero.")

# ==========================================
# MENÚ PRINCIPAL Y FLUJO DE CONTROL
# ==========================================
def mostrar_menu():
    print("\n" + "="*30)
    print(" GIMNASIO - GESTIÓN DE CLIENTES")
    print("="*30)
    print("1. Crear cliente")
    print("2. Listar clientes")
    print("3. Buscar cliente")
    print("4. Actualizar cliente")
    print("5. Eliminar cliente")
    print("6. Salir")
    print("="*30)

def main():
    # Cargar datos guardados al iniciar la aplicación
    lista_clientes = cargar_datos()
    
    # Bucle infinito para mantener el programa corriendo hasta que el usuario elija "Salir"
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-6): ").strip()
        
        if opcion == '1':
            crear_cliente(lista_clientes)
        elif opcion == '2':
            listar_clientes(lista_clientes)
        elif opcion == '3':
            buscar_cliente(lista_clientes)
        elif opcion == '4':
            actualizar_cliente(lista_clientes)
        elif opcion == '5':
            eliminar_cliente(lista_clientes)
        elif opcion == '6':
            print("Guardando datos y cerrando el sistema... ¡Hasta luego!")
            guardar_datos(lista_clientes)
            break
        else:
            print("❌ Opción no válida. Por favor, elige un número del 1 al 6.")

# Punto de entrada del script
if __name__ == "__main__":
    main()