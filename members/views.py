from rest_framework import generics

from members.models import Member
from members.serializers import MemberSerializer


class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
