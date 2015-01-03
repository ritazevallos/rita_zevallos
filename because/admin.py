from django.contrib import admin

from ritazevallos.because.models import Beginning, Ending

class BeginningAdmin(admin.ModelAdmin):
    pass
admin.site.register(Beginning, BeginningAdmin)

class EndingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ending, EndingAdmin)