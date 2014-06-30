#!/usr/bin/python

import csv
import re


#Se verifica que los datos ingresados sean coherentes.
number = re.compile('[0-9]{9,10}')
text = re.compile('([ -~]){0,160}')


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
    csvfile = csv.reader(archivo, delimiter=';')

    for row in csvfile:
        n = number.match(row[0])
        t = text.match(row[1])
        if n and t:
            campania.mensaje_set.create(destino=n.group(),
                                        contenido=t.group(),
                                        activado=True,
                                        intentos_fallidos=0,
                                        gateway_id=0)