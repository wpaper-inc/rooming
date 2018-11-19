# Generated by Django 2.1.3 on 2018-11-18 15:06

from django.db import migrations, models
import django.db.models.deletion
import lib.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20181119_0006'),
        ('diagnoses', '0003_auto_20181118_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswerProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', lib.fields.AutoCreatedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('updated_at', lib.fields.AutoLastModifiedField(db_index=True, default=lib.fields.unix_timestamp, editable=False)),
                ('live', lib.fields.IndexedLiveField(default=True)),
                ('qap_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnoses.Answer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnoses.Question')),
            ],
            options={
                'verbose_name': 'QuestionAnswerProduct/質問回答商品関連',
                'verbose_name_plural': 'QuestionAnswerProducts/質問回答商品関連',
                'db_table': 'question_answer_product',
            },
        ),
        migrations.AlterModelOptions(
            name='questionanswer',
            options={'verbose_name': 'QuestionAnswer/質問回答関連', 'verbose_name_plural': 'QuestionAnswers/質問回答関連'},
        ),
        migrations.AddIndex(
            model_name='questionanswerproduct',
            index=models.Index(fields=['question', 'answer'], name='question_an_questio_50d119_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='questionanswerproduct',
            unique_together={('question', 'answer', 'live')},
        ),
    ]
