# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo import tools, _


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    publisher = fields.Boolean(string="Publisher")


class Level(models.Model):
    _name = 'book.product.level'
    _description = 'Book Level'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    _sql_constraints = [
        ('unique_level_name', 'UNIQUE(name)', _('Name must be unique! '))
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    parent_id = fields.Many2one(comodel_name="book.product.level", string="Parent", required=False, )
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise exceptions.ValidationError(_('You cannot create recursive categories.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]


class Series(models.Model):
    _name = 'book.product.series'
    _rec_name = 'name'
    _description = 'Book Series'
    _sql_constraints = [
        ('unique_series_name', 'UNIQUE(name)', _('Name must be unique! '))
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Type(models.Model):
    _name = 'book.product.type'
    _rec_name = 'name'
    _description = 'Book Type'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', _('Name must be unique! '))
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Contractor(models.Model):
    _name = 'book.product.contractor'
    _rec_name = 'name'
    _description = 'Book Contractor'
    _sql_constraints = [
        ('unique_contractor_name', 'UNIQUE(name)', _('Name must be unique! '))
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Distributor(models.Model):
    _name = 'book.product.distributor'
    _rec_name = 'name'
    _description = 'Book Distributor'
    _sql_constraints = [
        ('unique_distributor_name', 'UNIQUE(name)', _('Name must be unique! '))
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Subject(models.Model):
    _name = 'book.product.subject'
    _description = 'Book Subject'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    _sql_constraints = [
        ('unique_subject_name', 'UNIQUE(name)', _('Name must be unique! '))
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    parent_id = fields.Many2one(comodel_name="book.product.subject", string="Parent", required=False, )
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise exceptions.ValidationError(_('You cannot create recursive categories.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]


class Author(models.Model):
    _name = 'book.product.author'
    _rec_name = 'name'
    _description = 'Book Author'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class Language(models.Model):
    _name = 'book.product.language'
    _rec_name = 'name'
    _description = 'Book Language'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
