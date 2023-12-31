from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail

class YourAppTests(APITestCase):
    def setUp(self):
        self.invoice_data = {
            "id": 1,
            "date": "2023-12-31",
            "invoice_no": "INV001",
            "customer_name": "Rakesh Gain"
        }
        self.invoice = Invoice.objects.create(**self.invoice_data)
        self.invoice_detail_data = {
            "id": 1,
            "description": "iphone 15pro",
            "quantity": 1,
            "unit_price": "120000.00",
            "price": "120000.00",
            "invoice": self.invoice.id
        },
        self.invoice_detail = InvoiceDetail.objects.create(**self.invoice_detail_data)

    def test_create_invoice(self):
        data = {"date": "2023-01-01", "invoice_no": "INV002", "customer_name": "Ram"}
        response = self.client.post("/api/invoices/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(Invoice.objects.last().invoice_no, "INV002")

    def test_retrieve_invoice(self):
        response = self.client.get(f"/api/invoices/{self.invoice.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_no'], self.invoice_data['invoice_no'])

    def test_update_invoice(self):
        updated_data = {"date": "2023-01-02", "customer_name": "Updated Name"}
        response = self.client.put(f"/api/invoices/{self.invoice.id}/", updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, "Updated Name")

    def test_delete_invoice(self):
        response = self.client.delete(f"/api/invoices/{self.invoice.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

    def test_create_invoice_detail(self):
        data = {"invoice": self.invoice.id, "description": "Item 2", "quantity": 3, "unit_price": 15.0, "price": 45.0}
        response = self.client.post("/api/invoice_details/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 2)
        self.assertEqual(InvoiceDetail.objects.last().description, "Item 2")

    def test_retrieve_invoice_detail(self):
        response = self.client.get(f"/api/invoice_details/{self.invoice_detail.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.invoice_detail_data['description'])

    def test_update_invoice_detail(self):
        updated_data = {"description": "Updated Item", "quantity": 2}
        response = self.client.put(f"/api/invoice_details/{self.invoice_detail.id}/", updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InvoiceDetail.objects.get(id=self.invoice_detail.id).description, "Updated Item")
        self.assertEqual(InvoiceDetail.objects.get(id=self.invoice_detail.id).quantity, 2)

    def test_delete_invoice_detail(self):
        response = self.client.delete(f"/api/invoice_details/{self.invoice_detail.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetail.objects.count(), 0)

