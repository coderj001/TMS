# Generated by Django 3.2.6 on 2021-08-09 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tax', '0003_auto_20210809_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTax',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('income', models.FloatField(default=0, verbose_name='Income Amount')),
                ('status', models.CharField(choices=[('NEW', 'NEW'), ('PAID', 'PAID'), ('DELAYED', 'DELAYED')], default='NEW', max_length=7, verbose_name='Status Tax')),
                ('tax_amount', models.FloatField(blank=True, null=True, verbose_name='Tax Amount')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('fines', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_amount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tax_accountant', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tax_payer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Tax',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]