from odoo import models, fields, api, _

class ChickenVaccination(models.Model):
    _name = "chicken.vaccination"
    _description = "Handles vaccinations of the chicken"

    # Independent fields
    vaccination_ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    comment = fields.Char()
    vaccination_date = fields.Date(default=fields.Date.today)
    scheduled_date = fields.Date()
    quantity = fields.Float()
    status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], default='scheduled', string='Status')

    # Relational fields
    product_id = fields.Many2one('product.product', string='Vaccine')
    partner_id = fields.Many2one('res.partner', string='Responsible')
    batch_id = fields.Many2one('chicken.batch', string='Batch')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('vaccination_ref') or vals['vaccination_ref'] == _('New'):
                vals['vaccination_ref'] = self.env['ir.sequence'].next_by_code('vaccination.sequence') or _('New')
        return super().create(vals_list)

    @api.model
    def _cron_check_vaccination_schedule(self):
        """ Automated job to check upcoming vaccinations """
        today = fields.Date.today()
        vaccinations = self.search([('scheduled_date', '=', today), ('status', '=', 'scheduled')])
        for vac in vaccinations:
            # Notify responsible user or take automated action
            message = f"Reminder: Vaccination {vac.vaccination_ref} is scheduled today."
            vac.partner_id.message_post(body=message)

