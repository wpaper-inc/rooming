# Generated by Django 2.1.3 on 2018-11-08 07:21

import accounts.managers
from django.db import migrations, models
import django.db.models.deletion
import functools
import lib.cipher
import lib.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', lib.fields.AutoCreatedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('updated_at', lib.fields.AutoLastModifiedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('live', lib.fields.IndexedLiveField(default=True)),
                ('member_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=50)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Member/企業メンバー',
                'verbose_name_plural': 'Members/企業メンバー',
                'db_table': 'member',
            },
            managers=[
                ('objects', accounts.managers.MemberManager()),
                ('all_objects', accounts.managers.MemberManager(include_soft_deleted=True)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', lib.fields.AutoCreatedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('updated_at', lib.fields.AutoLastModifiedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('live', lib.fields.IndexedLiveField(default=True)),
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('public_key', models.CharField(default=functools.partial(lib.cipher.generate_secret, *('pb',), **{}), editable=False, max_length=35, unique=True)),
                ('secret_key', models.CharField(default=functools.partial(lib.cipher.generate_secret, *('sk',), **{}), editable=False, max_length=35, unique=True)),
            ],
            options={
                'verbose_name': 'Account/契約企業',
                'verbose_name_plural': 'Accounts/契約企業',
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', lib.fields.AutoCreatedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('updated_at', lib.fields.AutoLastModifiedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('live', lib.fields.IndexedLiveField(default=True)),
                ('store_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
            options={
                'verbose_name': 'Store/店舗',
                'verbose_name_plural': 'Stores/店舗',
                'db_table': 'store',
            },
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['account_id'], name='account_account_5fedc7_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['name'], name='account_name_a89769_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['public_key'], name='account_public__8a9463_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['secret_key'], name='account_secret__a90a56_idx'),
        ),
        migrations.AddField(
            model_name='member',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='member',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='member',
            name='store',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Store'),
        ),
        migrations.AddField(
            model_name='member',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['store_id'], name='store_store_i_0e0eac_idx'),
        ),
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['account'], name='store_account_be11d2_idx'),
        ),
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['name'], name='store_name_42037f_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['member_id'], name='member_member__fc7e2e_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['account'], name='member_account_036de7_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['store'], name='member_store_i_666532_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['email'], name='member_email_70e8ce_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['is_active'], name='member_is_acti_1d4be6_idx'),
        ),
    ]
