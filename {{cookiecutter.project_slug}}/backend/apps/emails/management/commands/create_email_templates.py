"""Management command to create default email templates."""
from django.core.management.base import BaseCommand
from apps.emails.models import EmailTemplate


class Command(BaseCommand):
    help = 'Create default email templates in the database'
    
    def handle(self, *args, **options):
        templates = [
            {
                'name': 'welcome',
                'template_type': 'welcome',
                'subject': 'Welcome to {% raw %}{{ site_name }}{% endraw %}!',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to {% raw %}{{ site_name }}{% endraw %}!</h1>
        </div>
        <div class="content">
            <h2>Hi {% raw %}{{ username }}{% endraw %},</h2>
            <p>Thank you for joining {% raw %}{{ site_name }}{% endraw %}! We're excited to have you on board.</p>
            <p>Your account has been successfully created with the email address: <strong>{% raw %}{{ email }}{% endraw %}</strong></p>
            <p>Here are some things you can do to get started:</p>
            <ul>
                <li>Complete your profile</li>
                <li>Explore our features</li>
                <li>Connect with other users</li>
            </ul>
            <center>
                <a href="{% raw %}{{ site_url }}{% endraw %}/dashboard" class="button">Go to Dashboard</a>
            </center>
            <p>If you have any questions, feel free to reach out to our support team.</p>
            <p>Best regards,<br>The {% raw %}{{ site_name }}{% endraw %} Team</p>
        </div>
        <div class="footer">
            <p>&copy; {% raw %}{{ site_name }}{% endraw %}. All rights reserved.</p>
            <p>You received this email because you signed up for {% raw %}{{ site_name }}{% endraw %}.</p>
        </div>
    </div>
</body>
</html>
                ''',
                'text_content': '''
Welcome to {% raw %}{{ site_name }}{% endraw %}!

Hi {% raw %}{{ username }}{% endraw %},

Thank you for joining {% raw %}{{ site_name }}{% endraw %}! We're excited to have you on board.

Your account has been successfully created with the email address: {% raw %}{{ email }}{% endraw %}

Here are some things you can do to get started:
- Complete your profile
- Explore our features
- Connect with other users

Visit your dashboard: {% raw %}{{ site_url }}{% endraw %}/dashboard

If you have any questions, feel free to reach out to our support team.

Best regards,
The {% raw %}{{ site_name }}{% endraw %} Team

---
You received this email because you signed up for {% raw %}{{ site_name }}{% endraw %}.
                '''
            },
            {
                'name': 'password_reset',
                'template_type': 'password_reset',
                'subject': 'Reset Your {% raw %}{{ site_name }}{% endraw %} Password',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f44336; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; padding: 12px 30px; background: #f44336; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .warning { background: #fff3cd; border: 1px solid #ffc107; padding: 10px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Password Reset Request</h1>
        </div>
        <div class="content">
            <h2>Hi {% raw %}{{ user.username }}{% endraw %},</h2>
            <p>We received a request to reset your password for your {% raw %}{{ site_name }}{% endraw %} account.</p>
            <p>Click the button below to reset your password:</p>
            <center>
                <a href="{% raw %}{{ reset_url }}{% endraw %}" class="button">Reset Password</a>
            </center>
            <div class="warning">
                <strong>Important:</strong> This link will expire in {% raw %}{{ expiry_hours }}{% endraw %} hours.
            </div>
            <p>If you didn't request this password reset, please ignore this email or contact support if you have concerns.</p>
            <p>Best regards,<br>The {% raw %}{{ site_name }}{% endraw %} Team</p>
        </div>
    </div>
</body>
</html>
                ''',
                'text_content': '''
Password Reset Request

Hi {% raw %}{{ user.username }}{% endraw %},

We received a request to reset your password for your {% raw %}{{ site_name }}{% endraw %} account.

Click the link below to reset your password:
{% raw %}{{ reset_url }}{% endraw %}

Important: This link will expire in {% raw %}{{ expiry_hours }}{% endraw %} hours.

If you didn't request this password reset, please ignore this email or contact support if you have concerns.

Best regards,
The {% raw %}{{ site_name }}{% endraw %} Team
                '''
            },
            {
                'name': 'email_verification',
                'template_type': 'email_verification',
                'subject': 'Verify Your Email Address',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #4CAF50; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; padding: 12px 30px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Verify Your Email Address</h1>
        </div>
        <div class="content">
            <h2>Hi {% raw %}{{ user.username }}{% endraw %},</h2>
            <p>Please verify your email address to complete your registration.</p>
            <center>
                <a href="{% raw %}{{ verification_url }}{% endraw %}" class="button">Verify Email</a>
            </center>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all;">{% raw %}{{ verification_url }}{% endraw %}</p>
            <p>Best regards,<br>The {% raw %}{{ site_name }}{% endraw %} Team</p>
        </div>
    </div>
</body>
</html>
                ''',
                'text_content': '''
Verify Your Email Address

Hi {% raw %}{{ user.username }}{% endraw %},

Please verify your email address to complete your registration.

Click the link below to verify your email:
{% raw %}{{ verification_url }}{% endraw %}

Best regards,
The {% raw %}{{ site_name }}{% endraw %} Team
                '''
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for template_data in templates:
            template, created = EmailTemplate.objects.update_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated template: {template.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: Created {created_count} templates, Updated {updated_count} templates'
            )
        )