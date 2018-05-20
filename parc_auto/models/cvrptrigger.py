# -*- coding: utf-8 -*-

from odoo import models, fields, api


class cvrptrigger(models.Model):
    _name='parcauto.cvrptrigger'

    agence_id = fields.Many2one(
        'parcauto.agence', ondelete='set null', string="Agence",index=True)

