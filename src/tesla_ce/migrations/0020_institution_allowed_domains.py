# Generated by Django 3.2.4 on 2021-10-09 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesla_ce', '0019_auto_20210907_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='allowed_domains',
            field=models.TextField(blank=True, default=None, help_text='Allowed domains for redirection', null=True),
        ),
    ]