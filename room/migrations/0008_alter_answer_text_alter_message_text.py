# Generated by Django 4.1.7 on 2023-03-18 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0007_alter_answer_room_alter_answer_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(max_length=300),
        ),
    ]