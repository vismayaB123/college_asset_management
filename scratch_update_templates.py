import os

templates = [
    'assets/templates/assets/asset_list.html', 
    'assets/templates/assets/allocation_list.html', 
    'assets/templates/assets/maintenance_list.html'
]

for filepath in templates:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Hide add buttons
    content = content.replace(
        '<a href="{% url \'assets:asset_add\' %}" class="btn btn-brand bg-brand text-white shadow-sm">',
        '{% if user.profile.role == \'SYSTEM_ADMIN\' %}<a href="{% url \'assets:asset_add\' %}" class="btn btn-brand bg-brand text-white shadow-sm">'
    )
    content = content.replace(
        '<a href="{% url \'assets:allocation_add\' %}" class="btn btn-brand bg-brand text-white shadow-sm">',
        '{% if user.profile.role == \'SYSTEM_ADMIN\' %}<a href="{% url \'assets:allocation_add\' %}" class="btn btn-brand bg-brand text-white shadow-sm">'
    )
    content = content.replace(
        '<a href="{% url \'assets:maintenance_add\' %}" class="btn btn-brand bg-brand text-white shadow-sm">',
        '{% if user.profile.role == \'SYSTEM_ADMIN\' %}<a href="{% url \'assets:maintenance_add\' %}" class="btn btn-brand bg-brand text-white shadow-sm">'
    )

    content = content.replace(
        '<i class="bi bi-plus-lg me-2"></i>Add Asset</a>',
        '<i class="bi bi-plus-lg me-2"></i>Add Asset</a>{% endif %}'
    )
    content = content.replace(
        '<i class="bi bi-plus-lg me-2"></i>Add Allocation</a>',
        '<i class="bi bi-plus-lg me-2"></i>Add Allocation</a>{% endif %}'
    )
    content = content.replace(
        '<i class="bi bi-plus-lg me-2"></i>Add Maintenance Record</a>',
        '<i class="bi bi-plus-lg me-2"></i>Add Maintenance Record</a>{% endif %}'
    )
    
    # Hide Actions table header
    content = content.replace(
        '<th class="text-end">Actions</th>',
        '{% if user.profile.role == \'SYSTEM_ADMIN\' %}<th class="text-end">Actions</th>{% endif %}'
    )
    
    # Hide Actions table data cell
    content = content.replace(
        '<td class="text-end">\n                                    <div class="dropdown">',
        '{% if user.profile.role == \'SYSTEM_ADMIN\' %}\n                                <td class="text-end">\n                                    <div class="dropdown">'
    )
    content = content.replace(
        '</ul>\n                                    </div>\n                                </td>',
        '</ul>\n                                    </div>\n                                </td>\n                                {% endif %}'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Templates updated.")
