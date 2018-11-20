# Generated by Django 2.1.2 on 2018-11-15 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_requestmatch_skillful'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='p1_request',
        ),
        migrations.RemoveField(
            model_name='match',
            name='p2_request',
        ),
        migrations.AddField(
            model_name='requestmatch',
            name='match',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='match.Match'),
        ),
    ]