from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient


# Test for tax-payer user
class UsersManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.client = APIClient()
        # create admin user
        self.admin = self.User.objects.create_superuser(
            email='admin_1@mail.com',
            username='admin_1',
            password='admin_1'
        )
        self.admin.save()
        # create tax-accountant user
        self.taxaccountant = self.User.objects.create_tax_accountant(
            email='tax_accountant_1@mail.com',
            username='tax_accountant_1',
            password='tax_accountant_1'
        )
        self.taxaccountant.save()
        # create tax-payer user
        self.taxpayer = self.User.objects.create_tax_payer(
            email='tax_payer_1@mail.com',
            username='tax_payer_1',
            password='tax_payer_1'
        )
        self.taxpayer.save()
        # getting token for admin
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'admin_1@mail.com',
            'password': 'admin_1'
        })
        self.token_admin = response.json()['token']
        # getting token for tax-accountant
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'tax_accountant_1@mail.com',
            'password': 'tax_accountant_1'
        })
        self.token_taxaccountant = response.json()['token']
        # getting token for tax-payer
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'tax_payer_1@mail.com',
            'password': 'tax_payer_1'
        })
        self.token_taxpayer = response.json()['token']

    def test_create_user(self):
        """
        test case for model manager - create_user
        """
        user = self.User.objects.create_user(
            email='normal@user.com',
            username='normal',
            password='foo'
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.username, 'normal')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNotNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='', username='', password="foo")

    def test_create_superuser(self):
        """
        test case for model manager - create_superuser
        """
        admin_user = self.User.objects.create_superuser(
            email='super@user.com',
            username='super',
            password='foo'
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'super')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNotNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com',
                username='super',
                password='foo',
                is_superuser=False
            )

    def test_registerTaxAccountant(self):
        """
        test case for register for tax-accountant
        """
        res = self.client.post(reverse_lazy('user:tax_accountant_register'), {
            'username': 'tax_accountant_3',
            'email': 'tax_accountant_3@mail.com',
            'password': 'tax_accountant_3',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['user_type'], 'tax-accountant')
        self.assertEqual(self.User.taxaccountantmanager.count(), 2)

    def test_registerTaxPayer(self):
        """
        test case for register for tax-payer
        """
        res = self.client.post(reverse_lazy('user:tax_payer_register'), {
            'username': 'tax_payer_3',
            'email': 'tax_payer_3@mail.com',
            'password': 'tax_payer_3',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['user_type'], 'tax-payer')
        self.assertEqual(self.User.taxpayermanager.count(), 2)

    def test_get_user_list(self):
        """
        test case for get list of user
        """
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # admin type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 2)

        # tax-accountant type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_taxaccountant}")
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

        # tax-payer type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_taxpayer}")
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_view(self):
        """
        test case for user
        """
        admin_id = self.admin.id
        taxaccountant_id = self.taxaccountant.id
        taxpayer_id = self.taxpayer.id
        # none type of user get unauthrized
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # admin type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)  # get admin view
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': taxaccountant_id}))
        # get tax-accountant view
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': taxpayer_id}))
        # get tax-payer view
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # tax-accountant type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_taxaccountant}")
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        # get admin view - unauthrized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': taxaccountant_id}))
        # get tax-accountant view
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': taxpayer_id}))
        # get tax-payer view
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # tax-payer type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_taxpayer}")
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        # get admin view - unauthrized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': taxaccountant_id}))
        # get tax-accountant view - unauthrized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': taxpayer_id}))
        # get tax-payer view
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user_edit(self):
        """
        test case for user edit view
        """
        admin_id = self.admin.id
        taxaccountant_id = self.taxaccountant.id
        taxpayer_id = self.taxpayer.id

        # tax-payer type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_taxpayer}")
        res = self.client.put(reverse_lazy(
            'user:user_edit', kwargs={'id': taxpayer_id}),
            {
                'first_name': 'taxpayer_edit_first_name',
                'last_name': 'taxpayer_edit_last_name'
        })
        self.assertEqual(
            res.status_code, status.HTTP_403_FORBIDDEN)  # can't edit

        # admin type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        # can edit tax-payer
        res = self.client.put(reverse_lazy(
            'user:user_edit', kwargs={'id': taxpayer_id}),
            {
                'first_name': 'admin_edit_first_name',
                'last_name': 'admin_edit_last_name'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['first_name'], 'admin_edit_first_name')
        self.assertEqual(res.json()['last_name'], 'admin_edit_last_name')
        # can edit tax-accountant
        res = self.client.put(reverse_lazy(
            'user:user_edit', kwargs={'id': taxaccountant_id}),
            {
                'first_name': 'admin_edit_first_name',
                'last_name': 'admin_edit_last_name'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['first_name'], 'admin_edit_first_name')
        self.assertEqual(res.json()['last_name'], 'admin_edit_last_name')

        # tax-accountant type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_taxaccountant}")
        # can edit tax-accountant
        res = self.client.put(reverse_lazy(
            'user:user_edit', kwargs={'id': taxaccountant_id}),
            {
                'first_name': 'taxaccountant_edit_first_name',
                'last_name': 'taxaccountant_edit_last_name'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['first_name'],
                         'taxaccountant_edit_first_name')
        self.assertEqual(res.json()['last_name'],
                         'taxaccountant_edit_last_name')
        # can edit tax-payer
        res = self.client.put(reverse_lazy(
            'user:user_edit', kwargs={'id': taxpayer_id}),
            {
                'first_name': 'taxaccountant_edit_first_name',
                'last_name': 'taxaccountant_edit_last_name'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['first_name'],
                         'taxaccountant_edit_first_name')
        self.assertEqual(res.json()['last_name'],
                         'taxaccountant_edit_last_name')
        # can't edit admin
        res = self.client.put(reverse_lazy(
            'user:user_edit', kwargs={'id': admin_id}),
            {
                'first_name': 'taxaccountant_edit_first_name',
                'last_name': 'taxaccountant_edit_last_name'
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
