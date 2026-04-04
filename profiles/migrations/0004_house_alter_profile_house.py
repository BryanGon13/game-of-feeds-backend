import django.db.models.deletion
from django.db import migrations, models


def migrate_house_data(apps, schema_editor):
    """
    For each profile that has a non-blank string in the old 'house' CharField,
    create (or get) a House record and assign it to the new 'house_fk' field.
    Blank or null values are left as NULL on the new FK field.
    """
    Profile = apps.get_model('profiles', 'Profile')
    House = apps.get_model('profiles', 'House')

    for profile in Profile.objects.exclude(house='').exclude(house__isnull=True):
        house_obj, _ = House.objects.get_or_create(name=profile.house)
        profile.house_fk = house_obj
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_profile_image'),
    ]

    operations = [
        # 1. Create the House model.
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),

        # 2. Add a brand-new nullable FK column next to the old CharField.
        #    A new column has no existing data, so no FK constraint issues.
        migrations.AddField(
            model_name='profile',
            name='house_fk',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='members',
                to='profiles.house',
            ),
        ),

        # 3. Migrate existing string values into House records and link profiles.
        migrations.RunPython(migrate_house_data, reverse_code=migrations.RunPython.noop),

        # 4. Drop the old CharField — no FK constraint, safe on SQLite.
        migrations.RemoveField(
            model_name='profile',
            name='house',
        ),

        # 5. Rename the new FK column to 'house'.
        migrations.RenameField(
            model_name='profile',
            old_name='house_fk',
            new_name='house',
        ),
    ]
