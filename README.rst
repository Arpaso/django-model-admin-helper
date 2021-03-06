Django Model Admin Helpers
==========================

Link to repository: https://github.com/Arpaso/django-model-admin-helper

Provides classes to extend default django admin functionality:

* **ButtonableModelAdmin**
* **ModelAdminWithForeignKeyLinksMetaclass** - adds clickable foreign key      links at admin interface in list view; Uses **list_display** fields to try adding link to the field in list item.  
* **AdminURLMixin** - provides ability to extend /admin/ urls and make views to urls like: /admin/myurl.



Usage
=====

**admin.py**::

    from admin_helpers import ButtonableModelAdmin, AdminURLMixin, ModelAdminWithForeignKeyLinksMetaclass

    class MyModelAdmin(AdminURLMixin, ButtonableModelAdmin):
        __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass

        list_display = ('title', 'link_to_user') # user is a foreignkey field of the MyModel

        def get_urls(self):
            urls = super(MyModelAdmin, self).get_urls()
            my_urls = patterns('',
                (r'^my_view/$', self.my_view)
            )
            return my_urls + urls

        def my_view(self, request):
            # custom view which should return an HttpResponse
            pass

**Note**:
Notice that the custom patterns are included before the regular admin URLs: the admin URL patterns are very permissive and will match nearly anything, so you’ll usually want to prepend your custom URLs to the built-in ones.
In this example, my_view will be accessed at /admin/myapp/mymodel/my_view/ (assuming the admin URLs are included at /admin/.)

Written by the development team of Arpaso company: http://arpaso.com