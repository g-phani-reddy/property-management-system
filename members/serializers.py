from rest_framework import serializers

from members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "full_name", "email", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_email(self, value):
        return value.strip().lower()
