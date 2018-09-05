# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
from datetime import datetime, timedelta


class PublicHolidaysReset(models.TransientModel):
    _name = 'public.holiday.reset'
    year = fields.Integer('Year', required=True, default=(lambda self: datetime.today().year))

    @api.multi
    def action_reset_holidays(self):
        public_holiday_obj = self.env['hr.holidays.public']
        public_holiday_line_obj = self.env['hr.holidays.public.line']

        for wizard in self:
            # unlink all currently existing holiday lines before deleting the year
            existing_holidays = public_holiday_obj.search([('year', '=', wizard.year)])
            if existing_holidays:
                for holiday_line in existing_holidays.line_ids:
                    holiday_line.unlink()

            # create floating holiday in new year by firstly calculating Easter sunday
            d = (((255 - 11 * (wizard.year % 19)) - 21) % 30) + 21
            if d > 48:
                d += 1
            delta = d + 6 - ((wizard.year + (wizard.year - (wizard.year % 4)) / 4) + d + 1) % 7
            str_3_1 = '%s-03-01' % wizard.year
            date_3_1 = datetime.strptime(str_3_1, '%Y-%m-%d')
            easter = date_3_1 + timedelta(days=delta)

            # create holiday lines for floating and fixed holidays
            new_holiday_date = easter - timedelta(days=2)
            public_holiday_line_obj.create({'name': _('Good Friday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': existing_holidays.id})
            new_holiday_date = easter
            public_holiday_line_obj.create({'name': _('Easter Sunday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': existing_holidays.id})
            new_holiday_date = easter + timedelta(days=1)
            public_holiday_line_obj.create({'name': _('Easter Monday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': existing_holidays.id})
            new_holiday_date = easter + timedelta(days=39)
            public_holiday_line_obj.create({'name': _('Ascension Day'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': existing_holidays.id})
            new_holiday_date = easter + timedelta(days=50)
            public_holiday_line_obj.create({'name': _('Whit Monday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': existing_holidays.id})
            #celebrated on the second Thursday after Whitsun.
#            public_holiday_line_obj.create({'name': _("Corpus Christi"),
#                                            'date': "%s-xx-xx" % wizard.year,
#                                            'variable': True,
#                                            'year_id': existing_holidays.id})


            public_holiday_line_obj.create({'name': _("New Years's Day"),
                                            'date': "%s-01-01" % wizard.year,
                                            'variable': False,
                                            'year_id': existing_holidays.id})
            public_holiday_line_obj.create({'name': _("International Workers' Day"),
                                            'date': "%s-05-01" % wizard.year,
                                            'variable': False,
                                            'year_id': existing_holidays.id})
            public_holiday_line_obj.create({'name': _("Day of German Unity"),
                                            'date': "%s-10-03" % wizard.year,
                                            'variable': False,
                                            'year_id': existing_holidays.id})
            public_holiday_line_obj.create({'name': _("Christmas Day"),
                                            'date': "%s-12-25" % wizard.year,
                                            'variable': False,
                                            'year_id': existing_holidays.id})
            public_holiday_line_obj.create({'name': _("Boxing Day"),
                                            'date': "%s-12-26" % wizard.year,
                                            'variable': False,
                                            'year_id': existing_holidays.id})

#            public_holiday_line_obj.create({'name': _("Three Kings Day"),
#                                            'date': "%s-01-06" % wizard.year,
#                                            'variable': False,
#                                            'year_id': existing_holidays.id})
#            public_holiday_line_obj.create({'name': _("Labour Day"),
#                                            'date': "%s-05-01" % wizard.year,
#                                            'variable': False,
#                                            'year_id': existing_holidays.id})
#            public_holiday_line_obj.create({'name': _("Assumption Day"),
#                                            'date': "%s-08-15" % wizard.year,
#                                            'variable': False,
#                                            'year_id': existing_holidays.id})
#            public_holiday_line_obj.create({'name': _("Day of Reformation"),
#                                            'date': "%s-10-31" % wizard.year,
#                                            'variable': False,
#                                            'year_id': existing_holidays.id})
#            public_holiday_line_obj.create({'name': _("All Saints’ Day"),
#                                            'date': "%s-11-01" % wizard.year,
#                                            'variable': False,
#                                            'year_id': existing_holidays.id})
#            public_holiday_line_obj.create({'name': _("Repentance Day"),
#                                            'date': "%s-11-23" % wizard.year,
#                                            'variable': False,
#                                            'year_id': existing_holidays.id})
        return {
            'type': 'ir.actions.act_window_close',
        }


PublicHolidaysReset()


class PublicHolidayCopy(models.TransientModel):
    _name = 'public.holiday.copy'

    year_from = fields.Integer('From', required=True, default=(lambda self: datetime.today().year))
    year_to = fields.Integer('To', required=True, default=(lambda self: datetime.today().year + 1))

    @api.multi
    def action_copy_holidays(self):
        public_holiday_obj = self.env['hr.holidays.public']
        public_holiday_line_obj = self.env['hr.holidays.public.line']

        for wizard in self:
            if wizard.year_to == wizard.year_from:
                raise exceptions.Warning(_('Warning'), _('You cannot copy the holidays to the same year.'))

            # unlink all currently existing holiday lines in target year (year_to)
            # before deleting target year
            existing_holidays_year_to = public_holiday_obj.search([('year', '=', wizard.year_to)])
            if existing_holidays_year_to:
                for holiday_line in existing_holidays_year_to.line_ids:
                    holiday_line.unlink()
                existing_holidays_year_to.unlink()

            # create new year for holidays
            new_holiday_year = public_holiday_obj.create({'year': wizard.year_to})

            # copy fixed holidays from source year (year_from) replacing the year (year_to)
            existing_holidays_year_from = public_holiday_obj.search([('year', '=', wizard.year_from)])
            if existing_holidays_year_from:
                for holiday in existing_holidays_year_from[0].line_ids:
                    if holiday.variable:
                        continue
                    holiday_date = datetime.strptime(holiday.date, '%Y-%m-%d')
                    new_holiday_date = "%s-%s-%s" % (wizard.year_to, holiday_date.month, holiday_date.day)
                    public_holiday_line_obj.create({'name': holiday.name,
                                                    'date': new_holiday_date,
                                                    'variable': False,
                                                    'year_id': new_holiday_year.id})

            # create floating holiday in new year by firstly calculating Easter sunday
            d = (((255 - 11 * (wizard.year_to % 19)) - 21) % 30) + 21
            if d > 48:
                d += 1
            delta = d + 6 - ((wizard.year_to + (wizard.year_to - (wizard.year_to % 4)) / 4) + d + 1) % 7
            str_3_1 = '%s-03-01' % wizard.year_to
            date_3_1 = datetime.strptime(str_3_1, '%Y-%m-%d')
            easter = date_3_1 + timedelta(days=delta)

            new_holiday_date = easter - timedelta(days=2)
            public_holiday_line_obj.create({'name': _('Good Friday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter
            public_holiday_line_obj.create({'name': _('Easter Sunday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter + timedelta(days=1)
            public_holiday_line_obj.create({'name': _('Easter Monday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter + timedelta(days=39)
            public_holiday_line_obj.create({'name': _('Ascension Day'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter + timedelta(days=50)
            public_holiday_line_obj.create({'name': _('Whit Monday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable': True,
                                            'year_id': new_holiday_year.id})
        return {
            'type': 'ir.actions.act_window_close',
        }


PublicHolidayCopy()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
