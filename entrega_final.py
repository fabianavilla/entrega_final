import sqlite3

# Crear la base de datos y tabla si no existen
def inicializar_base_de_datos():
    con = sqlite3.connect("inventario.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        categoria TEXT
    )
    """)
    con.commit()
    con.close()

# Llamar a la función antes de iniciar
inicializar_base_de_datos()

def conectar():
    return sqlite3.connect('inventario.db')

def registrar_productos():
    # Registrar un nuevo producto 
    con = conectar()
    cur = con.cursor()
    try:
        nombre = input("Ingrese el nombre del producto: ")
        descripcion = input("Ingrese una descripción del producto: ")
        cantidad = int(input("Ingrese la cantidad del producto: "))
        precio = float(input("Ingrese el precio del producto: "))
        categoria = input("Ingrese la categoría del producto: ")

        cur.execute("""
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, categoria))
        con.commit()
        print("Producto registrado exitosamente.\n")
    except ValueError:
        print("Por favor, ingresá valores válidos.\n")
    finally:
        con.close()

def mostrar_productos():
    # Mostrar todos los productos 
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()

    print("\nListado de Productos\n")
    print("ID | Nombre       | Descripción       | Cantidad | Precio  | Categoría")
    print("-" * 60)
    for producto in productos:
        print(f"{producto[0]:<3} | {producto[1]:<12} | {producto[2]:<15} | {producto[3]:<8} | ${producto[4]:<7.2f} | {producto[5]}")
    print(f"\nSe encontraron {len(productos)} producto(s).\n")
    con.close()

def actualizar_producto():
    # Actualizar la cantidad de producto
    mostrar_productos()
    con = conectar()
    cur = con.cursor()
    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: "))
        nueva_cantidad = int(input("Ingrese la nueva cantidad del producto: "))
        cur.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))
        con.commit()
        print("Producto actualizado exitosamente.\n")
    except ValueError:
        print("Por favor, ingresá valores válidos.\n")
    finally:
        con.close()

def eliminar_producto():
    # Eliminar un producto 
    mostrar_productos()
    con = conectar()
    cur = con.cursor()
    try:
        id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))
        cur.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        con.commit()
        print("Producto eliminado exitosamente.\n")
    except ValueError:
        print("Por favor, ingresá un ID válido.\n")
    finally:
        con.close()

def buscar_producto():
    # Buscar un producto 
    criterio = input("Ingrese el criterio de búsqueda (ID, nombre o categoría): ").lower()
    valor = input("Ingrese el valor a buscar: ")
    con = conectar()
    cur = con.cursor()
    if criterio == "id":
        cur.execute("SELECT * FROM productos WHERE id = ?", (valor,))
    elif criterio == "nombre":
        cur.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + valor + '%',))
    elif criterio == "categoría":
        cur.execute("SELECT * FROM productos WHERE categoria LIKE ?", ('%' + valor + '%',))
    else:
        print("Criterio no válido.\n")
        return
    producto = cur.fetchall()
    if producto:
        print("Resultados:")
        for p in producto:
            print(f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}")
    else:
        print("No se encontraron productos.\n")
    con.close()

def reporte_bajo_stock():
    """Generar reporte de bajo stock."""
    try:
        limite = int(input("Ingrese el límite de stock bajo: "))
    except ValueError:
        print("Por favor, ingresá un número válido.\n")
        return
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cur.fetchall()
    if productos:
        print("Productos con bajo stock:")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}")
    else:
        print("No hay productos con bajo stock.\n")
    con.close()

def menu_principal():
    """Menú principal de la aplicación."""
    while True:
        print("\nMenú Principal")
        print("1. Agregar producto")
        print("2. Ver productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Reporte bajo stock")
        print("7. Salir")
        try:
            opcion = int(input("Seleccioná una opción: "))
        except ValueError:
            print("Por favor, ingresá un número válido.\n")
            continue
        if opcion == 1:
            registrar_productos()
        elif opcion == 2:
            mostrar_productos()
        elif opcion == 3:
            actualizar_producto()
        elif opcion == 4:
            eliminar_producto()
        elif opcion == 5:
            buscar_producto()
        elif opcion == 6:
            reporte_bajo_stock()
        elif opcion == 7:
            print("Gracias por usar la aplicación!\n")
            break
        else:
            print("Opción no válida, intentá de nuevo.\n")

# Ejecutar la aplicación
if __name__ == "__main__":
    menu_principal()
