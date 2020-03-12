# coding=utf-8
"""Módulo que gestiona los clientes.
"""

import xlrd
from xlrd import sheet
import conexion
import sqlite3
import variables
import datetime
import time

def limpiarentry(fila):
    """
        Limpia las entradas de texto.

        Args:
            fila: Contiene un listado de widgets de clientes.

        Returns:
            void.
    """
    variables.menserror[1].set_text('')
    for i in range(len(fila)):
        fila[i].set_text('')


def validoDNI(dni):
    """
        Controla que el dni es correcto.

        Args:
            dni: Valor del dni del cliente.

        Returns:
             devuelve un booleano.
    """
    try:
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        dig_ext = "XYZ"
        reemp_dig_ext = {'X':'0','Y':'1','Z':'2'}
        numeros = "1234567890"
        dni = dni.upper()
        if len(dni) == 9:
            dig_control=dni[8]
            dni = dni[:8]
            if dni[0] in dig_ext:
                dni = dni.replace(dni[0],reemp_dig_ext[dni[0]])
            return len(dni)==len([n for n in dni if n in numeros]) and tabla[int(dni)%23]==dig_control
        return False
    except:
        print("Error en la aplicación")
        return None

def insertarcli(fila):
    """
       Se conecta a la bd e inserta un cliente.

       Args:
           fila: Contiene un listado con los valores de clientes.

       Returns:
           void.
    """
    try:
        conexion.cur.execute('insert into clientes(dni,apel,nome, data) values(?,?,?,?)',fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    """
        Se conecta a la bd y consulta la tabla clientes y los guarda en un listado

        Args:

        Returns:
            listado, es una lista con los datos de los clientes.
    """
    try:
        conexion.cur.execute('select * from clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarcli(listclientes):
    """
        Refresca los datos que muestra el treeview

        Args:
            listclientes: Contiene un listado de clientes a actualizar.

        Returns:
            void.
    """
    try:
        variables.listado = listar()
        variables.listclientes.clear()
        for registro in variables.listado:
            variables.listclientes.append(registro[1:5])
    except:
        print("error en cargar treeview")

def selectcli(dni):
    """
        Se conecta a la bd y consulta la tabla clientes para encontrar uno específico a partir de un dni

        Args:
            dni: Contiene el dni para encontrar el cliente

        Returns:
            listado, es una lista con los datos del cliente.
    """
    try:
        conexion.cur.execute('select id from clientes where dni=?',(dni,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajacli(dni):
    """
        Se conecta a la bd y borra una fila de la tabla clientes a partir de un dni determinado.

        Args:
            dni: Contiene el dni para encontrar el cliente

        Returns:
            void.
    """
    try:
        conexion.cur.execute('delete from clientes where dni = ?',(dni,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        print("error baja boton cliente")
        conexion.conexion.rollback()

def modifcli(registro,cod):
    """
        Se conecta a la bd y modifica una fila utilizando los datos que se le pasan en un listado y utilizando el codigo de cliente para encontrar el que se debe modificar.

        Args:
            registro: Contiene un listado con los diferentes campos que tiene un cliente.
            cod: Contiene el codigo de cliente que se quiere modificar.

        Returns:
            void.
    """
    try:
        conexion.cur.execute('update clientes set dni = ?, apel = ?, nome = ?, data = ? where id=?',(registro[0],registro[1],registro[2],registro[3],cod,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#def fecha():
    #variables.menserror[2].set_text(str(datetime.date.today()))
    #variables.menserror[2].set_text(str(time.ctime()))

def apelnomfac(dni):
    """
        Se conecta a la bd y recibe los apellidos y el nombre de un cliente con un determinado dni.

        Args:
            dni: Contiene el dni para encontrar el cliente

        Returns:
            apelnome: Contiene los apellidos y el nombre del cliente seleccionado.
    """
    try:
        conexion.cur.execute('select apel, nome from clientes where dni = ?', (dni,))
        apelnome = conexion.cur.fetchone()
        conexion.conex.commit()
        return apelnome
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def formatear_fecha_excel(celda):
    """
        Pone la fecha en el formato decidido.

        Args:
            celda: Contiene la fecha a formatear

        Returns:
            fecha_formateada: Contiene la fecha formateada.
    """
    archivo_excel = xlrd.open_workbook("clientes.xls")
    fecha_formateada = datetime.datetime(*xlrd.xldate_as_tuple(celda.value, archivo_excel.datemode))
    return fecha_formateada.strftime('%d/%m/%Y')

def insertarcliexcel(celdas_clientes):
    """
        Inserta los clientes que le llegan a traves de celdas_clientes.

        Args:
            celdas_clientes: Contiene todos los datos de un cliente.

        Returns:
            void.
    """
    cliente = []
    for celda_cliente in celdas_clientes:
        if celda_cliente.ctype == sheet.XL_CELL_DATE:
            cliente.append(formatear_fecha_excel(celda_cliente))
        else:
            cliente.append(celda_cliente.value)
    insertarcli(cliente)