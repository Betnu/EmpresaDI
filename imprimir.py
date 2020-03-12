# coding=utf-8
"""Módulo que gestiona la creación de la factura.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, funcionescli,funcionesreserva,variables

def basico(bill):
    """
        Construye la base de la factura

        Args:

        Returns:
            void.
        """
    try:
        text1 = 'Esperamos que vuelva pronto'
        text2 = 'CIF:00000000A '
        bill.drawImage('./img/logohotel.png', 475, 675, width=64, height=64)
        bill.setFont('Helvetica-Bold', size=16)
        bill.drawString(250, 780, 'HOTEL LITE')
        bill.setFont('Times-Italic', size=10)
        bill.drawString(240,765, text1)
        bill.drawString(260, 755, text2)
        bill.line(50,670,540,670)
        textpie = ('Hotel Lite, CIF = 00000000A Tlfo = 986000000 mail = info@hotellite.com')
        bill.setFont('Times-Italic', size=8)
        bill.drawString(170,20,textpie)
        bill.line(50, 30, 540, 30)
    except Exception as e:
        print(e)
        print('error en básico')


def factura(datosfactura):
    """
        Construye la factura a partir de los datos.

        Args:
            datosfactura: Contiene un listado con los datos de la factura.
        Returns:
            void.
        """
    try:
        bill = canvas.Canvas('servicios.pdf', pagesize=A4)
        basico(bill)
        bill.setTitle('FACTURA')
        bill.setFont('Helvetica-Bold', size= 8)

        text3 = 'Número de Factura:'
        bill.drawString(50,735, text3)
        bill.setFont('Helvetica', size=8)
        bill.drawString(140, 735, str(datosfactura[3]))
        bill.setFont('Helvetica-Bold', size=8)

        text4 = 'Fecha Factura:'
        bill.drawString(300, 735, text4)
        bill.setFont('Helvetica', size=8)
        bill.drawString(360, 735, str(datosfactura[5]))
        bill.setFont('Helvetica-Bold', size = 8)

        text5 = 'DNI CLIENTE:'
        bill.drawString(50, 710, text5)
        bill.setFont('Helvetica', size=8)
        bill.drawString(120, 710, str(datosfactura[0]))
        bill.setFont('Helvetica-Bold', size=8)

        text6 = 'Nº de Habitación:'
        bill.drawString(300, 710, text6)
        bill.setFont('Helvetica', size=8)
        bill.drawString(370, 710, str(datosfactura[4]))
        apelnome = funcionescli.apelnomfac(str(datosfactura[0]))
        bill.setFont('Helvetica-Bold', size=8)

        text7 = 'APELLIDOS:'
        bill.drawString(50, 680, text7)
        bill.setFont('Helvetica', size=9)
        bill.drawString(120, 680, str(apelnome[0]))
        bill.setFont('Helvetica-Bold', size=8)

        text8 = 'NOMBRE:'
        bill.drawString(300, 680, text8)
        bill.setFont('Helvetica', size=9)
        bill.drawString(350, 680, str(apelnome[1]))


        alojamiento=['Noches', str(datosfactura[6]), str(funcionesreserva.obtenerpreciopornumero(datosfactura[4])[0]),str(float(datosfactura[6])*funcionesreserva.obtenerpreciopornumero(datosfactura[4])[0])]
        cabecera = ['CONCEPTO','UNIDADES','PRECIO/UNIDAD','TOTAL']
        x = 75
        for i in range(0,4):
            bill.setFont('Helvetica-Bold', size=10)
            bill.drawString(x,655,cabecera[i])
            x +=130
        y=625
        for registro in variables.listfact:
            x = 75

            for i in range(0, 4):
                if i == 2 or i == 3:
                    bill.setFont('Helvetica', size=8)
                    bill.drawRightString(x + 30, y, str(registro[i]) + " €")
                else:
                    bill.setFont('Helvetica', size=8)
                    bill.drawString(x, y, str(registro[i]))
                x += 130
            y -= 30
        bill.line(50,645,540,645)
        bill.setFont('Helvetica', size=8)
        bill.drawString(420, 100, "Subtotal :")
        bill.drawString(420, 80, "Iva :")
        bill.drawString(420, 60, "Total :")
        bill.drawRightString(500, 100, str(variables.subtotal.get_text())+"€")
        bill.drawRightString(500, 80, str(variables.ivafactura.get_text())+"€")
        bill.drawRightString(500, 60, str(variables.totalfactura.get_text())+"€")
        bill.line(50, 645, 540, 645)
        bill.showPage()
        bill.save()
        dir = os.getcwd()
        os.system('/usr/bin/xdg-open ' + dir + '/servicios.pdf')
    except Exception as e:
        print(e)
        print('Error en módulo factura')

def clientes(listClientes):

    """
    Rellena la plantilla de la factura con los datos de la reserva a facturar
    :param datos_factura:   Datos de la factura de la reserva
    :return:                Void
    """
    try:
        bill = canvas.Canvas('clientes.pdf', pagesize=A4)
        bill.setTitle("CLIENTES")
        text1 = 'Esperamos que vuelva pronto'
        text2 = 'CIF:00000000A '
        bill.drawImage('./img/logohotel.png', 475, 675, width=64, height=64)
        bill.setFont('Helvetica-Bold', size=16)
        bill.drawString(250, 780, 'HOTEL LITE')
        bill.setFont('Times-Italic', size=10)
        bill.drawString(240, 765, text1)
        bill.drawString(260, 755, text2)
        bill.line(50, 670, 540, 670)
        textpie = ('Hotel Lite, CIF = 00000000A Tlfo = 986000000 mail = info@hotellite.com')
        bill.setFont('Times-Italic', size=8)
        bill.drawString(170, 20, textpie)
        bill.line(50, 30, 540, 30)
        cabecera = ['DNI', 'APELLIDOS', 'NOME', 'DATA ALTA']

        x = 75
        for i in range(0, 4):
            bill.setFont('Helvetica-Bold', size=10)
            bill.drawString(x, 655, cabecera[i])
            x += 130
        y=635
        for registro in listClientes:
            x = 75
            if y<= 50:
                y=850
                bill.showPage()
                bill.setFont('Helvetica-Bold', size=10)
                bill.drawString(560, 15, str(bill.getPageNumber()))
                bill.line(50, 800, 540, 800)
                for i in range(0, 4):
                    bill.setFont('Helvetica-Bold', size=10)
                    bill.drawString(x, 780, cabecera[i])
                    x += 130
                bill.line(50, 770, 540, 770)
                bill.line(50, 30, 540, 30)
                y=750
                x=75
            for i in range(0, 4):
                bill.setFont('Helvetica', size=8)
                if(i==0):
                    bill.drawString(x, y, str("*****"+registro[i][6]+registro[i][7]+registro[i][8]))
                else:
                    bill.drawString(x, y, str(registro[i]))

                x += 130
            y -= 30


        bill.showPage()
        bill.save()
        directorio_actual = os.getcwd()
        os.system('/usr/bin/xdg-open ' + directorio_actual + '/clientes.pdf')
    except Exception as e:
        print(e)
        print('Error en factura')
