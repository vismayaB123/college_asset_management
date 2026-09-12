from django.db import migrations

def backfill_allocation_types(apps, schema_editor):
    Allocation = apps.get_model('assets', 'Allocation')
    for allocation in Allocation.objects.all():
        if allocation.expected_return_date is None:
            allocation.allocation_type = 'PERMANENT'
        else:
            # For backward compatibility, default to PARTIAL if there's a return date. 
            # Realistically, we can't fully know if it was full or partial initially, but PARTIAL is safer.
            # Actually, if quantity == asset.quantity, it's FULL. Let's check that.
            if allocation.quantity == allocation.asset.quantity:
                allocation.allocation_type = 'FULL'
            else:
                allocation.allocation_type = 'PARTIAL'
        allocation.save()

class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_allocation_allocation_type_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_allocation_types, reverse_code=migrations.RunPython.noop),
    ]
