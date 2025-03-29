from odoo import models, api, fields

class ChickenCull(models.Model):
    _name = 'chicken.cull'
    _description = 'this model covers removing chicken, and tracking culling reason,'

    # Fields
    cull_ref = fields.Char(default="New",
                           copy=False, readonly=True)
    cull_date = fields.Date(default=fields.datetime.today())
    cull_reason = fields.Selection([('death', 'Death'), ('weak', 'Weak'),
                                    ('low_production', 'Low Production')])
    cull_description = fields.Text()
    number = fields.Integer(required=True, default=0)

    # Relational fields
    batch_id = fields.Many2one('chicken.batch')

    # todo: Fields to implement later
    # transfer_id = fields.Char()


    # Add unique sequence number
    @api.model
    def create(self, records):
        records['cull_ref'] = self.env['ir.sequence'].next_by_code('cull.reference')
        return super(ChickenCull, self).create(records)


    ## === ToDo: Automatically create a transfer from Stock
    # @api.model
    # def create(self, vals):
    #     vals['cull_ref'] = self.env['ir.sequence'].next_by_code('cull.reference')
    #     record = super(ChickenCull, self).create(vals)
    #     # record.name = self.env['ir.sequence'].next_by_code('apex.jobcard')
    #     # picking_type_id = 5
    #     creator =  self.env.user.id
    #     # location_id = 8
    #     # location_dest_id = 16
    #     # source_doc = vals['name']
    #     if record.cull_reason == "death":
    #         transfer = self.env['stock.picking'].create({
    #             'partner_id': creator,
    #             'origin': record.cull_ref,
    #             'picking_type_id': 5,
    #             'location_id': 8,
    #             'location_dest_id' : 16,
    #             'note' : record.cull_ref,
    #             'move_ids': [(0, 0, {
    #             'name': 'Chicken' + record.cull_ref,
    #             'product_uom_qty': record.number,
    #             'product_id': 3,
    #             "product_uom": 1,
    #             "location_id": 8,
    #             "location_dest_id": 16,
    #         })]
    #         })
    #         # transfer['move_lines'] =
    #
    #     return record

## ==== TODO:Automaticcaly create a culling entry on PoS sale.
    #   class CreateCull(models.Model):
    #     _inherit = 'stock.picking'
    #     _description = 'this guy will create a cull entry everytime a POS transfer on chicken is made'
    #

    # @api.model
    # def create(self, vals_list):
    #     if vals_list['picking_type_id'] == 7:
    #         print(vals_list)
    #         # number_chicken = 0
    #         # chicken_not_present = False
    #         # for product in vals_list['move_ids_without_package']:
    #         #     if product[2]['product_id'] == 3:
    #         #         number_chicken += product[2]['product_uom_qty']
    #         #         chicken_not_present = True
    #         #
    #         # if chicken_not_present:
    #         #     self.env['chicken.cull'].create({
    #         #         'number': number_chicken,
    #         #         'cull_reason': 'weak'
    #         #     })
    #
    #
    #     return super(CreateCull, self).create(vals_list)

#   stage_obj = self.env['project.task.type']
#         stage_ids = stage_obj.search([('set_default', '=', True)])