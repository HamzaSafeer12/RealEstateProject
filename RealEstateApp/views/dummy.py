from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from RealEstateApp.models import DummyModel
from RealEstateApp.serializer import DummyModelSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')  # Correctly apply csrf_exempt to the view
class DummyAPIView(APIView):
    def get(self, request):
        properties = DummyModel.objects.all()
        serializer = DummyModelSerializer(properties, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DummyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically associate the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
