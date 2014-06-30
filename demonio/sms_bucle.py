#!/usr/bin/python

from subprocess import *
from sms_api import *
import os
import time

debug = True
# Clase que implementa la estructura y principales funciones de un SMS
# Atributos
#     estado: Estado en el que se encuentra el mensaje
#                    -1: Mensaje no iniciado
#                     0: Nuevo
#                     1: Procesando
#                     2: Enviado
#                     3: Fallo
#     contenido: Contenido del SMS
#     destino: Numero del destino
#     message_id: Ticket que identifica el mensaje
#
# Metodos
#     queue: Encola el mensaje utilizando el comando api_queue_sms de la API Web
#     get_status: Obtiene el estado actual del mensaje utilizando el comando api_get_status de la API Web
#
#     Los argumentos para invocar ambos metodos son los mismos:
#            url: Considera datos de autentificacion a servidor web y ruta del CGI que ejecuta los comandos API
#            api_user, api_pass: Autentificacion a API web
#            api_version: Version de API web que soporta el equipo
#
# Iniciacion
#     Cada mensaje se inicia como: msg = Mensaje(destino, contenido)
#
# Errores
#     En caso de que ocurra un error en los metodos, estos son escritos en la salida estandar. Revisar documentacion API Web.


def format_date(s):
    if s == u'0':
        return ''
    else:
        return time.strftime('%Y-%m-%d %X', time.localtime(long(s)))


class Mensaje:
    indice = 0
    estado = -1
    contenido = ""
    destino = ""
    message_id = -1
    failures = 0
    error = ""
    hora_de_envio = ""
    hora_de_encola = ""

    def __init__(self, indice, destino, contenido):
        self.indice = indice
        self.estado = 0
        self.destino = destino
        self.contenido = contenido

    def queue(self):
        respuesta = os.system("ping -c 1 -w 3 %s > /dev/null" % lyric_ip)
        if respuesta == 0:
            obj = api_queue_sms(self.destino, self.contenido)
            if obj is None:
                self.estado = -1
                if debug:
                    if debug:
                        print ('Error: Servicio desconectado')
                self.error = 'Servicio desconectado'
                return -1
            else:
                if obj['success']:
                    self.estado = 0
                    self.message_id = obj['message_id']
                    #self.error = obj['error_code']
                    if debug:
                        print ('Mensaje insertado exitosamente. Ticket: ' + str(obj['message_id']))
                    return 1
                else:
                    self.estado = -1
                    self.message_id = -2
                    self.error = obj['error_code']
                    if debug:
                        print ('Error al insertar mensaje. Codigo de error: ' + obj['error_code'])
                    return -1
        else:
            self.estado = -1
            if debug:
                print ("Error: Servidor desconectado")
            self.error = "Servidor desconectado"

    def get_status(self):
        if self.estado == -1 or self.estado == 2:
            return 1

        respuesta = os.system("ping -c 1 -w 3 %s > /dev/null" % lyric_ip)
        if respuesta == 0:
            obj = api_get_status(self.message_id)
            if obj is None:
                if debug:
                    print ('Error: Servicio desconectado')
                self.error = 'Servicio desconectado'
                time.sleep(5)
                return -1
            else:
                if obj['success']:
                    self.failures = obj['n_tries']
                    self.estado = obj['message_status']
                    self.error = ""
                    self.hora_de_envio = str(format_date(obj[u'send_date']))
                    self.hora_de_encola = str(format_date(obj[u'recv_date']))

                    if debug:
                        print ('Ticket: ' + str(self.message_id),
                                ' Estado: ' + str(self.estado),
                                'Intentos: ' + str(self.failures),
                                'hora de encola: ' + str(self.hora_de_encola),
                                'hora de envio: ' + str(self.hora_de_envio))
                    return 1
                else:
                    self.error = obj['error_code']
                    if debug:
                        print ('Error al consultar estado. Codigo de error: ' + obj['error_code'])
                    time.sleep(5)
                    return -1
        else:
            if debug:
                print ('Error: Servidor desconectado')
            self.error = 'Servidor desconectado'
            time.sleep(5)
            return -1

    def remove_queue(self):
        respuesta = os.system("ping -c 1 -w 3 %s > /dev/null" % lyric_ip)
        if respuesta == 0:
            obj = api_sms_delete_by_id(self.message_id)
            if obj is None:
                if debug:
                    print ('Error: Servicio desconectado')
                self.error = 'Servicio desconectado'
                time.sleep(5)
                return -1
            else:
                if obj['success']:
                    self.message_id = -2
                    if debug:
                        print ('Mensaje borrado exitosamente. Ticket: ' + str(self.message_id))
                        time.sleep(5)
                    return 1
                else:
                    if debug:
                        print ('Error al borrar mensaje. Codigo de error: ' + obj['error_code'])
                    time.sleep(5)
                    return -1
        else:
            if debug:
                print ('Error: Servidor desconectado')
            self.error = 'Servidor desconectado'
            time.sleep(5)
            return -1


