import xlrd
from xlrd import sheet
import conexion
import sqlite3
import variables
import datetime
import time
import funcionesreserva

def insertarprecios(fila):
    try:
        conexion.cur.execute('update precios set desayuno=?,comida=?,parking=?',fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def insertarservicio(codreser,concepto):
    try:
        conexion.cur.execute('select '+concepto+' from precios')
        precio = conexion.cur.fetchone()
        conexion.conex.commit()
        conexion.cur.execute('insert into servicios(Concepto,Precio,CodReser) values("'+concepto+'",'+str(precio[0])+','+codreser+')')
        print("Insertado")
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    """
            Se conecta a la bd y consulta la tabla habitaciones y los guarda en un listado

            Args:

            Returns:
                listado, es una lista con los datos de las habitaciones.
        """
    try:
        conexion.cur.execute('select * from servicios where CodReser='+variables.filaser[0].get_text()+'')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarservi(listservi):
    """
            Refresca los datos que muestra el treeview

            Args:
                listservi: Contiene un listado de servicios a actualizar.

            Returns:
                void.
        """
    try:
        noches = funcionesreserva.calculadias()
        variables.listado = listar()
        variables.listservi.clear()
        variables.listfact.clear()
        preciohabi=encontrarpreciohabitacionporcodigoreserva(variables.filaser[0].get_text())
        total=preciohabi*float(noches)
        variables.listfact.append(["Noches",noches,str(preciohabi),str(total)])
        for registro in variables.listado:
            variables.listservi.append(registro[0:4])
            variables.listfact.append([registro[1],"",str(registro[2]),str(registro[2]*float(noches))])
            
    except Exception as e:
        print(e)
        print("error en cargar treeview servicios")

def bajaservi(codigo):
    try:
        conexion.cur.execute('delete from servicios where codigo = '+codigo+'')
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        print("error baja boton servicio")
        conexion.conexion.rollback()

def insertarservicioadicional(codreser,concepto,precio):
    try:
        conexion.cur.execute('insert into servicios(Concepto,Precio,CodReser) values("'+concepto+'",'+precio+','+codreser+')')
        print("Insertado")
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        print("hola")
        conexion.conex.rollback()

def encontrarpreciohabitacionporcodigoreserva(codres):
    try:
        conexion.cur.execute('select habitacion from reservas where codigo="'+codres+'"')
        habi=conexion.cur.fetchone()
        conexion.conex.commit()
        conexion.cur.execute('select precio from habitaciones where numero='+habi[0]+'')
        precio = conexion.cur.fetchone()
        conexion.conex.commit()
        return precio[0]
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def calcularPreciosServicios():
    """
    esta funcion carga el treeview con los datos de la tabla servicios
    :param listFactura: lista de los servicios de la base de datos
    :return: Void
    """
    try:
        preciosSinIva=0
        iva=0
        for registro in variables.listfact:
            preciosSinIva= preciosSinIva + float(registro[3])
        for registro in variables.listfact:
            if registro[0] =="Noches" or registro[0] =="Desayuno" or registro[0] =="Comida" or registro[0] =="Parking" :
                iva= iva+float(registro[3])*0.10
            else:
                iva=iva+ float(registro[3])*0.21


        preciosConIva= preciosSinIva+iva
        variables.subtotal.set_text(str(preciosSinIva))
        variables.ivafactura.set_text(str("{0:.2f}".format(iva)))
        variables.totalfactura.set_text(str(preciosConIva))

    except Exception as e:
        print("error en calcular precios")
        print(e)