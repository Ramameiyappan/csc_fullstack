from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from login.permission import IsOperator, IsManager, IsOperatorOrManager
from .serializer import ( ElectricitySerializer, RechargeSerializer, PanSerializer, TravelSerializer, 
                         InsuranceSerializer, OnlineSerializer, EsevaiSerializer, TopupSerializer, 
                         LedgerDashboardSerializer, LedgerDashboardManagerSerializer, UserDashboardSerializer)
from rest_framework.response import Response
from rest_framework import status 
from .models import Ledger
from login.models import User

class Electricity(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self,request):
        serializer = ElectricitySerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'successfully the work added'},
                status = status.HTTP_201_CREATED
            )
    
class Recharge(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self, request):
        serializer = RechargeSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'successfully the work added'},
                status = status.HTTP_201_CREATED
            )
    
class Pan(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self, request):
        serializer = PanSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'PAN service added successfully'},
                status = status.HTTP_201_CREATED
            )

class Travel(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self, request):
        serializer = TravelSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'successfully the work added'},
                status = status.HTTP_201_CREATED
            )

class Insurance(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self, request):
        serializer = InsuranceSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'successfully the work added'},
                status = status.HTTP_201_CREATED
            )
    
class Online(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self, request):
        serializer = OnlineSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'successfully the work added'},
                status = status.HTTP_201_CREATED
            )
    
class Esevai(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self, request):
        serializer = EsevaiSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'successfully the work added'},
                status = status.HTTP_201_CREATED
            )

class Topup(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrManager]

    def post(self, request):
        serializer = TopupSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                {'success':'successfully the work added'},
                status = status.HTTP_201_CREATED
            )
    
class LedgerDashboard(APIView):
    permission_classes=[IsAuthenticated, IsOperatorOrManager]

    def get(self,request):
        if request.user.role == 'operator':
            passbook = Ledger.objects.filter(operator=request.user)
            serializer = LedgerDashboardSerializer(instance=passbook, many=True)
        elif request.user.role == 'manager':
            passbook = Ledger.objects.all()
            serializer = LedgerDashboardManagerSerializer(instance=passbook, many=True)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )
    
class UserDashboard(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        userdetail = User.objects.all()
        serializer = UserDashboardSerializer(instance=userdetail, many=True)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )