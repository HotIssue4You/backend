# Generated by Django 4.2.11 on 2024-04-18 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_article_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='noun_title',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.TextField(),
        ),
    ]
