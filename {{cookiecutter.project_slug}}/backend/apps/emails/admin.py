"""Admin configuration for email templates."""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import EmailTemplate, EmailLog


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'subject', 'category', 'language', 'is_active', 'updated_at']
    list_filter = ['template_type', 'is_active', 'category', 'language']
    search_fields = ['name', 'subject', 'html_content', 'text_content']
    readonly_fields = ['created_at', 'updated_at', 'preview_html']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'template_type', 'category', 'language', 'is_active')
        }),
        ('Email Content', {
            'fields': ('subject', 'html_content', 'text_content')
        }),
        ('Default Context', {
            'fields': ('default_context',),
            'description': 'Default variables to use when rendering this template'
        }),
        ('Preview', {
            'fields': ('preview_html',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_html(self, obj):
        """Show a preview of the rendered HTML template."""
        if obj.pk:
            try:
                rendered = obj.render()
                return format_html(
                    '<div style="border: 1px solid #ddd; padding: 10px; max-width: 600px;">'
                    '<h4>Subject: {}</h4>'
                    '<iframe srcdoc="{}" style="width: 100%; height: 400px; border: none;"></iframe>'
                    '</div>',
                    rendered['subject'],
                    rendered['html_content'].replace('"', '&quot;')
                )
            except Exception as e:
                return format_html('<div style="color: red;">Error rendering template: {}</div>', str(e))
        return "Save the template to see preview"
    
    preview_html.short_description = "Template Preview"
    
    actions = ['test_send_email']
    
    def test_send_email(self, request, queryset):
        """Send test email to admin user."""
        for template in queryset:
            try:
                template.send(
                    to_email=request.user.email,
                    context_data={'test': True, 'user': request.user}
                )
                self.message_user(
                    request,
                    f"Test email '{template.name}' sent to {request.user.email}"
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Failed to send '{template.name}': {str(e)}",
                    level='ERROR'
                )
    
    test_send_email.short_description = "Send test email to yourself"


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['to_email', 'subject', 'template_link', 'status', 'sent_at', 'created_at']
    list_filter = ['status', 'created_at', 'template']
    search_fields = ['to_email', 'subject', 'error_message']
    readonly_fields = ['to_email', 'from_email', 'subject', 'template', 'status', 
                      'sent_at', 'error_message', 'user', 'context_data', 'created_at']
    date_hierarchy = 'created_at'
    
    def template_link(self, obj):
        """Link to the email template."""
        if obj.template:
            url = reverse('admin:emails_emailtemplate_change', args=[obj.template.pk])
            return format_html('<a href="{}">{}</a>', url, obj.template.name)
        return '-'
    
    template_link.short_description = 'Template'
    
    def has_add_permission(self, request):
        """Prevent manual creation of email logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make email logs read-only."""
        return False
    
    actions = ['resend_failed_emails']
    
    def resend_failed_emails(self, request, queryset):
        """Resend failed emails."""
        resent_count = 0
        failed_count = 0
        
        for log in queryset.filter(status='failed'):
            if log.template:
                try:
                    log.template.send(
                        to_email=log.to_email,
                        context_data=log.context_data,
                        from_email=log.from_email
                    )
                    resent_count += 1
                except Exception:
                    failed_count += 1
        
        self.message_user(
            request,
            f"Resent {resent_count} emails, {failed_count} failed"
        )
    
    resend_failed_emails.short_description = "Resend failed emails"