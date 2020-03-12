# coding=utf-8
"""Módulo que gestiona la conexión a la base de datos.
"""
import os
import sqlite3

class Conexion:

    def abrirbbdd(self):
        """
            Se conecta con la base de datos.
            Args:

            Returns:
                void
        """
        try:
            global bbdd, conex, cur
            bbdd = 'empresa.sqlite'
            conex = sqlite3.connect(bbdd)
            cur = conex.cursor()
            print("Conexion realizada correctamente")
        except sqlite3.OperationalError as e:
            print("Error al abrir",e)

    def cerrarbbdd(self):
        """
            Se cierra la base de datos.
            Args:

            Returns:
                void
        """
        try:
            cur.close()
            conex.close()
            print("Base de datos cerrada correctamente")
        except sqlite3.OperationalError as e:
            print("Error al cerrar",e)