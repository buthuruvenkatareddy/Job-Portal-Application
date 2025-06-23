from django.contrib import admin
from .models import Job, Application, Profile

# Custom Admin Site to add custom styles
class MyAdminSite(admin.AdminSite):
    site_header = "Job Portal Admin"
    site_title = "Job Portal Admin Portal"
    index_title = "Welcome to Job Portal Admin Dashboard"

    class Media:
        css = {
            'all': ('css/admin_custom.css',)  # This refers to static/css/admin_custom.css
        }

# Create an instance of our custom Admin site
custom_admin_site = MyAdminSite(name='custom_admin')

# Register models using the default admin site (optional if not using custom site)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Profile)
