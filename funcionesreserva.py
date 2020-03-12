# coding=utf-8
"""Módulo que gestiona las reservas.
"""
import sqlite3
from datetime import datetime
import conexion
import variables
import funcionesservi

def listadonumhab(self):
    """
        Lista número de habitaciones.

        Args:

        Returns:
            void.
    """
    try:
        conexion.cur.execute('select numero from habitaciones')
        listado = conexion.cur.fetchall()
        for row in listado:
            variables.listcmbhab.append(row)
            conexion.conex.commit()
        return listado
    except Exception as e:
        print(e)
        conexion.conex.rollback()

def listar():
    """
            Se conecta a la bd y consulta la tabla reserva y los guarda en un listado

            Args:

            Returns:
                listado, es una lista con los datos de las reservas.
    """
    try:
        conexion.cur.execute('select * from reservas')
        listado3 = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado3
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()
def listares(listres):
    """
        Refresca los datos que muestra el treeview

        Args:
            listres: Contiene un listado de reservas a actualizar.

        Returns:
            void.
        """
    try:

        variables.listado3 = listar()
        variables.listres.clear()
        for registro in variables.listado3:
            variables.listres.append(registro[0:7])

    except Exception as e:
        print(e)
        print("error en cargar treeview 3")

def insertarres(fila):
    """
           Se conecta a la bd e inserta una reserva.

           Args:
               fila: Contiene un listado con los valores de reserva.

           Returns:
               void.
        """
    try:
        conexion.cur.execute('insert into reservas(dni,apelidos,habitacion,entrada,salida,noches) values(?,?,?,?,?,?)',fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()
def calculadias():
    """
        Calcula el número de noches

        Args:

        Returns:
            void.
    """
    diain = variables.filares[3].get_text()
    date_in = datetime.strptime(diain, '%d/%m/%Y').date()
    diaout = variables.filares[4].get_text()
    date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
    noches = (date_out - date_in).days
    if noches <= 0:
        variables.filares[5].set_text('Check-Out debe ser posterior')
        variables.reserva = 0
    else:
        variables.reserva = 1
        variables.filares[5].set_text(str(noches))
        return(str(noches))

def bajares(codigo):
    """
        Se conecta a la bd y borra una fila de la tabla reservas a partir de un codigo de reserva determinado.

        Args:
            codigo: contiene el codigo de reserva que indica cual se va a borrar

        Returns:
            void.
        """
    try:
        conexion.cur.execute('delete from reservas where codigo = ?',(codigo,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        print("error baja boton reserva")
        conexion.conexion.rollback()

def versilibre(numhab):
    """
        Se conecta a la base de datos y comprueba si una habitación determinada está libre.

        Args:
            numhab: contiene el número de la habitación de la que se va a comprobar

        Returns:
            boolean
    """
    try:
        conexion.cur.execute('select libre from habitaciones where numero = ?')
        lista = conexion.cur.fetchone()
        conexion.conex.commit()
        if lista[0] == 'SI':
            return True
        else:
            return False
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def cambialibre(cambio,numhab):
    """
        Se conecta a la bd y cambia el estado de la habitación entre libre y no libre

        Args:
            cambio: Recibe un número que indica si está libre o no.
            numhab: Recibe el número de la habitación de la que se va a cambiar el estado.

        Returns:
            void.
    """
    try:
        if(cambio==1):
            si = "SI"
        else:
            si = "NO"
        conexion.cur.execute('update habitaciones set libre = ? where numero = ?', (si, numhab,))
        conexion.conex.commit()
    except Exception as e:
        print(e)
        print("error cambiar libre")
        conexion.conex.rollback()

def limpiarres(fila):
    """
        Limpia las entradas de texto.

        Args:
            fila: Contiene un listado de widgets de reservas

        Returns:
            void.
    """
    fila[0].set_text('')
    fila[1].set_text('')
    #fila[2].set_active(0)
    fila[3].set_text('')
    fila[4].set_text('')
    fila[5].set_text('')

def modifreser(registro,codigo):
    """
        Se conecta a la bd y modifica una fila utilizando los datos que se le pasan en un listado y utilizando el codigo de reserva para encontrar la que se debe modificar.

        Args:
            registro: Contiene un listado con los diferentes campos que tiene una reserva.
            codigo: Contiene el codigo de reserva que se quiere modificar.

        Returns:
            void.
        """
    try:
        conexion.cur.execute('update reservas set dni = ?, apelidos = ?, habitacion = ?, entrada = ?, salida = ?, noches = ? where codigo = ?',(registro[0],registro[1],registro[2],registro[3],registro[4],registro[5],codigo,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def obtenerpreciopornumero(numero):
    """
        Obtiene el precio según el número de la habitación.

        Args:
            numero: contiene el número de la habitación.

        Returns:
            precio: devuelve el precio de las noches.
            """
    try:
        conexion.cur.execute('select precio from habitaciones where numero = ?',(numero,))
        precio=conexion.cur.fetchone()
        conexion.conex.commit()
        return precio
    except sqlite3.OperationalError as e:
        print(e)
        print("error obtener precio")

def obtenernombredni(dni):
    """
        Obtiene el nombre a partir del dni

        Args:
            dni: Contiene el dni con el que se va a encontrar el cliente.

        Returns:
            void.
            """
    try:
        conexion.cur.execute('select nome from clientes where dni = ?', (dni,))
        nombre=conexion.cur.fetchone()
        conexion.conex.commit()
        return nombre
    except sqlite3.OperationalError as e:
        print(e)
        print("error al obtener nombre por dni")