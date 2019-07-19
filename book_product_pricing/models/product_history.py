# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import models, fields, api, exceptions
from odoo import tools, _


class PricingHistory(models.Model):
    _name = 'book.price.history'
    _rec_name = 'product_tmpl_id'
    _description = 'Book Pricing History'

    date = fields.Datetime(string="Date", required=False)
    date_only = fields.Date(string="Date", required=False)
    user_id = fields.Many2one(comodel_name="res.users", string="User")
    product_tmpl_id = fields.Many2one(comodel_name="product.template", string="Product")
    barcode = fields.Char(related="product_tmpl_id.barcode", store=True, string="Product ISBN")

    # Base Price
    list_price = fields.Float(string="Sale Price")
    standard_price = fields.Float(string="Cost")
    # Extended  Pricing
    extended_price = fields.Boolean(string="Extended Price")
    ex_currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    ex_list_price = fields.Float(string="Purchase List Price")
    ex_discount_percentage = fields.Float(string="Discount(%)")
    ex_net_price = fields.Float(string="Purchase Net Price")
    ex_markup_method = fields.Selection(string="Markup Method", selection=[('list', 'List'), ('net', 'Net'), ],
                                        default='list')
    ex_markup = fields.Float(string="Markup")
    ex_selling_margin = fields.Float(string="Selling Margin")
