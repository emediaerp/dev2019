# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo import tools, _


class Company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    book_specialized = fields.Boolean(string="Book Specialized", default=True)

