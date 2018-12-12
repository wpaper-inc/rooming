# Generated by Django 2.1.3 on 2018-12-10 07:49

from django.db import migrations, models
import django.db.models.deletion
import lib.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20181210_1628'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', lib.fields.AutoCreatedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('updated_at', lib.fields.AutoLastModifiedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('live', lib.fields.IndexedLiveField(default=True)),
                ('tracking_url_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('url', models.URLField(max_length=1024, unique=True)),
                ('click_count', models.IntegerField(default=0)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
            options={
                'verbose_name': 'TrackingURL/短縮URL',
                'verbose_name_plural': 'TrackingURLs/短縮URL',
                'db_table': 'tracking_url',
            },
        ),
        migrations.AddIndex(
            model_name='trackingurl',
            index=models.Index(fields=['tracking_url_id'], name='tracking_ur_trackin_712c42_idx'),
        ),
        migrations.AddIndex(
            model_name='trackingurl',
            index=models.Index(fields=['account'], name='tracking_ur_account_a2df97_idx'),
        ),
        migrations.AddIndex(
            model_name='trackingurl',
            index=models.Index(fields=['user'], name='tracking_ur_user_id_d6032b_idx'),
        ),
    ]