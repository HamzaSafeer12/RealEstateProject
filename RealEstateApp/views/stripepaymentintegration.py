from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from RealEstateApp.models import Property
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from RealEstateApp.models.paymentdetail_model import PaymentDetail
from RealEstateApp.models import Property
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

class CreateCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # JWT token se user ID lo
            user_id = request.user.id
            property_id = request.data.get("property_id")
            if not property_id:
                return Response({"error": "Property ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            property_obj = get_object_or_404(Property, property_id=property_id)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Card payment allow kar rahe hain
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': property_obj.agency_name,
                            },
                            'unit_amount': int(property_obj.price),  # Price in cents
                        },
                        'quantity': 1,  # Default quantity
                    },
                ],
                mode='payment',
                success_url='http://127.0.0.1:8000/success',
                cancel_url='http://127.0.0.1:8000/cancel',
                metadata={
                    'user_id': user_id,
                    'property_id': property_id,
                },
                billing_address_collection='required',
            )

            # Frontend ko session URL bhejo
            return Response({
                "checkout_url": checkout_session.url
            }, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback.print_exc()  # Full traceback dekhne ke liye
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret, tolerance=600
        )
    except ValueError as e:
        print("Payload issue:", str(e))
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Signature issue:", str(e))
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    except Exception as e:
        print("Unknown error:", str(e))
        return JsonResponse({'error': 'Unknown error'}, status=500)
    # Handle checkout session completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')  # User ID from metadata
        property_id = metadata.get('property_id')  # Property ID from metadata
        charge_id = session.get('payment_intent')  # Payment Intent ID
        amount_total = session.get('amount_total')  # Amount in cents (not dollars)
        # Save payment details in the database
        try:
            user = User.objects.get(id=user_id)
            property_obj = Property.objects.get(property_id=property_id)

            print("Saving payment details...")

            PaymentDetail.objects.create(
                user=user,
                property=property_obj,
                amount=amount_total,  # Convert cents to dollars
                charge_id=charge_id,
            )
            print("Payment details saved successfully.")
        except Exception as e:
            print(f"Error saving payment details: {e}")
            return JsonResponse({'error': 'Failed to save payment details'}, status=500)

    return JsonResponse({'status': 'success'}, status=200)


