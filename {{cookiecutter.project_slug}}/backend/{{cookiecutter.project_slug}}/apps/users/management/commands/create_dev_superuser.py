"""
Management command to create a default superuser for development.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a default superuser for development environment"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            default="admin@example.com",
            help="Email for the superuser",
        )
        parser.add_argument(
            "--username",
            type=str,
            default="admin",
            help="Username for the superuser",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="admin123",
            help="Password for the superuser",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Override existing superuser with the same email",
        )

    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]
        force = options["force"]

        # Check if we're in development
        from django.conf import settings
        if not settings.DEBUG and not force:
            self.stdout.write(
                self.style.ERROR(
                    "This command should only be run in development! "
                    "Use --force to override this check."
                )
            )
            return

        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                if force:
                    User.objects.filter(email=email).delete()
                    self.stdout.write(
                        self.style.WARNING(f"Deleted existing user with email {email}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"User with email {email} already exists. "
                            "Use --force to override."
                        )
                    )
                    return

            # Create superuser
            user = User.objects.create_superuser(
                email=email,
                username=username,
                password=password,
                first_name="Admin",
                last_name="User",
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nSuccessfully created superuser:"
                    f"\n  Email: {email}"
                    f"\n  Username: {username}"
                    f"\n  Password: {password}"
                    f"\n\n⚠️  Remember to change the password in production!"
                )
            )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to create superuser: {str(e)}")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"An error occurred: {str(e)}")
            )