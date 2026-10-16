from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers

from properties.models import Property, Unit
from properties.serializers import PropertySerializer, UnitSerializer


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.prefetch_related("units")
    serializer_class = PropertySerializer


class PropertyDetailView(generics.RetrieveUpdateAPIView):
    queryset = Property.objects.prefetch_related("units")
    serializer_class = PropertySerializer
    lookup_url_kwarg = "property_id"


class PropertyUnitListCreateView(generics.ListCreateAPIView):
    serializer_class = UnitSerializer

    def get_property(self):
        return get_object_or_404(Property, pk=self.kwargs["property_id"])

    def get_queryset(self):
        return Unit.objects.filter(property_id=self.kwargs["property_id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["property"] = self.get_property()
        return context


class UnitListView(generics.ListAPIView):
    serializer_class = UnitSerializer
    queryset = Unit.objects.select_related("property")

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get("status")
        if status is not None:
            valid_statuses = Unit.Status.values
            if status not in valid_statuses:
                raise serializers.ValidationError(
                    {"status": f"Must be one of: {', '.join(valid_statuses)}."}
                )
            queryset = queryset.filter(status=status)
        return queryset


class UnitDetailView(generics.RetrieveUpdateAPIView):
    queryset = Unit.objects.select_related("property")
    serializer_class = UnitSerializer
    lookup_url_kwarg = "unit_id"
