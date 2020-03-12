# coding=utf-8
"""Módulo que gestiona la facturación.
"""
import funcionesreserva
import variables


def limpiar_labels_factura(labels_factura):
    """
       Vacia los labels de los campos de factura.
        Args:
            labels_factura: contiene los labels de factura.
        Returns:
            void

    """
    for i in range(len(labels_factura)):
        labels_factura[i].set_text('')


def obtener_factura(dni, apellidos, nombre, codigo):
    """
       Coloca el texto de la factura con los datos que le llegan.
        Args:
            dni: Contiene el dni del cliente
            apellidos: Contiene los apellidos del cliente
            nombre: Contiene el nombre del cliente
            codigo: Contiene el codigo de reserva
            numero_habitacion: Contiene el numero de la habitación
            check_out: Contiene la fecha de salida
            noches: Contiene el número de noches
        Returns:
            void

    """
    try:
        variables.labels_factura[0].set_text(str(dni))
        variables.labels_factura[1].set_text(str(apellidos))
        variables.labels_factura[2].set_text(str(nombre[0]))
        variables.labels_factura[3].set_text(str(codigo))
    except Exception as e:
        print(e)
        print('Error en obtener_factura')