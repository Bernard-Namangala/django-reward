# Generated by Django 2.2.8 on 2020-02-19 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='post',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='your_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_text',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
