from datetime import datetime # Importación del módulo datetime para manejar fechas
import logging # Importación del módulo logging para manejar registros de eventos


# Implementación de la configuración del sistema de logging
logging.basicConfig(
    filename='clinica_veterinaria.log', # Archivo donde se guardarán los logs
    level=logging.INFO, # Nivel de logging INFO para registrar eventos informativos
    format='%(asctime)s - %(levelname)s - %(message)s') # Formato de los mensajes de los evventos o logs


# Definición de la clase Dueño que almacena información del dueño de la mascota
class Dueno:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    # Método para mostrar la información del dueño
    def __str__(self):
        return f"Dueño: {self.nombre}, Teléfono: {self.telefono}, Dirección: {self.direccion}"


# Definición de la clase Mascota que almacena información de la mascota y su dueño
class Mascota:
    def __init__(self, nombre, especie, raza, edad, dueno):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno = dueno
        self.consultas = []

    def agregar_consulta(self, consulta):
        self.consultas.append(consulta)

    # Método para mostrar la información de la mascota y su dueño
    def __str__(self):
        return (f"Nombre: {self.nombre}, Especie: {self.especie}, Raza: {self.raza}, "
                f"Edad: {self.edad}, {self.dueno}")


# Definición de la clase Consulta que almacena información de una consulta veterinaria
class Consulta:
    def __init__(self, fecha, motivo, diagnostico, mascota):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota

    # Método para mostrar la información de la consulta veterinaria
    def __str__(self):
        return (f"Fecha: {self.fecha}, Motivo consulta: {self.motivo}, "
                f"Diagnóstico: {self.diagnostico}")


# Lista vacía para almacenar todas las mascotas registradas
mascotas = []

# Función para registrar una nueva mascota y su dueño
def registrar_mascota():
    
    # Validación de posibles errores en la entradas de datos
    try:
        print("\n--- Registrar Nueva Mascota ---")
        nombre = input("Nombre de la mascota: ")
        especie = input("Especie: ")
        raza = input("Raza: ")
        edad = int(input("Edad: "))
        if edad < 0:
            raise ValueError("La edad no puede ser un númerio negativo.")
        
        print("\n--- Datos del Dueño ---")
        nombre_dueno = input("Nombre del dueño: ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        
        dueno = Dueno(nombre_dueno, telefono, direccion)
        mascota = Mascota(nombre, especie, raza, edad, dueno)
        mascotas.append(mascota)
        print("\n¡Mascota registrada exitosamente!\n")
        
        logging.info(f"Mascota registrada exitosamente: {mascota.nombre}, Dueño: {dueno.nombre}")
    except ValueError as ve: # Captura de errores de valor
        print(f"Error: {ve}") 
        logging.error(f"Error al registrar mascota: {ve}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de jecución
        print("Error al registrar la mascota.")
        logging.exception("Excepción general al registrar mascota.") # Registro de la excepción general       


# Función para registrar una consulta veterinaria para una mascota
def registrar_consulta():
    
    # Validación de posibles errores en la entradas de datos
    try:
        print("\n--- Registrar Consulta ---")
        if not mascotas:
            print("\nNo hay mascotas registradas.\n")
            return
        
        listar_mascotas()
        idmascota = int(input("Seleccione el número de la mascota: ")) - 1
        if not (0 <= idmascota < len(mascotas)):
            raise IndexError("Número de mascota no válido.")
        while True:
            fecha = input("Fecha (YYYY-MM-DD): ")
            try:
                datetime.strptime(fecha, "%Y-%m-%d")  # Validar formato de fecha
                break
            except ValueError:
                print("Formato de fecha inválido. Intente nuevamente.")
                
        motivo = input("Motivo de la consulta: ")
        diagnostico = input("Diagnóstico: ")
        
        consulta = Consulta(fecha, motivo, diagnostico, mascotas[idmascota])
        mascotas[idmascota].agregar_consulta(consulta)
        print("\n¡Consulta registrada exitosamente!\n")
        
        logging.info(f"Consulta registrada para {mascotas[idmascota].nombre} en {fecha}")
    except ValueError: # Captura de errores de valor
        print("Entrada inválida. Por favor ingrese un número válido.")
        logging.error("Valor inválido al seleccionar mascota para realizar consulta.") # Registro del error
    except IndexError as ie: # Captura de errores de índice
        print(f"Error: {ie}")
        logging.warning(f"El número seleccionado está fuera del rango: {ie}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
        print("Ocurrió un error al registrar la consulta.")
        logging.exception("Excepción general al registrar consulta.") # Registro de la excepción general
        
        
# Función para mostrar todas las mascotas registradas
def listar_mascotas():
    print("\n--- Lista de Mascotas ---")
    if not mascotas:
        print("No hay mascotas registradas.\n")
        logging.info("Listado solicitado con éxito. No hay mascotas registradas") # Registro del evento ocurrido
        return
    for i, mascota in enumerate(mascotas, 1):
        print(f"{i}. {mascota}")
        

# Función para mostrar el historial de consultas veterinarias de una mascota
def ver_historial_consultas():
    
    # Validación de posibles errores en la consulta del historial
    try:
        print("\n--- Historial de Consultas ---")
        if not mascotas:
            print("\nNo hay mascotas registradas.\n")
            logging.info("Listado solicitado con éxito. No hay consultas registradas.")
            return
        
        listar_mascotas()
        idmascota = int(input("Seleccione el número (ID) de la mascota: ")) - 1
        if not (0 <= idmascota < len(mascotas)):
            raise IndexError("ID de mascota no válido.")   
             
        mascota = mascotas[idmascota]
        if not mascota.consultas:
            print("\nNo hay consultas registradas para esta mascota.\n")
            logging.info(f"No hay consultas para la mascota {mascota.nombre}")
        else:
            print(f"\nHistorial de consultas para {mascota.nombre}:")
            for consulta in mascota.consultas:
                print(consulta)
    except ValueError: # Captura de errores de valor
        print("Entrada inválida. Por favor ingrese un número válido.")
        logging.error("Valor inválido para ver historial de consultas.") # Registro del error
    except IndexError as ie: # Captura de errores de índice
        print(f"Error: {ie}")
        logging.warning(f"El índice seleccionado está fuera del rango: {ie}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
        print("Ocurrió un error al ver el historial.")
        logging.exception("Excepción general al ver historial.") # Registro de la excepción general
        


# Menú principal de la aplicación
def menu():
    logging.info("Inicio de la aplicación.") # Registro del inicio de la aplicación
    while True:
        print("\n--- Clínica Veterinaria Amigos Peludos ---")
        print("1. Registrar mascota")
        print("2. Agendar consulta")
        print("3. Listar mascotas")
        print("4. Ver historial de consultas de una mascota específica")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        
        # Validación de posibles errores en la entrada del menú
        try:
            if opcion == "1":
                registrar_mascota()
            elif opcion == "2":
                registrar_consulta()
            elif opcion == "3":
                listar_mascotas()
            elif opcion == "4":
                ver_historial_consultas()
            elif opcion == "5":
                print("¡Hasta luego!")
                logging.info("Cierre de la aplicación.")  # Registro del cierre de la aplicación
                break
            else:
                print("Opción inválida. Intente de nuevo.\n")
        except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
            print("Error en el menú principal.")
            logging.exception("Error en el menú principal") # Registro de la excepción general


# Punto de entrada de la aplicación
if __name__ == "__main__":
    menu()