from functools import partial

from django.contrib import admin
from django.utils.datastructures import SortedDict
from django.http import HttpResponseRedirect
from django.contrib.admin.options import RenameBaseModelAdminMethods

try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper


class ButtonableModelAdmin(admin.ModelAdmin):

    buttons = ()

    def change_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, admin.util.unquote(object_id))
        extra = {'buttons': self.get_buttons(request, obj).values()}
        extra.update(extra_context or {})

        return super(ButtonableModelAdmin, self).change_view(request, object_id, extra_context=extra)

    def button_view_dispatcher(self, request, object_id, command):
        obj = self.get_object(request, admin.util.unquote(object_id))
        response = self.get_buttons(request, obj)[command][0](request, obj)

        return response or HttpResponseRedirect(request.META['HTTP_REFERER'])

    def get_buttons(self, request, obj):
        """
        Return a dictionary mapping the names of all buttons for this
        ModelAdmin to a tuple of (callable, name, description) for each button.
        Each button may assign 'condition', which chould be callable with following attrs: self, request, obj
        """

        buttons = SortedDict()
        for name in self.buttons:
            handler = getattr(self, name)
            if getattr(handler, 'condition', lambda self, request, obj: True)(self, request, obj):
                buttons[name] = (handler, name,
                                 getattr(handler, 'short_description', name.replace('_', ' ')))

        return buttons

    def get_urls(self):

        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        return patterns('',
            *(url(r'^(\d+)/(%s)/$' % command, wrap(self.button_view_dispatcher)) for command in self.buttons)
        ) + super(ButtonableModelAdmin, self).get_urls()
    

class ModelAdminWithForeignKeyLinksMetaclass(RenameBaseModelAdminMethods):

    def __new__(cls, name, bases, attrs):
        new_class = super(ModelAdminWithForeignKeyLinksMetaclass, cls).__new__(cls, name, bases, attrs)

        def foreign_key_link(instance, field):
            target = getattr(instance, field)
            return u'<a href="../../%s/%s/%s/">%s</a>' % (
                target._meta.app_label, target._meta.module_name, target.pk, unicode(target))

        for col in new_class.list_display:
            if col[:8] == 'link_to_':
                field_name = col[8:]
                method = partial(foreign_key_link, field=field_name)
                method.__name__ = col[8:]
                method.allow_tags = True
                method.admin_order_field = field_name
                setattr(new_class, col, method)

        return new_class


class AdminURLMixin(object):
    
    def wrap(self, view):
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view)(*args, **kwargs)
        return update_wrapper(wrapper, view)
