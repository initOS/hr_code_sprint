# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": 'HR Holidays Public Germany',
    "version": '11.0.1.0.0',
    "license": "AGPL-3",
    "category": "Human Resources",
    "author": "Yu Weng <yweng@elegosoft.com>, "
              "Nikolina Todorova <nikolina.todorova@initos.com>, "
              "Odoo Community Association (OCA)",
    "description": """

HR Holidays Public Germany
=================================================

Functions:

1. Notifies the human resource managers when somebody ask for a holiday.
2. Wizard to create/delete allocation and leaves for public holidays.
3. Improves onchange event to calculate public holidays

""",
    "website": "https://github.com/OCA/hr",
    "depends": [
        "l10n_de_country_states",
        "hr",
        "hr_holidays",
        "hr_holidays_public",
    ],
    "data": [
        "wizard/copy_public_holidays_view.xml",
        "data/hr_holidays_data.xml",
        "views/hr_public_holidays_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
