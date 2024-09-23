from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    # Flag to indicate usage in migrations
    use_in_migrations = True

    # Method to create a user
    def create_user(self, email, password=None, **extra_fields):
        # Check if email is provided
        if not email:
            raise ValueError('Email is required.')

        email = self.normalize_email(email)
        # Create user instance with provided email and extra fields
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Set password for the user
        user.save(using=self._db)  # Save user in the database
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
