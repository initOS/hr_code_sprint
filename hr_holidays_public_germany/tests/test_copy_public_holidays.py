# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.hr_holidays_public_germany.tests.common import \
    TestPublicHolidays


class TestCopyPublicHolidays(TestPublicHolidays):

    def test_public_holiday_reset(self):
        self.public_holiday_reset.action_reset_holidays()

        hr_holiday_public = \
            self.HrHolidaysPublic.search([('year', '=', self.TestYear)])
        if not hr_holiday_public:
            hr_holiday_public = None

        self.assertIsNotNone(hr_holiday_public)

        if hr_holiday_public:
            line_ids = hr_holiday_public.line_ids
            if not line_ids:
                line_ids = None
            self.assertIsNotNone(line_ids)
