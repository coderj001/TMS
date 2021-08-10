from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime, timedelta

from tax.models import Tax


class TaxsManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.Tax = Tax
        self.client = APIClient()
        # create admin user
        self.admin = self.User.objects.create_superuser(
            email='admin_1@mail.com',
            username='admin_1',
            password='admin_1'
        )
        self.admin.save()
        # create tax-accountant user
        self.tax_accountant = self.User.objects.create_tax_accountant(
            email='tax_accountant_1@mail.com',
            username='tax_accountant_1',
            password='tax_accountant_1'
        )
        self.tax_accountant.save()
        # create tax-payer user
        self.tax_payer = self.User.objects.create_tax_payer(
            email='tax_payer_1@mail.com',
            username='tax_payer_1',
            password='tax_payer_1',
            state='Goa'
        )
        self.tax_payer.save()
        # admin token
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'admin_1@mail.com',
            'password': 'admin_1'
        })
        self.token_admin = response.json()['token']
        # tax-accountant token
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'tax_accountant_1@mail.com',
            'password': 'tax_accountant_1'
        })
        self.token_tax_accountant = response.json()['token']
        # tax-payer token
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'tax_payer_1@mail.com',
            'password': 'tax_payer_1'
        })
        self.token_tax_payer = response.json()['token']

    def test_create_tax(self):
        """
        test case for tax model
        """
        tax = self.Tax.objects.create(
            income=250001,
            status='NEW',
            tax_accountant=self.tax_accountant,
            tax_payer=self.tax_payer
        )
        tax.save()
        self.assertEqual(tax.income, 250001)
        self.assertEqual(tax.tax_accountant, self.tax_accountant)
        self.assertEqual(tax.tax_payer, self.tax_payer)
        self.assertEqual(tax.tax_amount, 30000.12)
        self.assertEqual(tax.total_amount, 30000.12)
        tax.deadline = datetime.now() - timedelta(days=1)
        tax.save()
        self.assertEqual(tax.total_amount, 30000.12)
        self.assertEqual(tax.fines, 0)

    def test_request_tax(self):
        """
        test case for request tax
        """
        # None type user
        res = self.client.post(reverse_lazy('tax:create_tax'), {
            'income': '60000',
            'deadline': '2021/11/10',
            'tax_payer': 'tax_payer_1',
            'tax_accountant': 'tax_accountant_1',
        })
        # can't request tax
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # admin type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.post(reverse_lazy('tax:create_tax'), {
            'income': '60000',
            'deadline': '2021/11/10',
            'tax_payer': 'tax_payer_1',
            'tax_accountant': 'tax_accountant_1',
        })
        # can't request tax
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # tax-payer type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_tax_payer}")
        res = self.client.post(reverse_lazy('tax:create_tax'), {
            'income': '60000',
            'deadline': '2021/11/10',
            'tax_payer': 'tax_payer_1',
            'tax_accountant': 'tax_accountant_1',
        })
        # can't request tax
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # tax-accountant type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_tax_accountant}")
        res = self.client.post(reverse_lazy('tax:create_tax'), {
            'income': '60000',
            'deadline': '2021/11/10',
            'tax_payer': 'tax_payer_1',
            'tax_accountant': 'tax_accountant_1',
        })
        # can request tax
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['income'], 60000)
        self.assertEqual(res.json()['deadline'], '2021-11-10T00:00:00+05:30')
        res = self.client.post(reverse_lazy('tax:create_tax'), {
            'income': '60000',
            'deadline': '2021/11/10',
            'tax_payer': 'tax_payer_1',
            'tax_accountant': 'tax_accountant_1',
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
