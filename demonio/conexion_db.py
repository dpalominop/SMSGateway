#!/usr/bin/python

import MySQLdb
from sms_bucle import *
import time
import os
import signal
import sys


def Null_if_neg(i):
    if i in (-1, -2):
        return 'NULL'
    else:
        return str(i)

host = "localhost"
user = "root"
passw = "tccperu2013"
db_name = "sms"

db = None
cursor = None
debug = True


def main_proces():

    if debug:
        print "Abriendo conexion de base de datos : %s ..." % (db_name)
    db = MySQLdb.connect(host, user, passw, db_name)

    if db:
        if debug:
            print "Conexion establecida"
        cursor = db.cursor()


    else:
        if debug:
            print "Conexion rechazada\n"


    while True:
        while db is None:
            if debug:
                print "Reabriendo conexion de base de datos : %s ..." % (db_name)
            db = MySQLdb.connect(host, user, passw, db_name)

            if db:
                if debug:
                    print "Conexion establecida"
                cursor = db.cursor()

            else:
                if debug:
                    print "Conexion rechazada\n"

            time.sleep(1)

        sql = """select id, nombre, dia_de_inicio, dia_final, hora_de_inicio, hora_final, max_fallas from campanias
                where activado=1
                and dia_de_inicio <= current_date
                and dia_final >= current_date
                and (
                        (
                            hora_de_inicio <= hora_final and
                            hora_de_inicio <= current_time and
                            current_time <= hora_final
                        ) or (
                                hora_final < hora_de_inicio
                                and (
                                        hora_de_inicio <= current_time or
                                        current_time <= hora_final
                                    )
                            )
                )
        """

        try:

            if debug:
                print "\nBuscando campania para ejecutar ..."

            # Execute the SQL command
            db.commit()
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            campaign = cursor.fetchall()

            if campaign:

                if debug:
                    print "Se encontro una campania programada para ahora."
                    print "Informacion de campania:"
                    print campaign

                codigo = campaign[0][0]
                nombre = campaign[0][1]
                fecha_init = campaign[0][2]
                fecha_fin = campaign[0][3]
                hora_init = campaign[0][4]
                hora_fin = campaign[0][5]

                if str(hora_fin) < str(hora_init) and str(hora_init) <= time.strftime("%X"):
                    hora_fin = '23:59:59'

                max_fallas = campaign[0][6]

                if debug:
                    print "campania: %s, codigo: %d,\
     fecha de inicio: %s, fecha de fin: %s, horas a ejecutarse: %s - %s\
    " % (nombre, codigo, fecha_init, fecha_fin, hora_init, hora_fin)

                sql = """
                        select id, destino, contenido from mensajes
                        where campania_id = %d and activado = 1
                """ % (codigo)

                try:

                    if debug:
                        print "Cargando mensajes de campania seleccionada ..."

                    cursor.execute(sql)

                    fichero = cursor.fetchall()
                    mensajes = []

                    if debug:
                        print "fichero: ", fichero
                        print "Ejecutando envio de mensajes de campania ..."

                    campaign_run(fichero, hora_fin, fecha_fin, mensajes, max_fallas)

                    if debug:
                        print "Envio Finalizado"
                        print "Actualizando base de datos ..."

                    if str(fecha_fin) > time.strftime("%Y-%m-%d"):
                        sms_revisados = [m for m in mensajes if (m.estado in (2, 3)) or (m.message_id == -2)]
                    else:
                        sms_revisados = mensajes

                    for mensaje in sms_revisados:
                        sql = " ".join(["update mensajes set gateway_id = %s,"%(Null_if_neg(mensaje.message_id),),
                                "estado = %s,"%(Null_if_neg(mensaje.estado),),
                                "error = '%s',"%(mensaje.error,),
                                "intentos_fallidos = %d,"%(mensaje.failures,),
                                "activado = 0,",
                                "hora_de_envio = '%s',"%(mensaje.hora_de_envio,),
                                "hora_de_encola = '%s'"%(mensaje.hora_de_encola,),
                                "where id = %d"%(mensaje.indice,)])

                        try:
                            cursor.execute(sql)
                            db.commit()

                        except:
                            db.rollback()
                            if debug:
                                print "No se pudo actualizar registro.\
                                    indice de mensaje: ", mensaje.indice
                except:
                    if debug:
                        print "Error: Fallo al cargar mensajes"

                if str(fecha_fin) <= time.strftime("%Y-%m-%d") or (len(mensajes) == len(sms_revisados)):

                    sql = "update campanias set activado = 0 where id = %d" % (codigo)

                    try:
                        cursor.execute(sql)
                        db.commit()
                        if debug:
                            print "Campania %s finalizada" % (nombre)

                    except:
                        db.rollback()
                        if debug:
                            print "Error: Falla al actualizar tabla Campaigns"
                else:
                    if debug:
                        print "Campania %s NO finalizada. Hasta manhana ..." % (nombre)

                while True:
                    respuesta = os.system("ping -c 1 -w 3 %s > /dev/null" % lyric_ip)
                    if respuesta == 0:
                        obj = api_reset_queue()
                        if obj is None:
                            if debug:
                                print ('Error: Servicio desconectado')
                        else:
                            if obj['success']:
                                if debug:
                                    print "Cola reseteada exitosamente"
                                break
                            else:
                                if debug:
                                    print "No se pudo resetar la cola"
                    else:
                        if debug:
                            print ('Error: Servidor desconectado')

            else:
                if debug:
                    print "No hay campania programada para ahora"

        except:
            if debug:
                print "Error: Falla al ejecutar consulta de campanias pendientes"

        time.sleep(5)


def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    print "Cerrando proceso ..."
    time.sleep(2)
    if db:
        db.close()
        print "Servidor desconectado"

    print "Proceso cerrado"

    sys.exit(1)


if __name__ == "__main__":
    #set_exit_handler(on_exit)
    signal.signal(signal.SIGINT, on_exit)
    main_proces()