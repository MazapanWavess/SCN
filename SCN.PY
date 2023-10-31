import sqlite3            
import datetime

#-------------------------------------------------------------------------------------
#ESTABLECEMOS CONEXION CON BASE DE DATOS Y EJECUTAMOS COMANDOS

conexion = sqlite3.connect('SCP.db')
cursor = conexion.cursor()

#-------------------------------------------------------------------------------------
#SE CREAN TABLAS CON LOS NOMBRES 'PRODUCTOS' Y 'VENTAS' DENTRO DE LA VASE DE DATOS. :3

cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    precio REAL,
                    inversion REAL,
                    cantidad INTEGER,
                    precio_unidad REAL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER,
                    cantidad INTEGER,
                    fecha DATE,
                    venta REAL,
                    ganancia REAL,
                    FOREIGN KEY (producto_id) REFERENCES productos(id)
                )''')

#-------------------------------------------------------------------------------------

#SE DEFINEN VARIAS FUNCIONES CON UNA TAREA EN ESPECIFICA

#SE DA LA BIENVENIDA

def bienvenida():
    print("\n--- BIENVENIDO EMPRENDEDOR ---\n")
    nombre_usuario= input("Dime tu nombre emprendedor:")
    nombre_empresa = input("Dame el nombre de tu negocio:")
    print(" ")
    print(f"Muy bien {nombre_usuario}, comenzemos a organizar tu negocio. ")
    print(" ")

#-------------------------------------------------------------------------------------
#PIDE LOS DATOS DE UN PRODUCTO Y LO INSERTA EN LA TABLA PRODUCTOS

def agregar_producto():
    nombre = input("\nIngrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    inversion = float(input("Ingrese la inversión del producto: "))
    cantidad = int(input("Ingrese la cantidad comprada del producto: "))
    precio_unidad= inversion / cantidad

    cursor.execute("INSERT INTO productos (nombre, precio, inversion, cantidad, precio_unidad) VALUES (?, ?, ?, ?, ?)",
                    (nombre, precio, inversion, cantidad, precio_unidad))
    conexion.commit()
    print("Producto agregado con éxito.")

#-------------------------------------------------------------------------------------
#MUESTRA TODOS LOS PRODUCTOS CON SUS ESPECIFICACIONES Y LOS MUESTRA EN FORMA DE LISTA

def listar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if productos:
        print("\nLista de productos:")
        for producto in productos:
            print(f"ID: {producto[0]}\n Nombre: {producto[1]}\n Precio comercial: {producto[2]}\n Inversión: {producto[3]}\n Cantidad: {producto[4]}\n Precio por unidad: {producto[5]}")
            print("-------------------------")
    else:
        print("No hay productos registrados.")

#-------------------------------------------------------------------------------------
#MUESTRA UN PRODUCTO EN ESPECIFICO SEGUN SEA EL ID INGRESADO

def ver_producto():
    id_producto = int(input("\nIngrese el ID del producto: "))

    cursor.execute("SELECT * FROM productos WHERE id=?", (id_producto,))
    producto = cursor.fetchone()

    if producto:
        print(f"\nDetalles del Producto:")
        print(f"Nombre: {producto[1]}")
        print(f"Precio comercial: {producto[2]}")
        print(f"Inversión requerida: {producto[3]}")
        print(f"Cantidad: {producto[4]}")
        print(f"precio por unidad: {producto[5]} ")
    else:
        print("El producto no se encontró en la lista.\n")

#-------------------------------------------------------------------------------------
# PERMITE DAR VENTA A UN PRODUCTO Y REGISTRA LA VENTA EN LA TABLA DE VENTAS

def vender_producto():
    id_producto = int(input("\nIngrese el ID del producto a vender: "))
    cantidad = int(input("Ingrese la cantidad vendida: "))
    fecha = datetime.date.today()

    cursor.execute("SELECT * FROM productos WHERE id=?", (id_producto,))
    producto = cursor.fetchone()

    if producto:
        if producto[4] >= cantidad:
            venta = cantidad * producto[2]
            ganancia = (producto[2] * cantidad) - (producto[5]*cantidad)

            nueva_cantidad = producto[4] - cantidad
            cursor.execute("UPDATE productos SET cantidad=? WHERE id=?", (nueva_cantidad, id_producto))

            cursor.execute("INSERT INTO ventas (producto_id, cantidad, fecha, ganancia, venta) VALUES (?, ?, ?, ?, ?)",
                            (id_producto, cantidad, fecha, ganancia, venta))
            conexion.commit()
            print(f"Venta realizada con éxito. Ganancia: {ganancia}")
        else:
            print("No hay suficiente cantidad de producto disponible.\n")
    else:
        print("El producto no se encontró en la lista.\n")

#-------------------------------------------------------------------------------------
# PERMITE MOSTRAR LA VENTAS REALIZADAS EN EL DIA ACTUAL

def ver_ventas_dia():
    fecha_consulta = datetime.date.today()

    cursor.execute("SELECT * FROM ventas WHERE fecha=?", (fecha_consulta,))
    ventas = cursor.fetchall()

    if ventas:
        total_ventas = sum([venta[2] for venta in ventas])
        print(f"\nVentas del día {fecha_consulta}:")
        for venta in ventas:
            print(f"ID: {venta[0]}, Producto ID: {venta[1]}, Cantidad: {venta[2]}, Venta: {venta[4]} , Ganancia: {venta[5]} ,Fecha: {venta[3]}")
        print(f"Total de ventas: {total_ventas}")
    else:
        print("No se encontraron ventas para la fecha especificada.")

#-------------------------------------------------------------------------------------
#PERMITE VER LA VENTA DE DIAS ANTERIORES 

def ver_ventas_anteriores():
    cursor.execute("SELECT DISTINCT fecha FROM ventas")
    fechas = cursor.fetchall()

    if fechas:
        print("\nFechas disponibles:")
        for fecha in fechas:
            print(fecha[0])
        fecha_consulta = input("\nIngrese la fecha (formato: YYYY-MM-DD): ")

        cursor.execute("SELECT * FROM ventas WHERE fecha=?", (fecha_consulta,))
        ventas = cursor.fetchall()

        if ventas:
            total_ventas = sum([venta[2] for venta in ventas])
            print(f"\nVentas del día {fecha_consulta}:")
            for venta in ventas:
                print(f"ID: {venta[0]}, Producto ID: {venta[1]}, Cantidad: {venta[2]}, Venta: {venta[4]} , Ganancia: {venta[5]} ,Fecha: {venta[3]}")
            print(f"Total de ventas: {total_ventas}")
        else:
            print("No se encontraron ventas para la fecha especificada.")
    else:
        print("No hay ventas registradas.")

#-------------------------------------------------------------------------------------
# FUNCION PRINCIPAL QUE EJECUTA EL PROGRAMA

def menu():
    bienvenida()
    while True:
        print("\n-------- SCN --------")
        print("1. Agregar Producto")
        print("2. Lista Productos")
        print("3. Ver Detalles de un Producto")
        print("4. Vender Producto")
        print("5. Ver Ventas del Día")
        print("6. Ver Ventas de Dias Anteriores")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            listar_productos()
        elif opcion == '3':
            ver_producto()
        elif opcion == '4':
            vender_producto()
        elif opcion == '5':
            ver_ventas_dia()
        elif opcion == '6':
            ver_ventas_anteriores()
        elif opcion == '0':
            print("\n HASTA PRONTO \n")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

menu()

#-------------------------------------------------------------------------------------
#CIERRA LA CONEXION CON LA BASE DE DATOS

conexion.close()                 
