# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestPublicHolidays(common.TransactionCase):

    def setUp(self):
        super(PublicHolidaysReset, self).setUp()

        # Usefull models
        self.PublicHolidayReset = self.env['public.holiday.reset']
        self.HrHolidaysPublicLine = self.env['hr.holidays.public.line']
        self.HrHolidaysPublic = self.env['hr.holidays.public']
        self.TestYear = "2018"

        # Test Create Public Holidays for 2018
        wizard_data = {
            "year": self.TestYear
        }

        self.public_holiday_reset = \
            self.PublicHolidayReset.create(wizard_data)
