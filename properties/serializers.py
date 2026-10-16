from rest_framework import serializers

from properties.models import Property, Unit


class UnitSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Unit
        fields = ("id", "property", "unit_number", "monthly_rent", "status")
        read_only_fields = ("id", "status")

    def create(self, validated_data):
        return Unit.objects.create(
            property=self.context["property"],
            **validated_data,
        )


class PropertySerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ("id", "name", "address", "units", "created_at")
        read_only_fields = ("id", "created_at")
