import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"

    property = models.ForeignKey(
        Property,
        related_name="units",
        on_delete=models.CASCADE,
    )
    unit_number = models.CharField(max_length=50)
    monthly_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=(MinValueValidator(0),),
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("property_id", "unit_number")
        constraints = [
            models.UniqueConstraint(
                fields=("property", "unit_number"),
                name="unique_unit_number_per_property",
            ),
            models.CheckConstraint(
                condition=models.Q(monthly_rent__gte=0),
                name="unit_monthly_rent_nonnegative",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.unit_number}"
