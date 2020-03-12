# coding=utf-8
"""Módulo que gestiona las habitaciones.
"""
import conexion
import sqlite3
import variables
import datetime
import time

def limpiarentry(fila):
    """
            Limpia las entradas de texto.

            Args:
                fila: Contiene un listado de widgets de habitaciones.

            Returns:
                void.
        """
    fila[0].set_text('')
    fila[2].set_active(True)
    fila[4].set_text('')


def insertarhabi(fila):
    """
           Se conecta a la bd e inserta una habitacion.

           Args:
               fila: Contiene un listado con los valores de habitaciones.

           Returns:
               void.
        """
    try:
        conexion.cur.execute('insert into habitaciones(numero,tipo,precio,libre) values(?,?,?,?)',fila)
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
        conexion.cur.execute('select * from habitaciones')
        listado2 = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado2
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarhabi(listhabitaciones):
    """
            Refresca los datos que muestra el treeview

            Args:
                listhabitaciones: Contiene un listado de habitaciones a actualizar.

            Returns:
                void.
        """
    try:
        variables.listado2 = listar()
        variables.listhabitaciones.clear()
        for registro in variables.listado2:
            variables.listhabitaciones.append(registro[0:4])
    except Exception as e:
        print(e)
        print("error en cargar treeview 2")


def bajahabi(numero):
    """
            Se conecta a la bd y borra una fila de la tabla habitaciones a partir de un número de habitación determinado.

            Args:
                numero: Contiene el numero de habitacion para encontrarla.

            Returns:
                void.
        """
    try:
        conexion.cur.execute('delete from habitaciones where numero = ?',(numero,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        print("error baja boton cliente")
        conexion.conexion.rollback()

def modifhabi(registro,numero):
    """
            Se conecta a la bd y modifica una fila utilizando los datos que se le pasan en un listado y utilizando el número de habitación para encontrar el que se debe modificar.

            Args:
                registro: Contiene un listado con los diferentes campos que tiene una habitación.
                numero: Contiene el número de la habitación que se quiere modificar

            Returns:
                void.
        """
    try:
        conexion.cur.execute('update habitaciones set numero = ?, tipo = ?, precio = ?, libre = ? where numero=?',(registro[0],registro[1],registro[2],registro[3],numero,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()



