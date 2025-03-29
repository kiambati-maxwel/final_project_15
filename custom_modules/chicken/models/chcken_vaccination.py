from  odoo import models, fields, api, _

class ChickenVaccination(models.Model):
    _name = "chicken.vaccination"
    _description = "This guy handles vaccinations of the chicken"

    # Independent fields
    vaccination_ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    comment = fields.Char()
    vaccination_date = fields.Date(default=fields.datetime.today())
    quantity = fields.Float()

    # Relational fields
    product_id = fields.Many2one('product.product') # Vaccine
    partner_id = fields.Many2one('res.partner') # Responsible
    batch_id = fields.Many2one('chicken.batch')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('vaccination_ref') or vals['vaccination_ref'] == _('New'):
                vals['vaccination_ref'] = self.env['ir.sequence'].next_by_code('vaccination.sequence') or _('New')

                return super().create(vals_list)