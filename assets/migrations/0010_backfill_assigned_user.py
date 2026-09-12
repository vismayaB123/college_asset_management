from django.db import migrations
from django.db.models import Q

def match_users_to_allocations(apps, schema_editor):
    Allocation = apps.get_model('assets', 'Allocation')
    User = apps.get_model('auth', 'User')

    allocations = Allocation.objects.all()
    matched_count = 0
    unmatched_count = 0
    ambiguous_count = 0

    for alloc in allocations:
        assigned_text = alloc.assigned_to.strip()
        if not assigned_text:
            continue
            
        # 1. Try exact username match
        try:
            user = User.objects.get(username__iexact=assigned_text)
            alloc.assigned_user = user
            alloc.save()
            matched_count += 1
            continue
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            ambiguous_count += 1
            continue

        # 2. Try exact full name match
        possible_users = []
        for u in User.objects.all():
            full_name = f"{u.first_name} {u.last_name}".strip()
            if full_name.lower() == assigned_text.lower():
                possible_users.append(u)
                
        if len(possible_users) == 1:
            alloc.assigned_user = possible_users[0]
            alloc.save()
            matched_count += 1
        elif len(possible_users) > 1:
            ambiguous_count += 1
        else:
            unmatched_count += 1

    print(f"\\nData Migration Report: Matched {matched_count}, Unmatched {unmatched_count}, Ambiguous {ambiguous_count}")


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_allocation_assigned_user_userrequest_userfeedback_and_more'),
    ]

    operations = [
        migrations.RunPython(match_users_to_allocations, migrations.RunPython.noop),
    ]
