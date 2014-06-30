# utils/admin_auth.py
# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _


def roles(self):
    #short_name = unicode # function to get group name
    short_name = lambda x:unicode(x)[:1].upper() # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in self.groups.all()])
    if self.user_permissions.count():
        p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'Grupos'


def last(self):
    fmt = "%b %d, %H:%M"
    #fmt = "%Y %b %d, %H:%M:%S"
    value = self.last_login.strftime(fmt)
    return mark_safe("<nobr>%s</nobr>" % value)
last.allow_tags = True
last.admin_order_field = 'last_login'
last.short_description = u"Último inicio de sesión"


def adm(self):
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'
adm.short_description = u"Administrador"


def staff(self):
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'


def only_name(self):
    return self.first_name
only_name.short_description = u"Nombres"


def group_name(self):
    return self.name
group_name.short_description = u"Nombre de Grupo"

from django.core.urlresolvers import reverse


def persons(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in self.user_set.all().order_by('username')])
persons.allow_tags = True
persons.short_description = u"Usuarios por Grupo"


class UserAdminForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                           widget=FilteredSelectMultiple('Grupos', False),
                                           required=False,
                                           label="Grupos",
                                           help_text="Seleccionar los GRUPOS en los que se incluya este USUARIO")

    class Meta:
        model = User
        #exclude = ('user_permissions',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['groups'] = instance.groups.all()
            kwargs['initial'] = initial
        super(UserAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserAdminForm, self).save(commit=commit)

        if commit:
            user.group_set = self.cleaned_data['groups']
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                user.group_set = self.cleaned_data['groups']
            self.save_m2m = new_save_m2m
        return user


class MyUserAdmin(UserAdmin):
    form = UserAdminForm
    list_display = ['username', only_name, 'last_name', staff, adm, last]
    list_filter = ['groups', 'is_staff', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                       'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=FilteredSelectMultiple('Usuarios', False),
                                           required=False,
                                           label="Usuarios",
                                           help_text="Seleccionar los USUARIOS que desea incluir a este GRUPO")

    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['users'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(GroupAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super(GroupAdminForm, self).save(commit=commit)

        if commit:
            group.user_set = self.cleaned_data['users']
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                group.user_set = self.cleaned_data['users']
            self.save_m2m = new_save_m2m
        return group


class GroupAdmin(GroupAdmin):
    form = GroupAdminForm

    list_display = [group_name, persons]
    list_display_links = [group_name]


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, MyUserAdmin)
admin.site.register(Group, GroupAdmin)
