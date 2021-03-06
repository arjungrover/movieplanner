from django.shortcuts import render
from rest_framework import viewsets, status, permissions

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView

from user.models import UserInfo, Token
from user.serializers import SignUpSerializer, LoginSerializer

class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = SignUpSerializer
    queryset = UserInfo.objects.all()

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get_or_create(user=user)[0]
        is_admin = UserInfo.objects.get(id=token.user_id).is_admin
        return Response(
            {
                'token': token.key,
                'is_admin':is_admin
            }
        )

class EmailVerify(APIView):
    """
    Used to verify user Email
    """
    def get(self, request, pk=None):
        token = request.GET.get('token')
        try:
            user = UserInfo.objects.get(email_token=token)
            if(user.is_verified == True):
                return Response({'message': 'User already verified'}, status=status.HTTP_200_OK)
        except:
            response = {
                'error': 'Invalid Key!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if not token:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        return Response({'message': 'Verified Success'}, status=status.HTTP_200_OK)

class GetUserView(RetrieveAPIView):
    """
    Provides the user details of a user from its token
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = SignUpSerializer(user)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
        