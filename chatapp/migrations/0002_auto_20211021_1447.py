# Generated by Django 3.2.8 on 2021-10-21 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated_at']},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='created_by',
            new_name='speaker',
        ),
    ]
