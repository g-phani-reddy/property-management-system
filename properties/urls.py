from django.urls import path

from properties.views import (
    PropertyDetailView,
    PropertyListCreateView,
    PropertyUnitListCreateView,
    UnitDetailView,
    UnitListView,
)


urlpatterns = [
    path("properties", PropertyListCreateView.as_view(), name="property-list"),
    path(
        "properties/<uuid:property_id>",
        PropertyDetailView.as_view(),
        name="property-detail",
    ),
    path(
        "properties/<uuid:property_id>/units",
        PropertyUnitListCreateView.as_view(),
        name="property-unit-list",
    ),
    path("units", UnitListView.as_view(), name="unit-list"),
    path(
        "units/<uuid:unit_id>",
        UnitDetailView.as_view(),
        name="unit-detail",
    ),
]
