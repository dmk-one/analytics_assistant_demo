from django.db.models import TextChoices


class STATUS_CHOICES(TextChoices):
    SUCCESS = 'success'
    FAILURE = 'failure'
    UNKNOWN = 'unknown'


class METHOD_CHOICES(TextChoices):
    CARD = 'card'
    OTHER = 'other'
    UNKNOWN = 'unknown'
    ADMIN = 'admin'


# class SERVICE_PLAN_CHOICES(TextChoices):
#     SILVER = 'silver'
#     GOLD = 'gold'
#     PREMIUM = 'premium'
#     UNKNOWN = 'unknown'


class SERVICE_PLAN_TYPE_CHOICES(TextChoices):
    JURIDICAL = 'Juridical'
    INDIVIDUAL = 'Individual'
