from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

UserModel = get_user_model()


class Tax(models.Model):
    income = models.FloatField(
        verbose_name='Income Amount',
        default=0
    )
    statue_choice = (
        ('NEW', 'NEW'),
        ('PAID', 'PAID'),
        ('DELAYED', 'DELAYED'),
    )
    status = models.CharField(
        choices=statue_choice,
        max_length=7,
        default='NEW',
        blank=False,
        null=False,
        verbose_name='Status Tax'
    )
    tax_amount = models.FloatField(
        verbose_name='Tax Amount',
        null=True,
        blank=True
    )
    tax_accountant = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        related_name='user_tax_accountant',
        null=True,
        blank=True
    )
    tax_payer = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        related_name='user_tax_payer',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deadline = models.DateTimeField(blank=True, null=True)

    fines = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True
    )

    total_amount = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True
    )

    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxs"
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return super(Tax, self).__str__()

    def tax_calculate(self):
        cgst = 0.08
        sgst = 0
        tax_rate = 0
        income = float(self.income)
        if self.tax_payer.indian_state == '':
            self.tax_amount = 0
            return None
        if self.tax_payer is not None:
            if not self.tax_payer.union_territories:
                sgst = 0.08
            else:
                sgst = 0

        if income < 250000:
            self.tax_amount = 0
            return None
        elif 250001 >= income and income <= 500000:
            cgst = 0.04
        elif 500001 >= income and income <= 1000000:
            cgst = 0.1
        elif income > 1000000:
            cgst = 0.12

        tax_rate = cgst+sgst
        self.tax_amount = income*tax_rate

    def payment(self):
        self.payment_date = timezone.now()
        self.payment = True
        self.status = 'PAID'
        self.save()

    def save(self, *args, **kwargs):
        self.tax_calculate()
        if self.deadline is not None and self.tax_amount >= 0:
            dt = self.deadline - timezone.now()
            if dt.days >= 0:
                self.fines = 0
            else:
                self.fines = self.tax_amount*0.01
        self.total_amount = self.tax_amount+self.fines
        super(Tax, self).save(*args, **kwargs)
