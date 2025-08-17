"""Email template models."""
from django.db import models
from django.template import Context, Template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class EmailTemplate(models.Model):
    """Database-stored email templates."""
    
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Email'),
        ('password_reset', 'Password Reset'),
        ('email_verification', 'Email Verification'),
        ('account_activation', 'Account Activation'),
        ('notification', 'General Notification'),
        ('newsletter', 'Newsletter'),
        ('order_confirmation', 'Order Confirmation'),
        ('invoice', 'Invoice'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES, default='custom')
    subject = models.CharField(max_length=200)
    html_content = models.TextField(help_text="HTML template with Django template variables")
    text_content = models.TextField(help_text="Plain text template with Django template variables")
    
    # Optional fields for categorization
    category = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=10, default='en')
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional default context as JSON
    default_context = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['template_type', 'is_active']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def render(self, context_data=None):
        """Render the email template with given context."""
        context = self.default_context.copy()
        if context_data:
            context.update(context_data)
        
        # Add common context variables
        context.update({
            'site_name': getattr(settings, 'SITE_NAME', '{{ cookiecutter.project_name }}'),
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
            'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@example.com'),
        })
        
        # Render templates
        html_template = Template(self.html_content)
        text_template = Template(self.text_content)
        subject_template = Template(self.subject)
        
        context_obj = Context(context)
        
        return {
            'subject': subject_template.render(context_obj),
            'html_content': html_template.render(context_obj),
            'text_content': text_template.render(context_obj),
        }
    
    def send(self, to_email, context_data=None, from_email=None, attachments=None):
        """Send the email to specified recipient."""
        rendered = self.render(context_data)
        
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        
        msg = EmailMultiAlternatives(
            subject=rendered['subject'],
            body=rendered['text_content'],
            from_email=from_email,
            to=[to_email] if isinstance(to_email, str) else to_email,
        )
        
        msg.attach_alternative(rendered['html_content'], "text/html")
        
        if attachments:
            for attachment in attachments:
                msg.attach_file(attachment)
        
        return msg.send()


class EmailLog(models.Model):
    """Log of sent emails for tracking and debugging."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]
    
    template = models.ForeignKey(
        EmailTemplate, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='logs'
    )
    
    # Email details
    to_email = models.EmailField()
    from_email = models.EmailField()
    subject = models.CharField(max_length=200)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Optional user tracking
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs'
    )
    
    # Metadata
    context_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['to_email', 'status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.to_email} - {self.subject} ({self.status})"