from rest_framework import serializers

from contracts.models import Contract
from contracts.services import create_contract
from members.models import Member
from properties.models import Unit


class ContractSerializer(serializers.ModelSerializer):
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    monthly_rent = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        required=False,
    )
    total_value = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Contract
        fields = (
            "id",
            "unit",
            "member",
            "start_date",
            "end_date",
            "monthly_rent",
            "total_value",
            "created_at",
        )
        read_only_fields = ("id", "total_value", "created_at")

    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError(
                {"end_date": "End date must be on or after start date."}
            )
        return attrs

    def create(self, validated_data):
        return create_contract(**validated_data)
