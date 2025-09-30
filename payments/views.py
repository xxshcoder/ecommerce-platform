from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db import transaction
from django.utils import timezone
import requests
import hashlib
import hmac
import base64

from orders.models import Order
from .models import Payment

@login_required
def initiate_esewa_payment(request, order_number):
    """Auto-submit eSewa sandbox payment with correct total_amount and signature"""

    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    payment, created = Payment.objects.get_or_create(
        order=order,
        user=request.user,
        defaults={
            'payment_method': 'esewa',
            'amount': order.total_amount,
            'currency': 'NPR',
        }
    )

    # Breakdown amounts
    tax_amount = round(float(order.tax_amount), 2)
    delivery_charge = round(float(order.shipping_cost), 2)
    service_charge = 0.0
    amount = round(float(order.total_amount) - tax_amount - delivery_charge - service_charge, 2)
    total_amount = round(amount + tax_amount + service_charge + delivery_charge, 2)

    signed_fields = "total_amount,transaction_uuid,product_code"
    params = {
        'amount': amount,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'transaction_uuid': order.order_number,
        'product_code': settings.ESEWA_MERCHANT_ID,
        'product_service_charge': service_charge,
        'product_delivery_charge': delivery_charge,
        'success_url': request.build_absolute_uri(settings.ESEWA_SUCCESS_URL),
        'failure_url': request.build_absolute_uri(settings.ESEWA_FAILURE_URL),
        'signed_field_names': signed_fields,
    }

    # Generate signature
    message = ','.join(f"{k}={params[k]}" for k in signed_fields.split(','))
    signature = hmac.new(
        settings.ESEWA_SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    params['signature'] = base64.b64encode(signature).decode()

    context = {
        'order': order,
        'payment': payment,
        'esewa_payment_url': settings.ESEWA_PAYMENT_URL,  # sandbox
        **params
    }

    return render(request, 'payments/esewa_payment.html', context)


@login_required
def esewa_payment_success(request):
    """Handle eSewa payment success callback (V2)"""
    transaction_uuid = request.GET.get("transaction_uuid")
    reference_id = request.GET.get("referenceId")

    if not all([transaction_uuid, reference_id]):
        messages.error(request, "Invalid payment response from eSewa.")
        return redirect("products:product_list")

    order = get_object_or_404(Order, order_number=transaction_uuid, user=request.user)

    # Verify payment with eSewa V2 endpoint
    verification_url = settings.ESEWA_VERIFICATION_URL  # sandbox
    payload = {
        "product_code": settings.ESEWA_MERCHANT_ID,
        "total_amount": float(order.total_amount),
        "transaction_uuid": transaction_uuid,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(verification_url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        status = data.get("status", "").lower()

        with transaction.atomic():
            payment = Payment.objects.get(order=order)
            if status in ["success", "complete"]:
                payment.status = "succeeded"
                payment.esewa_reference_id = reference_id
                payment.paid_at = timezone.now()
                payment.save()

                order.payment_status = "completed"
                order.status = "processing"
                order.save()

                messages.success(request, f"Payment successful! Order {order.order_number} is processing.")
                return render(request, "payments/payment_success.html", {"order": order})
            else:
                payment.status = "failed"
                payment.failure_reason = f"Verification failed: {data}"
                payment.save()

                order.payment_status = "failed"
                order.status = "cancelled"
                order.save()

                messages.error(request, "Payment verification failed.")
                return redirect("orders:order_detail", order_number=order.order_number)

    messages.error(request, "Error contacting eSewa for verification.")
    return redirect("products:product_list")


@login_required
def esewa_payment_failure(request):
    """Handle eSewa payment failure callback"""
    transaction_uuid = request.GET.get("transaction_uuid")
    if transaction_uuid:
        try:
            order = get_object_or_404(Order, order_number=transaction_uuid, user=request.user)
            payment = Payment.objects.get(order=order)
            payment.status = "failed"
            payment.failure_reason = "Payment cancelled by user or failed"
            payment.save()

            order.payment_status = "failed"
            order.status = "cancelled"
            order.save()

            # Restore stock
            for item in order.items.all():
                if item.product.track_quantity:
                    item.product.quantity += item.quantity
                    item.product.save()

            messages.warning(request, "Payment was cancelled or failed. You can try again.")
            return redirect("orders:order_detail", order_number=order.order_number)
        except Exception as e:
            messages.error(request, f"Error processing payment failure: {str(e)}")

    messages.error(request, "Payment failed.")
    return redirect("products:product_list")


@login_required
def payment_method_selection(request, order_number):
    """Payment method selection page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if order.payment_status == "completed":
        messages.info(request, "This order has already been paid.")
        return redirect("orders:order_detail", order_number=order.order_number)

    context = {"order": order}
    return render(request, "payments/payment_method.html", context)


@login_required
def cash_on_delivery(request, order_number):
    """Handle Cash on Delivery payment"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if request.method == "POST":
        with transaction.atomic():
            payment, created = Payment.objects.get_or_create(
                order=order,
                user=request.user,
                defaults={
                    "payment_method": "cod",
                    "amount": order.total_amount,
                    "currency": "NPR",
                    "status": "pending",
                }
            )

            order.payment_status = "pending"
            order.status = "processing"
            order.save()

        messages.success(request, f"Order {order.order_number} placed successfully with Cash on Delivery!")
        return redirect("orders:order_detail", order_number=order.order_number)

    return render(request, "payments/cod_confirm.html", {"order": order})
