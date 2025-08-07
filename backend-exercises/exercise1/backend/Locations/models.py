from django.db import models
import uuid
from typing import Optional

# Create your models here.

class Country(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name: str = models.CharField(max_length=100)
    country_code: str = models.CharField(max_length=10, unique=True)
    curr_symbol: str = models.CharField(max_length=10)
    phone_code: str = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.name} ({self.country_code})"
    
class State(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name: str = models.CharField(max_length=100)
    state_code: str = models.CharField(max_length=10, unique=True)
    gst_code: Optional[str] = models.CharField(max_length=15, blank=True, null=True)

    country: Country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self) -> str:
        return f"{self.name} ({self.state_code}) in {self.country.name}"
    
class City(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name: str = models.CharField(max_length=100)
    city_code: str = models.CharField(max_length=10, unique=True)
    phone_code: str = models.CharField(max_length=10)
    population: int = models.PositiveIntegerField()
    avg_age: float = models.FloatField()
    num_of_adult_males: int = models.PositiveIntegerField()
    num_of_adult_females: int = models.PositiveIntegerField()

    state: State = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self) -> str:
        return f"{self.name} ({self.city_code}) in {self.state.name}, {self.state.country.name}"