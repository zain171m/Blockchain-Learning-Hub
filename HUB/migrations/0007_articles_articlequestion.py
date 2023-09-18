# Generated by Django 4.2.2 on 2023-09-16 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HUB', '0006_alter_quizquestion_correct_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='HUB/files/photos/')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('option1', models.CharField(max_length=255)),
                ('option2', models.CharField(max_length=255)),
                ('option3', models.CharField(max_length=255)),
                ('option4', models.CharField(max_length=255)),
                ('correct_option', models.CharField(max_length=255)),
                ('research_paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HUB.researchpaper')),
            ],
        ),
    ]