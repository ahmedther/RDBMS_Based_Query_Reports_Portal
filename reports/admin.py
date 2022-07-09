from django.contrib import admin
from .models import IAACR, FacilityDropdown


# Register Models
admin.site.register(IAACR)
admin.site.register(FacilityDropdown)


# CHnage admin Panel
admin.site.site_header = "Report Portal Admin Panel"
admin.site.site_title = "RDBMS RP Admin Panel"
admin.site.index_title = "Report Portal Administration"