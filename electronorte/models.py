from django.db import models
import time


class Campania(models.Model):
    class Meta:
        verbose_name = u'Campa\xf1a'
        verbose_name_plural = u'Campa\xf1as'
        db_table = 'campanias'

    nombre = models.CharField(max_length=40)
    dia_de_inicio = models.DateField()
    dia_final = models.DateField()
    hora_de_inicio = models.TimeField()
    hora_final = models.TimeField()
    activado = models.BooleanField(default=True)
    max_fallas = models.IntegerField(default=2, blank=True, verbose_name=u"N\u00FAmero")
    #archivo_CSV = models.FileField(upload_to='documents/%Y/%m/%d')

    def __unicode__(self):
        return self.nombre

    def activo(self):
        if(str(self.hora_de_inicio) <= str(self.hora_final) and
            str(self.hora_final) <= time.strftime("%X") and
            str(self.dia_final) <= time.strftime("%Y-%m-%d") and
            (self.activado is True)):

            self.activado = False
            self.save()

        if(str(self.hora_final) < str(self.hora_de_inicio) and
            str(self.dia_final) < time.strftime("%Y-%m-%d") and
            (self.activado is True)):

            self.activado = False
            self.save()

        return self.activado

    activo.admin_order_field = 'activado'
    activo.boolean = True
    activo.short_description = 'Activo'

    def enviados(self):
        return len(self.mensaje_set.filter(estado=2))

    enviados.short_description = "Mensajes Enviados"

    def num_mensajes(self):
        return len(self.mensaje_set.all())

    num_mensajes.short_description = u'Mensajes Totales'

    def remove(self):
        return '<input type="button" value="Borrar" onclick="location.href=\'%s/delete/\'" />' % (self.pk)
    remove.short_description = 'Acciones'
    remove.allow_tags = True


class Mensaje(models.Model):
    class Meta:
        db_table = 'mensajes'

    campania = models.ForeignKey(Campania)
    destino = models.CharField(max_length=16)
    contenido = models.CharField(max_length=160)
    estado = models.IntegerField(default=0, blank=True, null=True)
    error = models.CharField(max_length=40, default='', blank=True)
    intentos_fallidos = models.IntegerField(default=0)
    gateway_id = models.IntegerField(default=0, null=True)
    activado = models.BooleanField(default=True)
    hora_de_envio = models.CharField(max_length=19, default='', blank=True)
    hora_de_encola = models.CharField(max_length=19, default='', blank=True)

    def __unicode__(self):
        return self.destino