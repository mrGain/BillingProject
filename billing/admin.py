from django.contrib import admin
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_no', 'customer_name', 'date')
    search_fields = ('invoice_no', 'customer_name')

    def get_serializer_class(self, request, obj=None):
        return InvoiceSerializer

@admin.register(InvoiceDetail)
class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'description', 'quantity', 'unit_price', 'price')
    search_fields = ('invoice', 'description')

    def get_serializer_class(self, request, obj=None):
        return InvoiceDetailSerializer


