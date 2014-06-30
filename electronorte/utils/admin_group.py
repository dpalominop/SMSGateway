from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import GroupAdmin
#from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group


class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=FilteredSelectMultiple('Users', False),
                                           required=False,
                                           label="Usuarios")

    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['users'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        #print "kwargs: ", kwargs

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


class MyGroupAdmin(GroupAdmin):
    form = GroupAdminForm

#site = admin.AdminSite()
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)