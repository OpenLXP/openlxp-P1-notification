from django.contrib import admin

from .models import (recipient, subject, template, email)


@admin.register(recipient)
class recipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_address', )


@admin.register(subject)
class subjectAdmin(admin.ModelAdmin):
    list_display = ('subject', )


@admin.register(template)
class templateAdmin(admin.ModelAdmin):
    list_display = ('template_type', )


@admin.register(email)
class emailAdmin(admin.ModelAdmin):
    list_display = ('sender', 'subject',
                    'template_type', 'reference', )
    readonly_fields = ('created', 'modified', )
