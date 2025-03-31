# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _, exceptions
import re

class ChickenBatch(models.Model):
    _name = 'chicken.batch'
    _description = 'This the first model that is almost the base model of my tech driven chicken farm'

    # ====== Fields ===============
    name = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    hatch_date = fields.Date(required=True)
    house_number = fields.Integer()
    curled = fields.Integer(default=0, compute = '_compute_culled' , store=True)
    initial_stock = fields.Integer(default=0)
    laying_start_date = fields.Date()
    description = fields.Text()
    date_in = fields.Date()


    #====== Relational Fields ======
    cull_ids = fields.One2many('chicken.cull', 'batch_id')
    eggs_ids = fields.One2many('chicken.eggs', 'batch_id')
    feed_ids = fields.One2many('chicken.feed', 'batch_id')
    vaccination_ids = fields.One2many('chicken.vaccination', 'batch_id')

    # ToDo: fields to implement Later
    # transfer_ref_id = fields.Many2one('stock.picking')




    # ===== Computed Fields ==============
    stock = fields.Integer(compute='_compute_stock', store=True)
    age = fields.Integer(compute='_compute_age' , store=True)
    total_eggs = fields.Integer(compute = '_compute_total_eggs', default=0 , store=True)
    average_eggs_daily = fields.Integer(compute='_compute_average_eggs_daily', default=0 , store=True)
    total_feed = fields.Float(compute='_compute_total_feed' , store=True)
    average_feed_daily = fields.Float(compute='_compute_average_feed_daily' , store=True)
    # todo later
    # eggs_today = fields.Integer(compute='_compute_eggs_today', default=0)
    # feed_today=fields.Float()


    @api.depends('curled', 'initial_stock')
    def _compute_stock(self):
        for record in self:
            record.stock = record.initial_stock - record.curled

    @api.depends('cull_ids.number')
    def _compute_culled(self):
        for record in self:
            if len(record.cull_ids) > 0:
                record.curled = sum(record.mapped('cull_ids.number'))
            else:
                record.curled = 0


    @api.depends('hatch_date')
    def _compute_age(self):
        for record in self:
            if record.hatch_date:
                fmt = '%Y-%m-%d'
                start_date = fields.datetime.today().date()
                end_date = re.search('\d{4}-\d{2}-\d{2}', str(record.hatch_date))
                d2 = fields.datetime.strptime(end_date.group(), fmt).date()
                date_difference = start_date - d2
                record.age  =  int(date_difference.days)
            else:
                record.age = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('batch.sequence') or _('New')

                return super().create(vals_list)

    # ======================================== Eggs =====================================
    # @api.depends('eggs_ids.quantity', 'eggs_ids.date')
    # def _compute_eggs_today(self):
    #
    # # ==== ToDo: improve this banaa
    #     for record in self:
    #         if len(record.eggs_ids)>0:
    #             print(record.eggs_ids)
    #             print(record.mapped('eggs_ids.quantity'))
    #             print(record.mapped('eggs_ids.date'))
    #             counter = 0
    #             dates = record.mapped('eggs_ids.date')
    #             quantity = record.mapped('eggs_ids.quantity')
    #             for date in dates:
    #                 if date == fields.date.today():
    #                     counter += quantity[dates.index(date)]
    #                 record.eggs_today = counter
    #                 # break
    #         # record.eggs_today = 0

    @api.depends('eggs_ids.quantity')
    def _compute_total_eggs(self):
        for record in self:
            if len(record.eggs_ids) > 0:
                record.total_eggs = sum(record.mapped('eggs_ids.quantity'))
            else:
                record.total_eggs = 0


  # ========== todo Improve The following =========================================
    @api.depends('eggs_ids.quantity', 'laying_start_date')
    def _compute_average_eggs_daily(self):
        for record in self:
            if len(record.eggs_ids) > 0:
                if record.laying_start_date:
                    fmt = '%Y-%m-%d'
                    start_date = fields.datetime.today().date()
                    end_date = re.search('\d{4}-\d{2}-\d{2}', str(record.laying_start_date))
                    d2 = fields.datetime.strptime(end_date.group(), fmt).date()
                    date_difference = start_date - d2
                    if date_difference > datetime.timedelta(0):
                        record.average_eggs_daily = sum(record.mapped('eggs_ids.quantity')) / int(date_difference.days)
                    else:
                        record.average_eggs_daily = 0
                else:
                    exceptions.UserError('Please input start laying date')
                    record.average_eggs_daily = 0
            else:
                record.average_eggs_daily = 0

    @api.depends('feed_ids.quantity')
    def _compute_total_feed(self):
        for record in self:
            if len(record.feed_ids) > 0:
                record.total_feed = sum(record.mapped('feed_ids.quantity'))
            else:
                record.total_feed = 0

    @api.depends('feed_ids.quantity', 'date_in')
    def _compute_average_feed_daily(self):
        for record in self:
            if len(record.feed_ids) > 0:
                if record.date_in:
                    fmt = '%Y-%m-%d'
                    start_date = fields.datetime.today().date()
                    end_date = re.search('\d{4}-\d{2}-\d{2}', str(record.date_in))
                    d2 = fields.datetime.strptime(end_date.group(), fmt).date()
                    date_difference = start_date - d2
                    if date_difference > datetime.timedelta(0):
                        record.average_feed_daily = sum(record.mapped('feed_ids.quantity')) / int(date_difference.days)
                    else:
                        record.average_feed_daily = 0
                else:
                    exceptions.UserError('Please input Date in')
                    record.average_feed_daily = 0
            else:
                record.average_feed_daily = 0


class ChickenBatchReport(models.AbstractModel):
    _name = 'report.chicken.report_chicken_batch_template'
    _description = 'Chicken Batch Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['chicken.batch'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'chicken.batch',
            'docs': docs,
        }
