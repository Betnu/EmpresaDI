# coding=utf-8
"""Módulo principal
"""
import gi

import funcionesreserva

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk
import eventos, conexion, variables, funcionescli, funcioneshabi, funcionesservi
class Empresa:
    def __init__(self):
        b = Gtk.Builder()
        b.add_from_file('ventana_prueba3.glade')
        self.vprincipal = b.get_object('venPrincipal')
        b.connect_signals(eventos.Eventos())
        #s = Gdk.Screen.get_default()
        #a = s.get_width()
        #c = s.get_height()
        self.vprincipal.show()
        self.set_styles()
        #self.vprincipal.resize(a,c)
        self.vprincipal.maximize()
        self.entdni = b.get_object('entDni')
        self.entapel= b.get_object('entApel')
        self.entnome = b.get_object('entNome')
        self.entdatacli = b.get_object('entData')
        self.entnumero = b.get_object('entNumero')
        self.entprecio = b.get_object('entPrecio')
        self.ententrada= b.get_object('ententrada')
        self.entsalida = b.get_object('entsalida')
        self.entdesayuno = b.get_object('entDesayuno')
        self.entcomida = b.get_object('entComida')
        self.entparking = b.get_object('entParking')
        self.entServicio = b.get_object('entServicio')
        self.entPrecioSer = b.get_object('entPrecioSer')
        self.lblerrdni = b.get_object('lblErrdni')
        self.lblcodcli = b.get_object('lblCodcli')
        self.lbldnifactura = b.get_object('lblDnifactura')
        self.lblapelfactura = b.get_object('lblApelFactura')
        self.lblnomefactura = b.get_object('lblNomefactura')
        self.lblcodigofactura = b.get_object('lblCodigoFactura')
        self.lblhabfactura = b.get_object('lblHabFactura')
        self.lbldatafactura = b.get_object('lblDataFactura')
        self.lblUnidades = b.get_object('lblUnidades')
        self.lblPrecioUni = b.get_object('lblPrecioUni')
        self.lblTotal = b.get_object('lblTotal')
        self.lbldni = b.get_object('lbldni')
        self.lblapel = b.get_object('lblapel')
        self.lblnoches = b.get_object('lblnoches')
        self.lblCodResSer = b.get_object('lblCodResSer')
        self.lblHabSer = b.get_object('lblHabSer')
        self.fecha = b.get_object('lblFecha')
        self.opecorrecta = b.get_object('lblOpecorrecta')
        self.lblsubtotal = b.get_object('lblSubtotal')
        self.lblTotalPrecio = b.get_object('lblTotalPrecio')
        self.lblIVA = b.get_object('lblIVA')
        self.calendario = b.get_object('ventCalendar')
        self.calendar = b.get_object('Calendar')
        self.rb1 = b.get_object('rbSimple')
        self.rb2 = b.get_object('rbDoble')
        self.rb3 = b.get_object ('rbFamiliar')
        self.cmbhab = b.get_object('cmbNumres')
        self.swtlibre = b.get_object('swtlibre')
        self.rbdesayuno = b.get_object('rbDesayuno')
        self.rbcomida = b.get_object('rbComida')
        self.cbParking = b.get_object('cbParking')
        variables.subtotal=self.lblsubtotal
        variables.totalfactura=self.lblTotalPrecio
        variables.ivafactura=self.lblIVA
        variables.filacli = ( self.entdni,self.entapel,self.entnome,self.entdatacli)
        variables.filahabi = (self.entnumero,self.rb1,self.rb2,self.rb3,self.entprecio,self.swtlibre)
        variables.filares = (self.lbldni, self.lblapel, self.cmbhab, self.ententrada, self.entsalida, self.lblnoches)
        variables.filaser = (self.lblCodResSer, self.lblHabSer, self.rbdesayuno, self.rbcomida,self.cbParking,self.entServicio,self.entPrecioSer)
        variables.labels_factura = (self.lbldnifactura,self.lblapelfactura,self.lblnomefactura,self.lblcodigofactura,self.lblhabfactura,self.lbldatafactura, self.lblUnidades, self.lblPrecioUni, self.lblTotal)
        variables.ent_precios = (self.entdesayuno,self.entcomida,self.entparking)
        variables.cmbhab = (self.cmbhab)
        variables.listclientes = b.get_object('listClientes')
        variables.listhabitaciones = b.get_object('listHabitaciones')
        variables.listres = b.get_object('listReserva')
        variables.listservi = b.get_object('listServicios')
        variables.listfact = b.get_object('listFactura')
        variables.treehabitaciones = b.get_object('treeHabitaciones')
        variables.treeclientes = b.get_object('treeClientes')
        variables.treeres = b.get_object('treeReservas')
        variables.treeser = b.get_object('treeServicios')
        variables.ventcalendar = self.calendario
        variables.calendar = self.calendar
        variables.menserror = (self.lblerrdni,self.lblcodcli,self.fecha,self.opecorrecta)
        variables.panel = b.get_object('panel')
        variables.venacercade = b.get_object('venAcercade')
        variables.venfiledialog = b.get_object('venBackup')
        variables.venfiledialog2 = b.get_object('venRestBackup')
        variables.venPrecio = b.get_object('venPrecios')
        conexion.Conexion().abrirbbdd()
        funcionescli.listarcli(variables.listclientes)
        funcioneshabi.listarhabi(variables.listhabitaciones)
        funcionesreserva.listares(variables.listres)
        funcionesreserva.listadonumhab(self)
        #CSS
        menubar = b.get_object('menuBar').get_style_context().add_class('menuBar')
        menuBarFile = b.get_object('menuBarFile').get_style_context().add_class('menuBarFile')
        menuInternoFile = b.get_object('menuInternoFile').get_style_context().add_class('menuInternoFile')
        #funcionescli.fecha()
    def set_styles(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('estilos.css')
        Gtk.StyleContext().add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
if __name__ == '__main__':
    main= Empresa()
    Gtk.main()
