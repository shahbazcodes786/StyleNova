from django.contrib import admin
from .models import Order, Payment, OrderProduct, PaymentMethod
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at')
    list_filter = ('status', 'is_ordered')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_per_page = 20
    inlines = (OrderProductInline, )
    
    
    

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id',
        'user',
        'status',
    )

    def save_model(self, request, obj, form, change):

        old_status = None

        if change:
            old_payment = Payment.objects.get(pk=obj.pk)
            old_status = old_payment.status

        super().save_model(request, obj, form, change)

        if old_status != "Verified" and obj.status == "Verified":

            order = Order.objects.get(payment=obj)

            subject = "Payment Verified - StyleNova"

            message = render_to_string(
                "orders/payment_verified_email.html",
                {
                    "user": obj.user,
                    "order": order,
                }
            )

            email = EmailMessage(
                subject,
                message,
                to=[obj.user.email],
            )

            email.content_subtype = "html"
            email.send()
                    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(PaymentMethod)
