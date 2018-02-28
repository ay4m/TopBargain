from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views, permissions
from rest_framework.response import Response
import json

from accounts.models import UserAccount
from accounts.serializers import AccountSerializer


class LoginView(views.APIView):
    def post(self, request):
        """
        This function is called when the HTTP request method is POST for the url /api/login/
        """
        data = json.loads(request.body)
        #loads json data from the request and converts to python dictionary

        username = data.get('username', None)
        password = data.get('password', None)

        print(username+' '+password)
        account = authenticate(username=username, password=password)
        print(account)
        """
        username and password are extracted from the json data and authenticated from the database
        if matched, an instance of UserAccount for the user is returned
        else HTTP_401_UNAUTHORIZED method is run
        """
        if account is not None:

            login(request, account)
            #if the given account is valid, then the user is logged in

            serialized = AccountSerializer(account)
            #converts UserAccount instance to JSON

            return Response({
                'loggedIn': "yes",
              },status=status.HTTP_202_ACCEPTED)
            #return Response(serialized.data)
            #returns JSON data
        
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(views.APIView):
    queryset = UserAccount.objects.all()
    def post(self, request):
        data = json.loads(request.body)
        #load JSON data from request and convert to python dict
        serialized = AccountSerializer(data=data)

        if serialized.is_valid():
            UserAccount.objects.create_user(**serialized.validated_data)
            return Response(serialized.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


        