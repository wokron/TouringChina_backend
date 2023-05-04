from django.shortcuts import render
from rest_framework.views import APIView

from utils.perm import permission_check


# Create your views here.
class TicketView(APIView):
    @permission_check(['Common User'], user=True)
    def get(self, request, user):
        pass

    @permission_check(['Common User'], user=True)
    def post(self, request, user):
        pass


class TicketIdView(APIView):
    @permission_check(['Common User'], user=True)
    def put(self, request, user):
        pass

    @permission_check(['Common User'], user=True)
    def patch(self, request, user):
        pass

    @permission_check(['Common User'], user=True)
    def delete(self, request, user):
        pass
