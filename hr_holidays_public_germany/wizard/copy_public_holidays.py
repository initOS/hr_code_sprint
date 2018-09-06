# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class PublicHolidaysReset(models.TransientModel):
    _name = 'public.holiday.reset'
    year = fields.Integer('Year', required=True, default=(lambda self: datetime.today().year))
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State')
    @api.model
    def calculate_easter_sunday(self, year):
        d = (((255 - 11 * (year % 19)) - 21) % 30) + 21
        if d > 48:
            d += 1
        delta = d + 6 - ((year + (year - (year % 4)) / 4) + d + 1) % 7
        str_3_1 = '%s-03-01' % year
        date_3_1 = fields.Datetime.from_string(str_3_1)
        easter = date_3_1 + timedelta(days=delta)
        return easter

    @api.model
    def calculate_new_good_friday(self, easter):
        good_friday = easter - timedelta(days=2)
        return fields.Date.to_string(good_friday)

    @api.model
    def calculate_easter_monday(self, easter):
        easter_monday = easter + timedelta(days=1)
        return fields.Date.to_string(easter_monday)

    @api.model
    def calculate_ascension_day(self, easter):
        ascension_day = easter + timedelta(days=39)
        return fields.Date.to_string(ascension_day)

    @api.model
    def calculate_whit_monday(self, easter):
        whit_monday = easter + timedelta(days=50)
        return fields.Date.to_string(whit_monday)

    @api.model
    def calculate_corpus_christi(self, easter):
        corpus_christi = easter + timedelta(days=60)
        return fields.Date.to_string(corpus_christi)

    @api.model
    def calculate_floating_holidays(self, existing_holidays):
        public_holiday_line_obj = self.env['hr.holidays.public.line']
        easter = self.calculate_easter_sunday(self.year)

        public_holiday_line_obj.create({'name': _('Good Friday'),
                                        'date': self.calculate_new_good_friday(easter),
                                        'variable_date': True,
                                        'year_id': existing_holidays.id})
        public_holiday_line_obj.create({'name': _('Easter Sunday'),
                                        'date': fields.Date.to_string(easter),
                                        'variable_date': True,
                                        'year_id': existing_holidays.id})

        public_holiday_line_obj.create({'name': _('Easter Monday'),
                                        'date': self.calculate_easter_monday(easter),
                                        'variable_date': True,
                                        'year_id': existing_holidays.id})
        public_holiday_line_obj.create({'name': _('Ascension Day'),
                                        'date': self.calculate_ascension_day(easter),
                                        'variable_date': True,
                                        'year_id': existing_holidays.id})

        public_holiday_line_obj.create({'name': _('Whit Monday'),
                                        'date': self.calculate_whit_monday(easter),
                                        'variable_date': True,
                                        'year_id': existing_holidays.id})

    @api.model
    def calculate_state_floating_holidays(self, existing_holidays, state=None):
        if not state:
            return
        public_holiday_line_obj = self.env['hr.holidays.public.line']
        easter = self.calculate_easter_sunday(self.year)
        #Baden-Württemberg, Bavaria, Hesse, North Rhine-Westphalia, Rhineland-Palatinate, Saarland 
        if state.id in [self.ref('l10n_de_country_states.res_country_state_BW').id,
                        self.ref('l10n_de_country_states.res_country_state_BY').id,
                        self.ref('l10n_de_country_states.res_country_state_HE').id,
                        self.ref('l10n_de_country_states.res_country_state_NW').id,
                        self.ref('l10n_de_country_states.res_country_state_RP').id,
                        self.ref('l10n_de_country_states.res_country_state_SL').id]:
            public_holiday_line_obj.create({'name': _("Corpus Christi"),
                                            'date': self.calculate_corpus_christi(easter),
                                            'variable_date': True,
                                            'year_id': existing_holidays.id})

    @api.model
    def calculate_fixed_holidays(self, existing_holidays):
        public_holiday_line_obj = self.env['hr.holidays.public.line']

        public_holiday_line_obj.create({'name': _("New Years's Day"),
                                        'date': "%s-01-01" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        public_holiday_line_obj.create({'name': _("International Workers' Day"),
                                        'date': "%s-05-01" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        public_holiday_line_obj.create({'name': _("Day of German Unity"),
                                        'date': "%s-10-03" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        public_holiday_line_obj.create({'name': _("Christmas Day"),
                                        'date': "%s-12-25" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        public_holiday_line_obj.create({'name': _("Boxing Day"),
                                        'date': "%s-12-26" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})

    @api.model
    def calculate_state_fixed_holidays(self, existing_holidays, state=None):
        if not state:
            return
        public_holiday_line_obj = self.env['hr.holidays.public.line']
        #Baden-Württemberg, Bavaria, Saxony-Anhalt
        state_ids = [self.ref('l10n_de_country_states.res_country_state_BW').id,
                     self.ref('l10n_de_country_states.res_country_state_BY').id,
                     self.ref('l10n_de_country_states.res_country_state_ST').id]
        if state.id in state_ids:
            public_holiday_line_obj.create({'name': _("Three Kings Day"),
                                        'date': "%s-01-06" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        #Bavaria, Saarland
        state_ids = [self.ref('l10n_de_country_states.res_country_state_BY').id,
                     self.ref('l10n_de_country_states.res_country_state_SL').id]

        if state.id in state_ids:
            public_holiday_line_obj.create({'name': _("Assumption Day"),
                                        'date': "%s-08-15" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        #??
        state_ids = [self.ref('l10n_de_country_states.res_country_state_BW').id,
                     self.ref('l10n_de_country_states.res_country_state_BY').id,
                     self.ref('l10n_de_country_states.res_country_state_HE').id,
                     self.ref('l10n_de_country_states.res_country_state_NW').id,
                     self.ref('l10n_de_country_states.res_country_state_RP').id,
                     self.ref('l10n_de_country_states.res_country_state_SL').id]
        if state.id in state_ids:
            public_holiday_line_obj.create({'name': _("Day of Reformation"),
                                        'date': "%s-10-31" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        #Baden-Württemberg, Bavaria, North Rhine-Westphalia, Rhineland-Palatinate, Saarland
        state_ids = [self.ref('l10n_de_country_states.res_country_state_BW').id,
                        self.ref('l10n_de_country_states.res_country_state_BY').id,
                        self.ref('l10n_de_country_states.res_country_state_NW').id,
                        self.ref('l10n_de_country_states.res_country_state_RP').id,
                        self.ref('l10n_de_country_states.res_country_state_SL').id]
        if state.id in state_ids:
            public_holiday_line_obj.create({'name': _("All Saints’ Day"),
                                        'date': "%s-11-01" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})
        #Sachsen
        state_ids = [self.ref('l10n_de_country_states.res_country_state_SN').id]
        if state.id in state_ids:
            public_holiday_line_obj.create({'name': _("Repentance Day"),
                                        'date': "%s-11-23" % existing_holidays.year,
                                        'variable_date': False,
                                        'year_id': existing_holidays.id})

    @api.multi
    def action_delete_holidays(self, existing_holidays):
        self.ensure_one()
        if existing_holidays:
            for holiday_line in existing_holidays.line_ids:
                holiday_line.unlink()
        return existing_holidays

    @api.multi
    def action_reset_holidays(self):
        public_holiday_obj = self.env['hr.holidays.public']
        public_holiday_line_obj = self.env['hr.holidays.public.line']

        for wizard in self:
            existing_holidays = public_holiday_obj.search([('year', '=', self.year), ('country_id', '=', wizard.country_id.id)])
            if not (existing_holidays):
                existing_holidays = public_holiday_obj.create({'year': wizard.year})
            wizard.action_delete_holidays(existing_holidays)
            wizard.calculate_floating_holidays(existing_holidays)
            wizard.calculate_fixed_holidays(existing_holidays)
            wizard.calculate_floating_holidays(existing_holidays)
            wizard.calculate_fixed_holidays(existing_holidays)

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
                raise UserError(_('Warning'), _('You cannot copy the holidays to the same year.'))

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
                    if holiday.variable_date:
                        continue
                    holiday_date = datetime.strptime(holiday.date, '%Y-%m-%d')
                    new_holiday_date = "%s-%s-%s" % (wizard.year_to, holiday_date.month, holiday_date.day)
                    public_holiday_line_obj.create({'name': holiday.name,
                                                    'date': new_holiday_date,
                                                    'variable_date': False,
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
                                            'variable_date': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter
            public_holiday_line_obj.create({'name': _('Easter Sunday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable_date': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter + timedelta(days=1)
            public_holiday_line_obj.create({'name': _('Easter Monday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable_date': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter + timedelta(days=39)
            public_holiday_line_obj.create({'name': _('Ascension Day'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable_date': True,
                                            'year_id': new_holiday_year.id})
            new_holiday_date = easter + timedelta(days=50)
            public_holiday_line_obj.create({'name': _('Whit Monday'),
                                            'date': new_holiday_date.strftime("%Y-%m-%d"),
                                            'variable_date': True,
                                            'year_id': new_holiday_year.id})
        return {
            'type': 'ir.actions.act_window_close',
        }


PublicHolidayCopy()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
