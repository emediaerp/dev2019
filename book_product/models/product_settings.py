# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo import tools, _


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    publisher = fields.Boolean(string="Publisher")


class Series(models.Model):
    _name = 'book.product.series'
    _rec_name = 'name'
    _description = 'Book Series'
    _sql_constraints = [
        ('unique_series_name', 'UNIQUE(name)', 'Name must be unique! ')
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Type(models.Model):
    _name = 'book.product.type'
    _rec_name = 'name'
    _description = 'Book Type'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Name must be unique! ')
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Contractor(models.Model):
    _name = 'book.product.contractor'
    _rec_name = 'name'
    _description = 'Book Contractor'
    _sql_constraints = [
        ('unique_contractor_name', 'UNIQUE(name)', 'Name must be unique! ')
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Distributor(models.Model):
    _name = 'book.product.distributor'
    _rec_name = 'name'
    _description = 'Book Distributor'
    _sql_constraints = [
        ('unique_distributor_name', 'UNIQUE(name)', 'Name must be unique! ')
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Subject(models.Model):
    _name = 'book.product.subject'
    _rec_name = 'name'
    _description = 'Book Distributor'
    _sql_constraints = [
        ('unique_subject_name', 'UNIQUE(name)', 'Name must be unique! ')
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    parent_id = fields.Many2one(comodel_name="book.product.subject", string="Parent", required=False, )


class Author(models.Model):
    _name = 'book.product.author'
    _rec_name = 'name'
    _description = 'Book Author'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
