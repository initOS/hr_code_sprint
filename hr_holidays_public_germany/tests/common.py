# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestPublicHolidays(common.TransactionCase):

    def setUp(self):
        super(TestPublicHolidays, self).setUp()

        # Usefull models
        self.PublicHolidayReset = self.env['public.holiday.reset']
        self.HrHolidaysPublicLine = self.env['hr.holidays.public.line']
        self.HrHolidaysPublic = self.env['hr.holidays.public']
        self.TestYear = "2018"
        self.CountryId = self.ref('base.de')

        # Test Create Public Holidays for 2018
        wizard_data = {
            "year": self.TestYear,
            "country_id": self.CountryId
        }

        self.public_holiday_reset = \
            self.PublicHolidayReset.create(wizard_data)
