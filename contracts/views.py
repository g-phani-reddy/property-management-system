from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, serializers

from contracts.models import Contract
from contracts.serializers import ContractSerializer


class ContractListCreateView(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.select_related("unit", "member")

    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get("active")
        if active is None:
            return queryset
        if active.lower() not in ("true", "false"):
            raise serializers.ValidationError(
                {"active": "Must be either 'true' or 'false'."}
            )

        today = timezone.localdate()
        active_filter = Q(start_date__lte=today, end_date__gte=today)
        if active.lower() == "true":
            return queryset.filter(active_filter)
        return queryset.exclude(active_filter)
