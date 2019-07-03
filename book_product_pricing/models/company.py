# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo import tools, _


class Company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    book_pricing = fields.Boolean(string="Book pricing", default=True)

