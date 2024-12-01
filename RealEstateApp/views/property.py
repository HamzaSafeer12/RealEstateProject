from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from RealEstateApp.models import Property
from RealEstateApp.serializer import PropertySerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache
from rest_framework import status
from django.db.models import Count
# libraries for Swagger and and requestbody :(hmy apny requestbody k multabik krny k liya)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi

class PropertyAPIView(APIView):    
    permission_classes = [IsAuthenticated]  # Ensure ke sirf authenticated user access kare
    def get(self, request):
        properties = Property.objects.filter(user=request.user)
        if not properties.exists():
            return Response({"detail": "No properties found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)
    
    parser_classes = [MultiPartParser, FormParser]  # Allow file uploads
    #requestbody ko add krna allow ni kr rha tha tbhee ya kiya
    @swagger_auto_schema(
        request_body=PropertySerializer(many=False, partial=True),
        security=[{'Bearer': []}]  # This will require the 'Bearer' token in the Authorization header
    )
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


class FilterProperty(APIView):
    def post(self, request):
        city = request.data.get('city', None)
        bedrooms = request.data.get('bedroom', None)
        price_range = request.data.get('price_range', None)
        product = request.data.get('product', None)
        area = request.data.get('area', None)
        location = request.data.get('location', None)

        # Cache key generate karte hain based on filters
        cache_key = f"filtered_properties:{city}:{bedrooms}:{price_range}:{product}:{area}:{location}"
        
        # Pehle cache se data lete hain
        response_data = cache.get(cache_key)
        if response_data:
            print("Cache hit")
        
        if response_data is None:  # Agar cache mein nahi hai
            print("Cache miss")
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
            if location:
                filters &= Q(location__icontains=location)

            # Group by location and count properties for each unique location
            filtered_properties = Property.objects.filter(filters).values(
                'location'
            ).annotate(
                count=Count('property_id')
            )

# # filtered_properties
# # filtered_properties ek queryset hai jo Django ORM se return hoti hai. Is queryset mein, har record ek dictionary ke format mein hota hai, jismein tumhare specified fields hote hain


# # #         values('location'):

# # Yeh line unique locations ki list banata hai. Tumhare case mein, isse DHA, Gulberg, aur Model Town milte hain.
# # annotate(count=Count('property_id')):

# # Yeh line check karti hai ke har unique location ke against database mein kitni properties hain.
# # Jab DHA aata hai, toh yeh database ko dekhata hai aur count karta hai ke DHA location ke liye kitni records hain.
# # Agar DHA ke liye 3 properties hain (jese pehle example mein tha), toh count column mein 3 aayega.

#         # Create a response list
            response_data = []
            for prop in filtered_properties:
                location_data = {
                    'location': prop['location'],  # Include the location name
                    'properties': list(Property.objects.filter(location=prop['location']).values(
                        'agency_name', 'agency_product', 'area', 'bathroom', 
                        'bedroom', 'category', 'city', 'contact_name', 'price'
                    )),
                    'count': prop['count']
                }
                response_data.append(location_data)

            # Cache the response data for 5 minutes
            cache.set(cache_key, response_data, timeout=300)

        return Response(response_data, status=status.HTTP_200_OK)