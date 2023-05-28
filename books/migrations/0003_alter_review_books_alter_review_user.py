# Generated by Django 4.2.1 on 2023-05-20 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='Books',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_book', to='books.book'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_user', to='books.userprofile'),
        ),
    ]