import json
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.models import UserAccount
from accounts.serializers import AccountSerializer

class LoginView(views.APIView):
    def post(self, request):
        print(request.user)
        data = json.loads(request.body)
        print(data)
        return Response({
            'message': 'Account could not be created with received data.'
        }, status = status.HTTP_400_BAD_REQUEST)


class RegisterView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        data = json.loads(request.body)
        #load JSON data from request and convert to python dict
        serialized = AccountSerializer(data=data)
        print(request.data)

        if serialized.is_valid():
            UserAccount.objects.create_user(**serialized.validated_data)
            return Response({
                'isRegistered': 'yes',
                'message': 'Registration Successful.'
            })

        return Response({
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


        