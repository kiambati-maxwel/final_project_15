from odoo import models, api, fields, _

class ChickenEggs(models.Model):
    _name = "chicken.eggs"
    _description = "Chicken eggs tracking"

    # Fields
    eggs_ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    quantity = fields.Integer()
    comment = fields.Text()
    date = fields.Date(default = fields.datetime.today())
    responsible = fields.Many2one('res.partner')  # Responsible

    # Relational fields
    batch_id = fields.Many2one('chicken.batch')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('eggs_ref') or vals['eggs_ref'] == _('New'):
                vals['eggs_ref'] = self.env['ir.sequence'].next_by_code('eggs.entries.sequence') or _('New')
        return super().create(vals_list)

