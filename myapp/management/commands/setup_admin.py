from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the KAROS admin account"

    def handle(self, *args, **options):
        User = get_user_model()

        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": username,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.email = username
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Admin account created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Admin account updated successfully.")
            )