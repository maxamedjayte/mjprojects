# Generated by Django 3.2.7 on 2021-09-25 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('darulxadith_system', '0010_alter_natiijada_buundada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ardada',
            name='sanadDugsiyedka',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='darulxadith_system.sanaddugsiyeedka'),
        ),
    ]
