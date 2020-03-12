# coding=utf-8
"""Módulo que gestiona los eventos
"""
import shutil
import zipfile
import xlrd
from datetime import datetime

import gi,os
import xlwt

import funcionesreserva,funcionesservi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import conexion, variables, funcionescli,funcioneshabi, os, imprimir, facturacion

class Eventos():
    def on_venPrincipal_destroy(self, widget):
        """
        Evento para cerrar la ventana
        """
        conexion.Conexion.cerrarbbdd(self)
        Gtk.main_quit()

    def on_btnAltacli_clicked(self, widget):
        """
        Evento que gestiona el botón para dar de alta un cliente
        """
        try:
            dni = variables.filacli[0].get_text()
            apelidos = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apelidos, nome, data)
            if funcionescli.validoDNI(dni):
                funcionescli.insertarcli(registro)
                funcionescli.listarcli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
                #variables.menserror[3].set_text("Cliente dado de alta correctamente")
        except Exception as e:
            print(e)
            print("Error alta cliente")

    def on_treeClientes_cursor_changed(self, widget):
        """
        Evento que gestiona el treeview de clientes
        """
        try:
            funcionescli.limpiarentry(variables.filacli)
            model, iter = variables.treeclientes.get_selection().get_selected()
            if iter != None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snome = model.get_value(iter, 2)
                sdata = model.get_value(iter, 3)
                if (sdata == None):
                    sdata = " "
                cod = funcionescli.selectcli(sdni)
                variables.menserror[1].set_text(str(cod[0]))
                variables.filacli[0].set_text(sdni)
                variables.filares[0].set_text(sdni)
                variables.filacli[1].set_text(sapel)
                variables.filares[1].set_text(sapel)
                variables.filacli[2].set_text(snome)
                variables.filacli[3].set_text(str(sdata))
        except Exception as e:
            print(e)
            print("error carga cliente")

    def on_entDni_focus_out_event(self, widget, Data=None):
        """
        Evento que controla si el dni es valido al salir de la entry para introducirlo
        """
        self.var = variables.filacli[0].get_text()
        if funcionescli.validoDNI(self.var):
            variables.menserror[0].set_text(' ')
            pass
        else:
            variables.menserror[0].set_text('DNI INCORRECTO')

    def on_btnBajacli_clicked(self, widget):
        """
        Evento que gestiona el botón para dar de baja un cliente
        """
        try:
            dni = variables.filacli[0].get_text()
            if dni != ' ':
                funcionescli.bajacli(dni)
                funcionescli.listarcli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta dni u otro error')
        except:
            print('error en boton baja cliente')

    def on_btnModifcli_clicked(self, widget):
        """
        Evento que gestiona el botón para modificar un cliente
        """
        try:
            cod = variables.menserror[1].get_text()
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != ' ':
                funcionescli.modifcli(registro, cod)
                funcionescli.listarcli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
        except Exception as e:
            print(e)
            print("error boton modificar")

    def on_btnCalendar_clicked(self, widget):
        """
        Evento que gestiona el botón para abrir una ventana de calendario.
        """
        try:
            variables.ventcalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.semaforo = 1
            variables.ventcalendar.show()
        except:
            print("Error abrir calendario")

    def on_Calendar_day_selected_double_click(self, widget):
        """
        Evento que gestiona la selección de fecha al dar doble click sobre una en el calendario.
        """
        try:
            agno, mes, dia = variables.calendar.get_date()
            fecha = "%s/" % dia + "%s/" % (mes + 1) + "%s" % agno
            if(variables.semaforo==1):
                variables.filacli[3].set_text(fecha)
            elif(variables.semaforo==2):
                variables.filares[3].set_text(fecha)
            elif(variables.semaforo==3):
                variables.filares[4].set_text(fecha)
                funcionesreserva.calculadias()
            else:
                pass
            variables.ventcalendar.hide()
        except:
            print("Error al coger la fecha")

    def on_btnAltaHabi_clicked(self, widget):
        """
        Evento que gestiona el botón para dar de alta una habitación
        """
        try:
            numero = variables.filahabi[0].get_text()
            if variables.filahabi[1].get_active():
                tipo = "Simple"
            elif variables.filahabi[2].get_active():
                tipo = "Doble"
            elif variables.filahabi[3].get_active():
                tipo = "Familiar"
            precio = variables.filahabi[4].get_text()
            if variables.filahabi[5].get_active():
                libre="SI"
            else:
                libre="NO"
            registro = (numero, tipo, precio,libre)
            if (len(numero) <= 3):
                funcioneshabi.insertarhabi(registro)
                funcioneshabi.listarhabi(variables.listhabitaciones)
                funcioneshabi.limpiarentry(variables.filahabi)
                #variables.menserror[3].set_text("Habitacion dada de alta correctamente")
        except Exception as e:
            print(e)
            print("Error alta habitacion")

    def on_treeHabitaciones_cursor_changed(self, widget):
        """
        Evento que gestiona el treeview de habitaciones
        """
        try:
            model, iter = variables.treehabitaciones.get_selection().get_selected()
            if iter != None:
                snumero = model.get_value(iter, 0)
                stipo = model.get_value(iter, 1)
                sprecio = model.get_value(iter, 2)
                slibre = model.get_value(iter,3)
                variables.filahabi[0].set_text(str(snumero))
                if (stipo == "Simple"):
                    variables.filahabi[1].set_active(True)
                elif (stipo == "Doble"):
                    variables.filahabi[2].set_active(True)
                elif (stipo == "Familiar"):
                    variables.filahabi[3].set_active(True)
                variables.filahabi[4].set_text(str(sprecio))
                if (slibre=='SI'):
                    variables.filahabi[5].set_active(True)
                else:
                    variables.filahabi[5].set_active(False)
        except Exception as e:
            print(e)
            print("error carga habitacion")

    def on_btnBajaHabi_clicked(self, widget):
        """
        Evento que gestiona el botón para dar de baja una habitación
        """
        try:
            numero = variables.filahabi[0].get_text()
            funcioneshabi.bajahabi(numero)
            funcioneshabi.listarhabi(variables.listhabitaciones)
            funcioneshabi.limpiarentry(variables.filahabi)
        except:
            print('error en boton baja habitación')

    def on_btnModifHabi_clicked(self, widget):
        """
        Evento que gestiona el botón para modificar una habitación
        """
        try:
            model, iter = variables.treehabitaciones.get_selection().get_selected()
            numero = model.get_value(iter, 0)
            numero2 = variables.filahabi[0].get_text()
            if (variables.filahabi[1].get_active()):
                tipo = "Simple"
            elif (variables.filahabi[2].get_active()):
                tipo = "Doble"
            elif (variables.filahabi[3].get_active()):
                tipo = "Familiar"
            precio = variables.filahabi[4].get_text()
            if (variables.filahabi[5].get_active()):
                libre = "SI"
            else:
                libre = "NO"
            registro = (numero2, tipo, precio, libre)
            if (len(numero2) <= 3 & numero != ''):
                funcioneshabi.modifhabi(registro, numero)
                funcioneshabi.listarhabi(variables.listhabitaciones)
                funcioneshabi.limpiarentry(variables.filahabi)
                #variables.menserror[3].set_text("Habitación modificada correctamente")
        except Exception as e:
            print(e)
            print("error boton modificar")

    def on_btnSalirtool_clicked(self, wiget):
        """
        Evento que gestiona el botón para salir en el toolbar.
        """
        conexion.Conexion.cerrarbbdd(self)
        Gtk.main_quit()

    def on_btnClitool_clicked(self, widget):
        """
        Evento que gestiona el botón para moverse a clientes desde el toolbar.
        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                funcionescli.limpiarentry(variables.filacli)
        except Exception as e:
            print(e)
            print("error botón cliente barra herramientas")

    def on_btnCalc_clicked(self, widget):
        """
        Evento que gestiona el botón para abrir la calculadora desde el toolbar.
        """
        os.system('gnome-calculator')

    def on_btnHabitool_clicked(self, widget):
        """
        Evento que gestiona el botón para moverse a habitaciones desde el toolbar.
        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                funcioneshabi.limpiarentry(variables.filahabi)
        except Exception as e:
            print(e)
            print("error botón habitación barra herramientas")

    def on_btnResertool_clicked(self, widget):
        """
        Evento que gestiona el botón para moverse las reservas desde el toolbar.
        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 1:
                variables.panel.set_current_page(1)
            else:
                pass
        except Exception as e:
            print(e)
            print("error botón reservas barra herramientas")

    def on_btnRefresh_clicked(self, widget):
        """
        Evento que limpia todas las entrys
        """
        funcionescli.limpiarentry(variables.filacli)
        funcioneshabi.limpiarentry(variables.filahabi)
        funcionesreserva.limpiarres(variables.filares)
        facturacion.limpiar_labels_factura(variables.labels_factura)

    def on_menuBarSalir_activate(self, widget):
        """
        Evento que gestiona el botón para salir desde el menubar
        """
        conexion.Conexion.cerrarbbdd(self)
        Gtk.main_quit()

    def on_btnSalirAcerca_clicked(self, widget):
        """
        Evento que gestiona el botón para salir de la ventana Acerca de
        """
        try:
            variables.venacercade.connect('delete_event', lambda w, e: w.hide() or True)
            variables.venacercade.hide()
        except:
            print('error cerrar salir acerca de')

    def on_menuBarAcercade_activate(self, widget):
        """
        Evento que gestiona el botón para abrir el Acerca de desde el menubar
        """
        try:
            variables.venacercade.show()
        except:
            print('error abrir acerca de')

    def on_menuBarBackup_activate(self, widget):
        """
        Evento que gestiona el botón para abrir una backup desde el menubar
        """
        try:
            variables.venfiledialog.show()
        except:
            print("error abrir backup")

    def on_btnBackup_clicked(self, widget):
        """
        Evento que gestiona el botón para crear una backup desde el menubar
        """
        try:
            conexion.Conexion().cerrarbbdd()
            backup = 'backup.zip'
            destino = str(variables.venfiledialog.get_filename())
            if os.path.exists(destino):
                pass
            else:
                os.system('mkdir ' + destino)
                os.system('chmod 0777 ' + destino)
            now = datetime.now()
            copia = zipfile.ZipFile(backup, 'w')
            copia.write('empresa.sqlite', compress_type=zipfile.ZIP_DEFLATED)
            copia.close()
            neobackup = str(datetime.now()) + str(backup)
            os.rename(backup, neobackup)
            shutil.move(neobackup, destino)
            conexion.Conexion.abrirbbdd(self)
        except Exception as e:
            print(e)
            print("error comprimir base datos")

    def on_btnSalirBackup_clicked(self, widget):
        """
        Evento que gestiona el botón para salir de la ventana de backup
        """
        try:
            variables.venfiledialog.connect('delete_event', lambda w, e: w.hide() or True)
            variables.venfiledialog.hide()
        except:
            print('error cerrar backup')


    def on_btnBackuptool_clicked(self,widget):
        """
        Evento que gestiona el botón para hacer un backup desde el toolbar
        """
        try:
            variables.venfiledialog.show()
        except:
            print("error abrir ventana")

    def on_menuBarCopia_activate(self,widget):
        try:
            variables.venfiledialog2.show()
        except:
            print("no abre ventana")


    def on_btnRestaurar_clicked(self,widget):
        try:
                conexion.Conexion().cerrarbbdd()
                #backup = 'backup.zip'
                fichero = variables.venfiledialog2.get_filename()
                copia = zipfile.ZipFile(fichero, 'r')
                os.system("rm empresa.sqlite")
                copia.extract("empresa.sqlite")
                copia.close()
                conexion.Conexion.abrirbbdd(self)


        except Exception as e:
                print(e)
                print("error comprimir base datos")

    def on_btnSalirRestaurar_clicked(self,widget):
        try:
            variables.venfiledialog2.connect('delete_event', lambda w, e: w.hide() or True)
            variables.venfiledialog2.hide()
        except:
            print('error cerrar backup')

    def on_cmbNumres_changed(self, widget):
        """
        Evento que gestiona el combobox de reservas con el numero de habitación
        """
        try:
            index = variables.cmbhab.get_active()
            model = variables.cmbhab.get_model()
            item = model[index]
            variables.numhabr = item[0]
        except Exception as e:
            print(e)
            print('error mostrar habitacion combo')

    def on_btnCheckOut_clicked(self, widget):
        """
        Evento que gestiona el botón de checkout
        """
        try:
            variables.ventcalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.semaforo = 3
            variables.ventcalendar.show()
        except:
            print("Error abrir calendario")

    def on_btnCheckIn_clicked(self, widget):
        """
        Evento que gestiona el botón de checkin
        """
        try:
            variables.ventcalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.semaforo = 2
            variables.ventcalendar.show()
        except:
            print("Error abrir calendario")

    def on_treeReservas_cursor_changed(self, widget):
        """
        Evento que gestiona el treeview de reservas
        """
        try:
            model, iter = variables.treeres.get_selection().get_selected()
            if iter != None:
                scodr = model.get_value(iter,0)
                sdni = model.get_value(iter, 1)
                nombre = funcionesreserva.obtenernombredni(sdni)
                sapelidos = model.get_value(iter, 2)
                shabitacion = model.get_value(iter, 3)
                sentrada = model.get_value(iter, 4)
                ssalida = model.get_value(iter, 5)
                snoches = model.get_value(iter, 6)
                variables.filaser[0].set_text(str(scodr))
                variables.filaser[1].set_text(shabitacion)
                variables.filares[0].set_text(sdni)
                variables.filares[1].set_text(sapelidos)
                listado = funcionesreserva.listadonumhab(self)
                for i in range(len(listado)):
                    habi="("+shabitacion+",)"
                    if(str(habi) == str(listado[i])):
                        variables.filares[2].set_active(i)
                variables.filares[3].set_text(str(sentrada))
                variables.filares[4].set_text(str(ssalida))
                variables.filares[5].set_text(snoches)
                funcionesservi.listarservi(variables.listservi)
                global datosfactura
                datosfactura = (sdni, sapelidos, nombre, scodr, shabitacion, ssalida, snoches)
                facturacion.obtener_factura(sdni, sapelidos, nombre, scodr)
                funcionesservi.calcularPreciosServicios()
        except Exception as e:
            print(e)
            print("error carga reservas")


    def on_btnAltaReserva_clicked(self, widget):
        """
        Evento que gestiona el botón para dar de alta una reserva.
        """
        try:

            dni = variables.filares[0].get_text()
            apel = variables.filares[1].get_text()
            habi = variables.numhabr
            entrada = variables.filares[3].get_text()
            salida = variables.filares[4].get_text()
            noches = variables.filares[5].get_text()
            registro = (dni,apel,habi,entrada,salida,noches)
            funcionesreserva.insertarres(registro)
            funcionesreserva.listares(variables.listhabitaciones)
            cambio = 0
            funcionesreserva.cambialibre(cambio,habi)
            funcioneshabi.listarhabi(variables.listhabitaciones)
            funcionesreserva.limpiarres(variables.filares)

        except Exception as e:
            print(e)
            print("Error alta habitacion")
    """
    def on_btnBajaReserva_clicked(self, widget):
        try:
            model, iter = variables.treeres.get_selection().get_selected()
            if iter != None:
                codigo = model.get_value(iter, 0)
                numbhab = model.get_value(iter, 3)
            funcionesreserva.bajares(codigo)
            funcionesreserva.listares(variables.listres)
            cambio = 1
            funcionesreserva.cambialibre(cambio,numbhab)
            funcioneshabi.listarhabi(variables.listhabitaciones)
            funcionesreserva.limpiarres(variables.filares)
        except Exception as e:
            print(e)
            print('error en boton baja reserva')
    """
    def btnCheckOutRes_clicked(self,widget):
        """
        Evento que gestiona el botón para hacer checkout en una reserva
        """
        try:
            model, iter = variables.treeres.get_selection().get_selected()
            if iter != None:
                numbhab = model.get_value(iter, 3)
            cambio = 1
            funcionesreserva.cambialibre(cambio,numbhab)
            funcioneshabi.listarhabi(variables.listhabitaciones)
            funcionesreserva.limpiarres(variables.filares)
        except Exception as e:
            print(e)
            print('error en boton checkout')
    def on_btnModifReserva_clicked(self, widget):
        """
        Evento que gestiona el botón para modificar una reserva
        """
        try:
            dni = variables.filares[0].get_text()
            apel = variables.filares[1].get_text()
            habi = variables.numhabr
            entrada = variables.filares[3].get_text()
            salida = variables.filares[4].get_text()
            noches = variables.filares[5].get_text()
            registro = (dni, apel, habi, entrada, salida, noches)
            model, iter = variables.treeres.get_selection().get_selected()
            cod = model.get_value(iter,0)
            shabi = model.get_value(iter,3)
            if (habi!=shabi):
                cambio=1
                funcionesreserva.cambialibre(cambio,shabi)
                cambio=0
                funcionesreserva.cambialibre(cambio,habi)
            funcionesreserva.modifreser(registro,cod)
            funcionesreserva.listares(variables.listres)
            funcionesreserva.limpiarres(variables.filares)
            funcioneshabi.listarhabi(variables.filahabi)
        except Exception as e:
            print(e)
            print("error boton modificar")


    def on_btnImprimir_clicked(self, widget):
        """
        Evento que gestiona el botón para imprimir una factura
        """
        try:
            imprimir.factura(datosfactura)
        except:
            print('Error en módulo factura')

    def on_menuBarImportar_activate(self, widget):
        """
        Evento que gestiona el botón para importar un archivo excel desde el menubar.
        """
        try:
            fichero_excel = xlrd.open_workbook("clientes.xls")
            hoja_clientes = fichero_excel.sheet_by_index(0)
            numero_filas_clientes = hoja_clientes.nrows
            numero_columnas_clientes = hoja_clientes.ncols
            for i in range(numero_filas_clientes):
                celdas_cliente = []
                if i > 0:
                    for j in range(numero_columnas_clientes):
                        celdas_cliente.append(hoja_clientes.cell(i,j))
                    funcionescli.insertarcliexcel(celdas_cliente)
                    funcionescli.listarcli(variables.listclientes)
        except Exception as e:
            print(e)
            print("Error en menu bar importar")

    def on_menuBarExportar_activate(self,widget):
        """
        Evento que gestiona el botón para exportar desde el menubar
        """
        try:
            estilo_cabecera = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
            estilo_celda = xlwt.easyxf(num_format_str='DD-MM-YY')
            fichero_excel = xlwt.Workbook()
            hoja_excel = fichero_excel.add_sheet('NuevoClientes',cell_overwrite_ok=True)
            hoja_excel.write(0,0,'DNI',estilo_cabecera)
            hoja_excel.write(0,1,'APELIDOS',estilo_cabecera)
            hoja_excel.write(0,2,'NOMBRE',estilo_cabecera)
            hoja_excel.write(0,3,'FECHA_ALTA',estilo_cabecera)
            listado_clientes = funcionescli.listar()
            for i in range(len(listado_clientes)):
                for j in range(len(listado_clientes[0])):
                    hoja_excel.write(i,j,listado_clientes[i][j], estilo_celda)
            fichero_excel.save('clientes_exportados.xls')
        except Exception as e:
            print(e)
            print("Error exportar menu bar")

    def on_gestion_activate(self,widget):
        """
        Evento que gestiona el botón para abrir la ventana de precios
        """
        try:
            variables.venPrecio.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venPrecio.show()
        except Exception as e:
            print(e)
            print("Error mostrar ventana precios")


    def on_btnAltaPrecio_clicked(self, widget):
        """
        Evento que gestiona el botón para modificar los precios.
        """
        try:
            desayuno = str(variables.ent_precios[0].get_text())
            comida = str(variables.ent_precios[1].get_text())
            parking = str(variables.ent_precios[2].get_text())
            listaprecios = (desayuno,comida,parking)
            funcionesservi.insertarprecios(listaprecios)
            variables.venPrecio.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venPrecio.hide()
        except Exception as e:
            print(e)
            print("Error Alta Precio")

    def on_btnSalirPrecios_clicked(self,widget):
        """
        Evento que gestiona el botón para salir de la ventana de precios.
        """
        try:
            variables.venPrecio.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venPrecio.hide()
        except Exception as e:
            print(e)
            print("Error salir")

    def on_Axuda_activate(self,widget):
        os.system('pydoc -p 1234|/usr/bin/firefox --new-window http://localhost:1234')

    def on_btnAltaBasico_clicked(self,widget):
        try:
            codres=variables.filaser[0].get_text()
            desayuno=variables.filaser[2]
            comida=variables.filaser[3]
            parking=variables.filaser[4]
            concepto=" "
            if desayuno.get_active():
                concepto="Desayuno"
                funcionesservi.insertarservicio(codres,concepto)
                if parking.get_active():
                    concepto="Parking"
                    funcionesservi.insertarservicio(codres,concepto)
            elif comida.get_active():
                concepto="Comida"
                funcionesservi.insertarservicio(codres,concepto)
                if parking.get_active():
                    concepto="Parking"
                    funcionesservi.insertarservicio(codres, concepto)
            elif parking.get_active():
                concepto="Parking"
                funcionesservi.insertarservicio(codres, concepto)
            funcionesservi.listarservi(variables.listservi)
        except Exception as e:
            print(e)
            print("Error Alta Servicio")

    def on_btnEliminarServicio_clicked(self,widget):
        try:
            model, iter = variables.treeser.get_selection().get_selected()
            if iter != None:
                scodser = model.get_value(iter, 0)
                funcionesservi.bajaservi(str(scodser))
            funcionesservi.listarservi(variables.filaser)
        except Exception as e:
            print(e)
            print("Error eliminar servicio")

    def on_btnAltaAdicional_clicked(self,widget):
        try:
            codres=variables.filaser[0].get_text()
            concepto=variables.filaser[5].get_text()
            precio=variables.filaser[6].get_text()
            funcionesservi.insertarservicioadicional(codres,concepto,precio)
            funcionesservi.listarservi(variables.listservi)
        except Exception as e:
            print(e)
            print("Error Alta Servicio")

    def on_menubarListar_activate(self,widget):
        try:
            imprimir.clientes(variables.listclientes)
        except Exception as e:
            print(e)