#!/usr/bin/python
# encoding: utf-8
import csv
import re


#Se verifica que los datos ingresados sean coherentes.
number = re.compile(u'[0-9]{9,10}')
text = re.compile(u'([ -Ñ]){0,160}')


def loadMessagesFromCSV(campania):
    #print "Leyendo archivo csv ... %s" %(campania.archivo_CSV.path)
    csvfile = csv.reader(open(campania.archivo_CSV.path), delimiter=';')

    for row in csvfile:
        n = number.match(row[0])
        t = text.match(row[1])
        if n and t:
            campania.mensaje_set.create(destino=n.group(), contenido=t.group(),
                                        activado=True, intentos_fallidos=0, gateway_id=0)


def loadMessagesFromMemory(campania, archivo):

    try:
        dialect = csv.Sniffer().sniff(archivo.read(), delimiters=';,')
        archivo.seek(0)

        csvfile = csv.reader(archivo, dialect)
        for row in csvfile:
            if len(row) == 2:
                n = number.match(row[0])
                try:
                    t = text.match(row[1].decode('iso-8859-15').encode('utf8'))
                except:
                    t = text.match(row[1])
                if n and t:
                    campania.mensaje_set.create(destino=n.group(),
                                                contenido=t.group(),
                                                activado=True,
                                                intentos_fallidos=0,
                                                gateway_id=0)
    except:
        pass