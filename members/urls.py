from django.urls import path

from members.views import MemberListCreateView


urlpatterns = [
    path("members", MemberListCreateView.as_view(), name="member-list"),
]
