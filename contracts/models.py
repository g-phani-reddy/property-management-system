import uuid

from django.core.validators import MinValueValidator
from django.db import models

from members.models import Member
from properties.models import Unit


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(
        Unit,
        related_name="contracts",
        on_delete=models.PROTECT,
        db_index=False,
    )
    member = models.ForeignKey(
        Member,
        related_name="contracts",
        on_delete=models.PROTECT,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=(MinValueValidator(0),),
    )
    total_value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("start_date", "id")
        indexes = [
            models.Index(
                fields=("unit", "start_date", "end_date"),
                name="contract_unit_dates_idx",
            ),
            models.Index(
                fields=("start_date", "id"),
                name="contract_start_id_idx",
            ),
            models.Index(
                fields=("end_date",),
                name="contract_end_date_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="contract_end_on_or_after_start",
            ),
            models.CheckConstraint(
                condition=models.Q(monthly_rent__gte=0),
                name="contract_monthly_rent_nonnegative",
            ),
        ]

    @staticmethod
    def billable_months(start_date, end_date):
        month_difference = (
            (end_date.year - start_date.year) * 12
            + end_date.month
            - start_date.month
        )
        return max(1, month_difference + (end_date.day > start_date.day))

    def save(self, *args, **kwargs):
        months = self.billable_months(self.start_date, self.end_date)
        self.total_value = self.monthly_rent * months
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contract {self.pk} - unit {self.unit_id}"
