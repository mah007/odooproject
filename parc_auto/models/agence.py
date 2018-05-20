# -*- coding: utf-8 -*-

from odoo import models, fields, api


class agence(models.Model):
    _name='parcauto.agence'

    name=fields.Char(required=True)
    nombre_vehicule = fields.Integer(compute='_count_vehicules')
    descriprion = fields.Char(required=True)
    longtitude = fields.Char()
    laltitude = fields.Char()
    adresse = fields.Char(required=True)
    ville = fields.Char(required=True)


    vehicule_ids = fields.One2many(
        'parcauto.vehicule', 'agence_id', string="Vehicules")


    @api.one
    def _count_vehicules(self):
        self.nombre_vehicule = len(self.vehicule_ids)