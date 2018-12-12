# Generated by Django 2.1.3 on 2018-12-10 06:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import lib.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', lib.fields.AutoCreatedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('updated_at', lib.fields.AutoLastModifiedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('live', lib.fields.IndexedLiveField(default=True)),
                ('activity_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('path', models.CharField(max_length=1024)),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(max_length=1024)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
            options={
                'verbose_name': 'Activity/ユーザーアクセスログ',
                'verbose_name_plural': 'Activities/ユーザーアクセスログ',
                'db_table': 'activity',
            },
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['user'], name='activity_user_id_39ee66_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['path'], name='activity_path_925c74_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['user', 'path'], name='activity_user_id_e85e44_idx'),
        ),
    ]