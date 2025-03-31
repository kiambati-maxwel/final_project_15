from odoo import models, fields, _, api


class ChickenFeeding(models.Model):
    _name = "chicken.feed"
    _description = 'this guy handles chicken feeding'

    # ====== Independent fields ====
    feeding_ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    feed_type = fields.Selection([
        ('starter_mash', 'Starter Mash (0-4 weeks)'),
        ('grower_mash', 'Grower Mash (5-10 weeks)'),
        ('pre_layer_mash', 'Pre-Layer Mash (11-16 weeks)'),
        ('layer_mash', 'Layer Mash (17+ weeks)')
    ], string="Feed Type", required=True)
    comment = fields.Text()



    # ========= Relational fields =======
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(required=True)
    batch_id = fields.Many2one('chicken.batch')
    date = fields.Date(default=fields.datetime.today())

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('feeding_ref') or vals['feeding_ref'] == _('New'):
                vals['feeding_ref'] = self.env['ir.sequence'].next_by_code('feeding.sequence') or _('New')
        return super().create(vals_list)

    ## === ToDo: Automatically create a transfer from Stock
    @api.model
    def create(self, vals):
        record = super(ChickenFeeding, self).create(vals)
        record['feeding_ref'] = self.env['ir.sequence'].next_by_code('feeding.sequence')
        creator =  self.env.user.id
        product_uom = self.env['product.product'].search([('id', '=', str(record.product_id.id))]).uom_id.id

        self.env['stock.picking'].create({
            'partner_id': creator,
            'origin': record.feeding_ref,
            'picking_type_id': 5,
            'location_id': 8,
            'location_dest_id' : 44,
            'note' : record.feeding_ref,
            'move_lines': [(0, 0, {
            'name': 'Chicken' + record.feeding_ref,
            'product_uom_qty': record.quantity,
            'description_picking': record.feeding_ref,
            'product_id': record.product_id.id,
            "product_uom": product_uom,
            "location_id": 8,
            "location_dest_id": 44,
        })]
        })

        return record

    @api.onchange('quantity')
    def _onchange_garden(self):
        record = self.env['stock.move'].search([('description_picking', '=', self.feeding_ref)])

        if record:
            record = self.env['stock.move'].search([('description_picking', '=', self.feeding_ref)], limit=1)
            record.write({
                'product_uom_qty': self.quantity,
            })
        else:
            print('I do not exist you')

