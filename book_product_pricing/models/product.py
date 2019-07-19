# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import models, fields, api, exceptions
from odoo import tools, _


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
    price_ids = fields.One2many(comodel_name="book.price.history", inverse_name="product_tmpl_id",
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
                  'ex_net_price', 'ex_markup_method', 'ex_markup')
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
        if 'list_price' in vals or 'standard_price' in vals or 'extended_price' in vals \
                or 'ex_currency_id' in vals or 'ex_list_price' in vals or 'ex_discount_percentage' in vals \
                or 'ex_net_price' in vals or 'ex_markup_method' in vals or 'ex_markup' in vals or 'ex_selling_margin' in vals:
            records_count = self.env['book.price.history'].search_count([
                ('list_price', '=', self.list_price),
                ('standard_price', '=', self.standard_price),
                ('extended_price', '=', self.extended_price),
                ('ex_currency_id', '=', self.ex_currency_id.id),
                ('ex_list_price', '=', self.ex_list_price),
                ('ex_discount_percentage', '=', self.ex_discount_percentage),
                ('ex_net_price', '=', self.ex_net_price),
                ('ex_markup_method', '=', self.ex_markup_method),
                ('ex_markup', '=', self.ex_markup),
                ('ex_selling_margin', '=', self.ex_selling_margin),
                ('user_id', '=', self.env.user.id),
                ('date_only', '=', datetime.today()),
                ('product_tmpl_id', '=', self.id)
            ])
            if records_count == 0:
                self.env['book.price.history'].create({
                    'list_price': res.list_price,
                    'standard_price': res.standard_price,
                    'extended_price': res.extended_price,
                    'ex_currency_id': res.ex_currency_id.id,
                    'ex_list_price': res.ex_list_price,
                    'ex_discount_percentage': res.ex_discount_percentage,
                    'ex_net_price': res.ex_net_price,
                    'ex_markup_method': res.ex_markup_method,
                    'ex_markup': res.ex_markup,
                    'ex_selling_margin': res.ex_selling_margin,
                    'date': datetime.now(),
                    'user_id': self.env.user.id,
                    'product_tmpl_id': res.id
                })
        return res

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'list_price' in vals or 'standard_price' in vals or 'extended_price' in vals \
                or 'ex_currency_id' in vals or 'ex_list_price' in vals or 'ex_discount_percentage' in vals \
                or 'ex_net_price' in vals or 'ex_markup_method' in vals or 'ex_markup' in vals or 'ex_selling_margin' in vals:
            records_count = self.env['book.price.history'].search_count([
                ('list_price', '=', self.list_price),
                ('standard_price', '=', self.standard_price),
                ('extended_price', '=', self.extended_price),
                ('ex_currency_id', '=', self.ex_currency_id.id),
                ('ex_list_price', '=', self.ex_list_price),
                ('ex_discount_percentage', '=', self.ex_discount_percentage),
                ('ex_net_price', '=', self.ex_net_price),
                ('ex_markup_method', '=', self.ex_markup_method),
                ('ex_markup', '=', self.ex_markup),
                ('ex_selling_margin', '=', self.ex_selling_margin),
                ('user_id', '=', self.env.user.id),
                ('date_only', '=', datetime.today()),
                ('product_tmpl_id', '=', self.id)
            ])
            print(records_count)
            if records_count == 0:
                self.env['book.price.history'].create({
                    'list_price': self.list_price,
                    'standard_price': self.standard_price,
                    'extended_price': self.extended_price,
                    'ex_currency_id': self.ex_currency_id.id,
                    'ex_list_price': self.ex_list_price,
                    'ex_discount_percentage': self.ex_discount_percentage,
                    'ex_net_price': self.ex_net_price,
                    'ex_markup_method': self.ex_markup_method,
                    'ex_markup': self.ex_markup,
                    'ex_selling_margin': self.ex_selling_margin,
                    'date': datetime.now(),
                    'date_only': datetime.today(),
                    'user_id': self.env.user.id,
                    'product_tmpl_id': self.id
                })
        return res
