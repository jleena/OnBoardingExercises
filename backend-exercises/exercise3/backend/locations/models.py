from django.db import models
from django.conf import settings
import uuid
from django.core.exceptions import ValidationError


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, unique=True)
    curr_symbol = models.CharField(max_length=10)
    phone_code = models.CharField(max_length=10, unique=True)

    my_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='countries'
    )

    class Meta:
        unique_together = [('my_user', 'name')]  # Each user can't have duplicate country names

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10, unique=True)
    gst_code = models.CharField(max_length=15, blank=True, null=True, unique=True)

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='states'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country', 'name'],
                name='unique_state_name_per_country'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.state_code}) in {self.country.name}"


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10)
    phone_code = models.CharField(max_length=10, unique=True)

    population = models.PositiveIntegerField()
    avg_age = models.FloatField()
    num_of_adult_males = models.PositiveIntegerField()
    num_of_adult_females = models.PositiveIntegerField()

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name='cities'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['state', 'name'],
                name='unique_city_name_per_state'
            ),
            models.UniqueConstraint(
                fields=['state', 'city_code'],
                name='unique_city_code_per_state'
            )
        ]

    def clean(self):
        if self.population <= (self.num_of_adult_males + self.num_of_adult_females):
            raise ValidationError("Population must be greater than total adult males and females.")

    def __str__(self):
        return f"{self.name} ({self.city_code}) in {self.state.name}, {self.state.country.name}"
