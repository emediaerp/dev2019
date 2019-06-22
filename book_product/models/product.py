# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo import tools, _


class Product(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    @api.multi
    @api.constrains('royalty_percentage')
    def _check_royalty_percentage(self):
        for record in self:
            if record.royalty_percentage < 0 and record.royalty_percentage > 100:
                raise exceptions.ValidationError('Royalty percentage must be in between 0 and 100')

    # Basic Information
    book_specialized = fields.Boolean(string="Book Specialized", related='company_id.book_specialized', store=True)
    publisher_id = fields.Many2one(comodel_name="res.partner", string="Publisher", required=False, )
    series_id = fields.Many2one(comodel_name="book.product.series", string="Series", required=False, )
    type_id = fields.Many2one(comodel_name="book.product.type", string="Type", required=False, )
    exclusive = fields.Boolean(string="Exclusive")
    # Royalty
    royalty = fields.Boolean(string="Royalty")
    contractor_id = fields.Many2one(comodel_name="book.product.contractor", string="Contractor", required=False, )
    distributor_id = fields.Many2one(comodel_name="book.product.distributor", string="Distributor", required=False, )
    royalty_percentage = fields.Float(string="Royalty Percentage")
    # Extended Information
    teacher_resources = fields.Boolean(string="Teacher Resources")
    subject_id = fields.Many2one(comodel_name="book.product.subject", string="Subject", required=False, )
    author_id = fields.Many2one(comodel_name="book.product.author", string="Subject", required=False, )
    language_id = fields.Many2one(comodel_name="res.lang", string="Language", required=False, )
    country_ids = fields.Many2many(comodel_name="res.country", string="Geographic Target", )
    # Flags
    moe_list = fields.Boolean(string="Title is in MOE List")
    out_of_print = fields.Boolean(string="Out of Print")
    termination = fields.Boolean(string="Termination")
    clear_stock = fields.Boolean(string="Clear Stock")
