# Generated by Django 4.2.2 on 2023-09-15 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HUB', '0005_alter_quizquestion_correct_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='correct_option',
            field=models.CharField(max_length=255),
        ),
    ]
