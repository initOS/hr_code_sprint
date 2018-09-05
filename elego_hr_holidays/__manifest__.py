{
    'name': 'Elego Holidays',
    'version': '0.1',
    'description': """

Holidays module of Elegosoft-ERP
=================================================

Functions:

1. Notifies the human resource managers when somebody ask for a holiday.
2. Wizard to create/delete allocation and leaves for public holidays.
3. Improves onchange event to calculate public holidays

""",
    'category': 'Tools',
    'depends': [
        'l10n_de_country_states',
        'hr',
        'hr_holidays',
        'hr_holidays_public',
    ],
    'installable': True,
    'auto_install': False,
    'data': [
        'wizard/add_holidays_view.xml',
        'wizard/copy_public_holidays_view.xml',
        'data/leave_notifications.xml',
        'data/hr_holidays_data.xml',
        'views/hr_public_holidays_view.xml',
    ],
    'demo': [
    ],
}
