import json
import urllib

# Username en el servidor web del equipo
web_user = 'admin'

# Password en el servidor web del equipo
web_pass = 'Pata'

# IP del equipo
lyric_ip = '10.112.34.5'

# Nombre de usuario de la API
api_user = 'lyric_api'

# Password de la API
api_pass = 'lyric_api'

# Version de la API Web soportada por el equipo
# Se puede obtener utilizando el comando api_get_version
api_version = '0.07'

# Ubicacion del CGI que implementa las funciones de la API
url = "http://" + web_user + ":" + web_pass + "@" + lyric_ip + "/cgi-bin/exec"
debug = True


def api_queue_sms(destino, contenido):
    try:
        args = urllib.urlencode({'cmd': 'api_queue_sms', 'content': contenido,
                                        'destination': destino, 'username': api_user,
                                        'password': api_pass, 'api_version': api_version})
        if debug:
            print "args: ", args

        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ("res: \n", res)

        obj = json.loads(res)
        if debug:
            print ("obj: \n", obj)

        return obj

    except:
        return None


def api_get_status(message_id):
    try:
        args = urllib.urlencode({'cmd': 'api_get_status', 'message_id': message_id,
                'username': api_user, 'password': api_pass, 'api_version': api_version})
        if debug:
            print ('args: ', args)
        res = urllib.urlopen(url + '?' + args).read()
        #if debug:
            #print ('res: ', res)
        obj = json.loads(res)
        #if debug:
            #print ('obj: ', obj)

        return obj

    except:
        return None


def api_sms_delete_by_id(message_id):
    try:
        args = urllib.urlencode({'cmd': 'api_sms_delete_by_id', 'sms_dir': 'out',
                                        'id': message_id, 'username': api_user,
                                        'password': api_pass, 'api_version': api_version})
        if debug:
            print ('args: ', args)
        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ('res: ', res)
        obj = json.loads(res)
        if debug:
            print ('obj: ', obj)

        return obj

    except:
        return None


def api_sms_delete_by_status(status):
    try:
        args = urllib.urlencode({'cmd': 'api_sms_delete_by_status', 'sms_dir': 'out',
                                        'status': status, 'username': api_user,
                                        'password': api_pass, 'api_version': api_version})
        if debug:
            print ('args: ', args)
        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ('res: ', res)
        obj = json.loads(res)
        if debug:
            print ('obj: ', obj)

        return obj

    except:
        return None


def api_get_channels_status():
    try:
        args = urllib.urlencode({'cmd': 'api_get_channels_status', 'username': api_user,
         'password': api_pass, 'api_version': api_version})
        if debug:
            print (args)

        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ("res: ", res)

        obj = json.loads(res)

        return obj

    except:
        return None


def api_get_queue_status():
    try:
        args = urllib.urlencode({'cmd': 'api_get_queue_status', 'username': api_user,
         'password': api_pass, 'api_version': api_version})
        if debug:
            print (args)

        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ("res: ", res)

        obj = json.loads(res)

        return obj

    except:
        return None


def api_reset_queue():
    try:
        args = urllib.urlencode({'cmd': 'api_reset_queue', 'username': api_user,
         'password': api_pass, 'api_version': api_version, 'sms_dir': 'out'})
        if debug:
            print (args)

        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ("res: ", res)

        obj = json.loads(res)

        return obj

    except:
        return None


def api_sms_send_enable():
    try:
        args = urllib.urlencode({'cmd': 'api_sms_send_enable', 'username': api_user,
         'password': api_pass, 'api_version': api_version, 'sms_dir': 'out'})
        if debug:
            print (args)

        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ("res: ", res)

        obj = json.loads(res)

        return obj

    except:
        return None


def api_sms_available_space():
    try:
        args = urllib.urlencode({'cmd': 'api_sms_available_space', 'username': api_user,
         'password': api_pass, 'api_version': api_version, 'sms_dir': 'out'})
        if debug:
            print (args)

        res = urllib.urlopen(url + '?' + args).read()
        if debug:
            print ("res: ", res)

        obj = json.loads(res)

        return obj

    except:
        return None