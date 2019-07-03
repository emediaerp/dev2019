# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import models, fields, api, exceptions
from odoo import tools, _


class Product(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        print(vals)
        if 'standard_price' in vals:
            print('innnn')
            x = self.price_ids.create({
                'name': 'Cost Price',
                'old_value': self.standard_price,
                'new_value': vals['standard_price'],
                'date': datetime.today(),
                'user_id': self.env.user.id,
                'product_tmpl_id': self.product_tmpl_id.id,
                'product_id': self.id})
            print(x)
        res = super(Product, self).write(vals)
        return res


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    @api.multi
    @api.constrains('ex_discount_percentage')
    def _check_ex_discount_percentage(self):
        for record in self:
            if record.ex_discount_percentage < 0 and record.ex_discount_percentage > 100:
                raise exceptions.ValidationError('Extended discount percentage must be in between 0 and 100')

    @api.multi
    @api.depends('ex_list_price', 'ex_discount_percentage')
    def _compute_ex_net_price(self):
        print('inn')
        for record in self:
            record.ex_net_price = record.ex_list_price - (
                record.ex_list_price * (record.ex_discount_percentage / 100.0))

    @api.multi
    @api.depends('standard_price', 'list_price')
    def _compute_ex_selling_margin(self):
        for record in self:
            if record.list_price != 0:
                record.ex_selling_margin = (1 - (record.standard_price / record.list_price)) * 100

    book_pricing = fields.Boolean(string="Book Pricing", related='company_id.book_pricing', store=True)
    price_ids = fields.One2many(comodel_name="product.price.history", inverse_name="product_tmpl_id",
                                string="Price History")
    extended_price = fields.Boolean(string="Extended Price")
    ex_currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    ex_list_price = fields.Float(string="Purchase List Price")
    ex_discount_percentage = fields.Float(string="Discount(%)")
    ex_net_price = fields.Float(string="Purchase Net Price", compute=_compute_ex_net_price)
    ex_markup_method = fields.Selection(string="Markup Method", selection=[('list', 'List'), ('net', 'Net'), ],
                                        default='list', )
    ex_markup = fields.Float(string="Markup")
    ex_selling_margin = fields.Float(string="Selling Margin", compute=_compute_ex_selling_margin)

    @api.onchange('ex_currency_id', 'ex_list_price', 'ex_discount_percentage',
                  'ex_net_price', 'ex_markup_method','ex_markup')
    def _onchange_extended_fields(self):
        if self.ex_markup_method == 'list':
            self.list_price = self.ex_list_price * self.ex_markup
        elif self.ex_markup_method == 'net':
            self.list_price = self.ex_net_price * self.ex_markup
        self.standard_price = self.ex_currency_id._compute(self.ex_currency_id, self.company_id.currency_id,
                                                           self.ex_net_price)

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if 'list_price' in vals:
            self.price_ids.create({
                'name': 'Sale Price',
                'old_value': 0.0,
                'new_value': vals['list_price'],
                'date': datetime.today(),
                'user_id': self.env.user.id,
                'product_tmpl_id': res.id
            })
        return res

    @api.multi
    def write(self, vals):
        if 'standard_price' in vals:
            self.price_ids.create({
                'name': 'Cost Price',
                'old_value': self.standard_price,
                'new_value': vals['standard_price'],
                'date': datetime.today(),
                'user_id': self.env.user.id,
                'product_tmpl_id': self.id})
        if 'list_price' in vals:
            self.price_ids.create({
                'name': 'Sale Price',
                'old_value': self.list_price,
                'new_value': vals['list_price'],
                'date': datetime.today(),
                'user_id': self.env.user.id,
                'product_tmpl_id': self.id})
        res = super(ProductTemplate, self).write(vals)
        return res


class PricingHistory(models.Model):
    _name = 'product.price.history'
    _rec_name = 'name'
    _description = 'Book Pricing History'

    name = fields.Char(string="Description", required=True)
    old_value = fields.Float(string="Old Value")
    new_value = fields.Float(string="New Value")
    date = fields.Date(string="Date", required=False, )
    user_id = fields.Many2one(comodel_name="res.users", string="User")
    product_tmpl_id = fields.Many2one(comodel_name="product.template")