def campaign_run(fichero, hora_fin, dia_fin, mensajes, max_intentos):

    if debug:
        print ("Creando lista con los mensajes extraidos de la base de datos ...")

    for row in fichero:
        mensajes.append(Mensaje(row[0], row[1], row[2]))

    if debug:
        print ("Lista creada")
        print "Revisando conexion de red con lyric ..."

    while(True):
        respuesta = os.system("ping -c 1 -w 3 %s > /dev/null" % lyric_ip)
        if respuesta == 0:
            if debug:
                print "Conexion establecida con lyric"
            break
        else:
            if debug:
                print "No se pudo establecer conexion con lyric"

    #print ("Obteniendo estado de los canales:")

    #api_get_channels_status()
    #api_get_queue_status()

    #time.sleep(10)

    if debug:
        print ("Iniciando envio de mensajes ...")

    #Numero de sms enviados al inicio.
    sms_send = 0
    #Maximo numero de sms enviados a la cola al mismo tiempo.
    sms_max = 100
    #Cantidad total de sms a enviar.
    sms_len = len(mensajes)
    #Maxima cantidad de envios fallidos antes de ser eliminado de la cola.
    max_failures = max_intentos
    #inicio y final de la trama de sms a evaluar por cada iteracion.
    init = 0
    last = min(sms_max, sms_len)

    #Bucle principal.
    while (str(hora_fin) > time.strftime("%X") and str(dia_fin) >= time.strftime("%Y-%m-%d")):
    #Si el inicio y final son iguales, significa que ya se recorrio por todos
    #los sms existenes en la lista total o que ya no hay espacio en la cola para
    #otros sms debido a que se igualo a la cantidad maxima de sms encolados.
        if (init == last):
            #Si todos los mensajes en la lista poseen estado de Enviado o
            #tienen intentos fallido mayores que max_failures, se
            #sale del bucle principal.
            if len([m for m in mensajes if m.estado == 2 or m.estado == 3 or m.message_id == -2]) == sms_len:
                break
            #Si todos los mensajes de la lista poseen un message_id diferente
            #de -1, significa que ya han sido asignados a la cola. Hay que volver
            #a evaluar los nuevos estados de los sms de la cola.
            elif len([m for m in mensajes if m.message_id != -1]) == sms_len:
                init = 0
                last = sms_len
            else:
                #Si no se cumple ninguno de las condiciones anteriores es porque
                #aun hay sms en la lista que no han sido asignados a la cola.
                if last == sms_len:
                    init = 0

    #Se agrupa a todos los sms de la lista dentro del tramo actual que NO han
    #sido asignados a la cola.
        l_msm = [m for m in mensajes[init:last] if m.message_id == -1]
    #Si la cantidad de sms de este grupo es menor a la cantidad planificada para
    #esta iteracion, se coge el siguiente sms en la lista hasta completar la
    #cantidad planificada.
        if len(l_msm) < (last - init):
            l_tmp = last - init
            while last < sms_len:
                    if mensajes[last].message_id == -1:
                        l_msm.append(mensajes[last])
                        last = last + 1
                        #Si ya se llego al final de la lista, se termina la
                        #busqueda de sms faltantes y se trabaja con los que hayan.
                        if len(l_msm) == l_tmp:
                            break
                    else:
                        last = last + 1
    #Se intenta encolar los sms agrupados anteriormente.
        for mensaje in l_msm:
            if debug:
                print ("Encolando mensajes ...")
            if mensaje.queue() == -1:
                #Si la cantidad de sms encolados exitosame.format(max_failuresnte son menores a la
                #cantidad de sms planificados para esta iteracion, se intenta
                #encolar a los siguientes de la lista.
                while last < sms_len:
                    if mensajes[last].message_id == -1:
                        l_msm.append(mensajes[last])
                        last = last + 1
                        break
                    last = last + 1

                if debug:
                    print ("Mensaje NO encolado")

            elif debug:
                print ("Mensaje encolado")
    #Se actualiza el estado de los sms encolados hasta ahora y que aun NO han
    #sido enviados exitosamente.
        sms_send = 0
        for mensaje in [m for m in mensajes if m.message_id not in (-1, -2)]:

            if mensaje.get_status() == 1:
                #Se guarda la cantidad de sms encolados que acaban de cambiar su
                #estado a Enviado exitosamente. Porque esta cantidad es igual a los
                #nuevos sms que se puede encolar sin sobrepasar la cantidad maxima en la cola.
                if mensaje.estado == 2:
                    if mensaje.remove_queue() == 1:
                        sms_send = sms_send + 1
                if (mensaje.estado == 3) or (mensaje.failures >= max_failures):
                    if mensaje.remove_queue() == 1:
                        mensaje.estado = 3
                        sms_send = sms_send + 1

    #Se actualizan los valores de inicio y fin para la siguiente iteracion.
        init = last
        last = min(last + sms_send, sms_len)
