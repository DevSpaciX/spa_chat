# Generated by Django 4.1.7 on 2023-03-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0003_message_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="image",
            field=models.FileField(blank=True, null=True, upload_to="messages/"),
        ),
    ]
