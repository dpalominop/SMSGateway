# -*- coding: utf-8 -*-
from electronorte.models import Campania, Mensaje
from django.contrib import admin
from django import forms
from utils.export_csv import *
from utils.load_messages import *
from utils.submit_button import *
#from django.utils.safestring import mark_safe


class CampaniaForm(forms.ModelForm):
    archivo_CSV = forms.FileField(required=False, label="Archivo CSV")

    class Meta:
        model = Campania
        fields = ('nombre', 'dia_de_inicio', 'dia_final', 'hora_de_inicio',
                    'hora_final', 'activado', 'max_fallas', 'archivo_CSV')

    def save(self, commit=True):
        campaign = super(CampaniaForm, self).save(commit=False)
        real_activado = campaign.activado
        campaign.activado = False
        campaign.save()

        if self.cleaned_data['archivo_CSV'] is not None:
            loadMessagesFromMemory(campaign, self.cleaned_data['archivo_CSV'])

        campaign.activado = real_activado
        campaign.save()

        return campaign


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ('destino', 'contenido', 'estado', 'error', 'hora_de_envio')


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 0
    form = MensajeForm


class CampaniaAdmin(admin.ModelAdmin):
    #def button(self, request):
        #print "request: ", request

        #return mark_safe('<input type="button" value="ssss" onclick="%s" />' % one_export_as_csv(request))
    #button.short_description = 'Action'
    #button.allow_tags = True

    fieldsets = [
            (None, {'fields': ['nombre']}),
            ('Duración de la campaña', {'fields': ['dia_de_inicio', 'dia_final']}),
            ('Horario', {'fields': ['hora_de_inicio', 'hora_final']}),
            ('Activar?', {'fields': ['activado']}),
            ('Leer Archivo CSV', {'fields': ['archivo_CSV']}),
            ('Máxima cantidad de intentos de envío por mensaje', {'fields': ['max_fallas']})
        ]
    inlines = [MensajeInline]
    list_display = ('nombre', 'dia_de_inicio', 'dia_final', 'num_mensajes',
                    'enviados', 'activo', 'remove')
    list_filter = ['dia_de_inicio', 'dia_final']
#    list_editable = ['archivo_CSV']

    search_fields = ['nombre']
    date_hierarchy = 'dia_de_inicio'
    list_per_page = 50
    #save_on_top = True

    form = CampaniaForm

    def make_enabled(self, request, queryset):
        rows_updated = queryset.update(activado=True)

        if rows_updated == 1:
            message_bit = u"Una campa\xf1a fue"
        else:
            message_bit = u"%s campa\xf1as fueron" % rows_updated
        self.message_user(request, "%s satisfactoriamente abilitadas" % message_bit)

    make_enabled.short_description = u"Selecciona las campa\xf1as para activar"

    def make_disabled(self, request, queryset):
        rows_updated = queryset.update(activado=False)

        if rows_updated == 1:
            message_bit = u"Una campa\xf1a fue"
        else:
            message_bit = "%s campanias fueron" % rows_updated
        self.message_user(request, "%s satisfactoriamente abilitadas" % message_bit)

    make_disabled.short_description = u"Selecciona las campa\xf1as para desactivar"

    #actions = ['make_enabled', 'make_disabled']
    actions = [multi_export_as_csv_action("Exportar como CSV")]


admin.site.register(Campania, CampaniaAdmin)
import utils.admin_auth