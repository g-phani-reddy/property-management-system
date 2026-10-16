from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from contracts.models import Contract
from properties.models import Unit


@transaction.atomic
def create_contract(*, unit, member, start_date, end_date, monthly_rent=None):
    locked_unit = Unit.objects.select_for_update().get(pk=unit.pk)
    has_overlap = Contract.objects.filter(
        unit=locked_unit,
        start_date__lte=end_date,
        end_date__gte=start_date,
    ).exists()
    if has_overlap:
        raise serializers.ValidationError(
            {"unit": "This unit already has a contract for overlapping dates."}
        )

    contract = Contract.objects.create(
        unit=locked_unit,
        member=member,
        start_date=start_date,
        end_date=end_date,
        monthly_rent=(
            locked_unit.monthly_rent if monthly_rent is None else monthly_rent
        ),
    )
    sync_unit_status(locked_unit)
    return contract


def sync_unit_status(unit):
    today = timezone.localdate()
    is_occupied = Contract.objects.filter(
        unit=unit,
        start_date__lte=today,
        end_date__gte=today,
    ).exists()
    new_status = (
        Unit.Status.OCCUPIED if is_occupied else Unit.Status.AVAILABLE
    )
    if unit.status != new_status:
        Unit.objects.filter(pk=unit.pk).update(status=new_status)
        unit.status = new_status
