"""Email service for sending templated emails."""
import logging
from typing import Dict, List, Optional, Any
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

from .models import EmailTemplate, EmailLog

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails with templates."""
    
    @staticmethod
    def send_templated_email(
        template_name: str,
        to_email: str | List[str],
        context: Optional[Dict[str, Any]] = None,
        from_email: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        use_db_template: bool = True,
        log_email: bool = True,
    ) -> bool:
        """
        Send an email using a template.
        
        Args:
            template_name: Name of the template to use
            to_email: Recipient email(s)
            context: Context data for template rendering
            from_email: Sender email (defaults to DEFAULT_FROM_EMAIL)
            attachments: List of file paths to attach
            use_db_template: Whether to use database template or file template
            log_email: Whether to log the email in the database
        
        Returns:
            Boolean indicating success
        """
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            context = context or {}
            
            # Ensure to_email is a list
            if isinstance(to_email, str):
                to_email = [to_email]
            
            if use_db_template:
                # Try to get template from database
                try:
                    template = EmailTemplate.objects.get(name=template_name, is_active=True)
                    rendered = template.render(context)
                    subject = rendered['subject']
                    html_content = rendered['html_content']
                    text_content = rendered['text_content']
                    
                except EmailTemplate.DoesNotExist:
                    logger.warning(f"Database template '{template_name}' not found, falling back to file template")
                    use_db_template = False
            
            if not use_db_template:
                # Use file-based templates
                subject = render_to_string(f'emails/{template_name}_subject.txt', context).strip()
                html_content = render_to_string(f'emails/{template_name}.html', context)
                text_content = render_to_string(f'emails/{template_name}.txt', context)
            
            # Create email message
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=to_email,
            )
            
            msg.attach_alternative(html_content, "text/html")
            
            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    msg.attach_file(attachment)
            
            # Send email
            result = msg.send()
            
            # Log email if requested
            if log_email:
                EmailLog.objects.create(
                    template=template if use_db_template and 'template' in locals() else None,
                    to_email=', '.join(to_email),
                    from_email=from_email,
                    subject=subject,
                    status='sent' if result else 'failed',
                    sent_at=timezone.now() if result else None,
                    context_data=context,
                )
            
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            
            # Log failed email
            if log_email:
                EmailLog.objects.create(
                    to_email=', '.join(to_email) if isinstance(to_email, list) else to_email,
                    from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                    subject=template_name,
                    status='failed',
                    error_message=str(e),
                    context_data=context or {},
                )
            
            return False
    
    @staticmethod
    def send_bulk_emails(
        template_name: str,
        recipients: List[Dict[str, Any]],
        from_email: Optional[str] = None,
        batch_size: int = 50,
    ) -> Dict[str, Any]:
        """
        Send bulk emails to multiple recipients.
        
        Args:
            template_name: Name of the template to use
            recipients: List of dicts with 'email' and 'context' keys
            from_email: Sender email
            batch_size: Number of emails to send in each batch
        
        Returns:
            Dictionary with success count and failed emails
        """
        success_count = 0
        failed_emails = []
        
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]
            
            for recipient in batch:
                email = recipient.get('email')
                context = recipient.get('context', {})
                
                if EmailService.send_templated_email(
                    template_name=template_name,
                    to_email=email,
                    context=context,
                    from_email=from_email,
                    log_email=True,
                ):
                    success_count += 1
                else:
                    failed_emails.append(email)
        
        return {
            'success_count': success_count,
            'failed_emails': failed_emails,
            'total': len(recipients),
        }


# Convenience functions for common emails
def send_welcome_email(user, **kwargs):
    """Send welcome email to new user."""
    context = {
        'user': user,
        'username': user.username,
        'email': user.email,
        **kwargs
    }
    
    return EmailService.send_templated_email(
        template_name='welcome',
        to_email=user.email,
        context=context,
    )


def send_password_reset_email(user, reset_url, **kwargs):
    """Send password reset email."""
    context = {
        'user': user,
        'reset_url': reset_url,
        'expiry_hours': 24,
        **kwargs
    }
    
    return EmailService.send_templated_email(
        template_name='password_reset',
        to_email=user.email,
        context=context,
    )


def send_email_verification(user, verification_url, **kwargs):
    """Send email verification link."""
    context = {
        'user': user,
        'verification_url': verification_url,
        **kwargs
    }
    
    return EmailService.send_templated_email(
        template_name='email_verification',
        to_email=user.email,
        context=context,
    )