__autor__='alberto'

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import impresion
class Hola:
    def __init__(self):
        #iniciamos la libreria gtk
        b = Gtk.Builder()
        b.add_from_file('ventana.glade')
        #cargamos los widgets con algun evento asociado o que son referenciados
        self.vprincipal = b.get_object('Vprincipal')
        self.btnsaludo = b.get_object('btnSaludo')
        self.lblsaludo = b.get_object('lblSaludos')
        self.btnsalir = b.get_object('btnSalir')
        #diccionario de eventos
        dic = {'on_Vprincipal_destroy':self.salir, 'on_btnSaludo_clicked':self.mostrar, 'on_btnSalir_clicked':self.salir, }

        #conectamostodo y lo mostramos
        b.connect_signals(dic)
        self.vprincipal.show()

    #ahora codificamos las funciones

    def salir(self,widget):
        Gtk.main_quit()
        self.btnsalir

    def mostrar(self,widget):
        impresion.factura()

if __name__=='__main__':
    main=Hola()
    Gtk.main()