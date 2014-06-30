import csv
from django.http import HttpResponse


def status2string(s):
    if s == -1:
        return 'No iniciado'
    elif s == 0:
        return 'Nuevo'
    elif s == 1:
        return 'Procesando'
    elif s == 2:
        return 'Enviado'
    else:
        return 'Error'


def register2unicode(obj, campo):
    reg = getattr(obj, campo)

    if campo == 'estado':
        reg = status2string(reg)

    return unicode(reg).encode("utf-8", "replace")


def multi_export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def multi_export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """

        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        m_fields = ['destino', 'estado', 'intentos_fallidos', 'hora_de_envio', 'error']

        writer = csv.writer(response)
        #if header:
            #writer.writerow(list(field_names))

        for obj in queryset:
            #writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
            writer.writerow([unicode(u'Campa\xf1a').encode("utf-8","replace"),
            unicode(getattr(obj, 'nombre')).encode("utf-8","replace")])
            writer.writerow([])
            #print m_fields
            writer.writerow([unicode(field).encode("utf-8", "replace") for field in m_fields])
            for m in obj.mensaje_set.all():
                writer.writerow([register2unicode(m, field) for field in m_fields])

            writer.writerow([])

        return response
    multi_export_as_csv.short_description = description
    return multi_export_as_csv


def one_export_as_csv(request):

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode('reporte')

        m_fields = ['destino', 'estado', 'intentos_fallidos', 'hora_de_envio', 'error']

        writer = csv.writer(response)

        writer.writerow([unicode(u'Campa\xf1a').encode("utf-8","replace"),
        unicode(getattr(request, 'nombre')).encode("utf-8","replace")])
        writer.writerow([])
        #print m_fields
        writer.writerow([unicode(field).encode("utf-8", "replace") for field in m_fields])
        for m in request.mensaje_set.all():
            writer.writerow([register2unicode(m, field) for field in m_fields])

        #print response

        return response