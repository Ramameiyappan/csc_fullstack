from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permission import IsAdmin
from rest_framework import status
from .models import User
from rest_framework.response import Response
from .serializer import RegisterSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

class Register(APIView): 
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success':'register successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error':serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class Login(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        name = request.data.get('username')
        pass_ = request.data.get('password')

        if not name or not pass_:
            return Response(
                {'error':'both username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            return Response(
                {'error': 'user not register yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not check_password(pass_, user.password):
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'role':user.role,
                'is_superuser': user.is_superuser
            },
            status=status.HTTP_200_OK
        )

class GoogleJWTLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("id_token")

        if not token:
            return Response(
                {"error": "ID token missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=10
            )

            email = idinfo.get("email")
            aud = idinfo.get("aud")

            if aud != settings.GOOGLE_CLIENT_ID:
                return Response(
                    {"error": "Token audience mismatch"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not email:
                return Response(
                    {"error": "Email not provided by Google"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print("GOOGLE TOKEN VERIFY ERROR:", str(e))

            return Response(
                {"error": "Invalid Google token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email}
        )

        if created:
            user.role = "operator"
            user.is_manager_approved = False
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "role": user.role
        })

class RequestManager(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role == 'manager':
            return Response(
                {'error': 'You are already a manager'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.manager_request:
            return Response(
                {'error': 'Manager request already sent'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.manager_request = True
        user.save()

        return Response(
            {'success': 'Manager request sent to admin'},
            status=status.HTTP_200_OK
        )

class PendingManagerRequests(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.filter(manager_request=True)

        data = []
        for u in users:
            data.append(
                {
                    'id': u.id,
                    'username': u.username
                }
            )
        return Response(data, status=status.HTTP_200_OK)

class ApproveManager(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.manager_request:
            return Response(
                {'error': 'No pending manager request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.role = 'manager'
        user.manager_request = False
        user.save()

        return Response(
            {'success': f'{user.username} approved as manager'},
            status=status.HTTP_200_OK
        )
    
class RejectManager(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.manager_request:
            return Response(
                {'error': 'No pending manager request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.manager_request = False
        user.save()

        return Response(
            {'success': f'{user.username} manager request rejected'},
            status=status.HTTP_200_OK
        )

class Refresh(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error':'refesh token is required'}
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response(
                {'access': str(refresh.access_token)}
            )
        except Exception:
            return Response(
                {'error': 'Invalid or expired refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"success": "Logged out successfully"},
            status=status.HTTP_205_RESET_CONTENT
        )