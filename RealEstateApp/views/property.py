from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from RealEstateApp.models import Property
from RealEstateApp.serializer import PropertySerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

class PropertyAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure ke sirf authenticated user access kare
    
    def get(self, request):
        properties = Property.objects.filter(user=request.user)
        if not properties.exists():
            return Response({"detail": "No properties found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically associate the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProperty(APIView):

    def get(self, request, pk):
        property_data = get_object_or_404(Property, pk=pk)
        serializer = PropertySerializer(property_data)
        return Response(serializer.data)
    
    def put(self, request, pk):
        property_instance = Property.objects.get(pk=pk)

        # Agar primary_image field request mein hai
        if 'primary_image' in request.data:
            # Agar request mein bheji gayi image ka URL purane image ke URL se match karta hai
            if request.data['primary_image'] == str(property_instance.primary_image.url):
                # Agar URL same hai, image update nahi karni
                request.data.pop('primary_image')  # Image ko request se hata do taake update na ho
            else:
                # Agar nayi image bheji gayi hai (file ke tor par), to update karo
                if 'primary_image' in request.FILES:
                    property_instance.primary_image = request.FILES['primary_image']
                else:
                    return Response({"error": "Invalid image data or image file missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ab baqi fields ko update karna (partial=True use kar rahe hain)
        serializer = PropertySerializer(property_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        property_data = Property.objects.get(pk=pk)
        property_data.delete()
        return Response({"message": "Property deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



    # def put(self, request, pk):
    #     property_data = Property.objects.get(pk=pk)
    #     serializer = PropertySerializer(property_data, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilterProperty(APIView):
    def post(self, request):
        city = request.data.get('city', None)
        bedrooms = request.data.get('bedroom', None)
        price_range = request.data.get('price_range', None)
        product = request.data.get('product', None)
        area = request.data.get('area', None)

        filters = Q()

        if city:
            filters &= Q(city=city)
        if bedrooms:
            filters &= Q(bedroom__in=bedrooms)
        if price_range:
            filters &= Q(price__gte=price_range[0], price__lte=price_range[1])
        if product:
            filters &= Q(product=product)
        if area:
            filters &= Q(area__in=area)

        filtered_properties = Property.objects.filter(filters)
        print(f"filtered_properties: {filtered_properties}")
        serializer = PropertySerializer(filtered_properties, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

