# Generated by Django 4.2 on 2025-07-21 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eloq_app', '0002_interest_alter_podcast_related_goals_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscoverY',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='podcast',
            name='related_goals',
            field=models.ManyToManyField(related_name='podcasts', to='Eloq_app.interest'),
        ),
        migrations.AlterField(
            model_name='video',
            name='related_goals',
            field=models.ManyToManyField(related_name='videos', to='Eloq_app.interest'),
        ),
    ]
