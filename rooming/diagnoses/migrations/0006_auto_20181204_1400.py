# Generated by Django 2.1.3 on 2018-12-04 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnoses', '0005_auto_20181119_2320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diagnosis',
            options={'verbose_name': 'Diagnosis/診断', 'verbose_name_plural': 'Diagnoses/診断'},
        ),
        migrations.AddField(
            model_name='question',
            name='message_type',
            field=models.IntegerField(choices=[(0, 'button'), (1, 'carousel'), (2, 'quick_reply')], default=0),
        ),
    ]
