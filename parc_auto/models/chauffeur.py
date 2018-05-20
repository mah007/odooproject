# -*- coding: utf-8 -*-

from odoo import models, fields, api

class chauffeur(models.Model):
    _name='parcauto.chauffeur'
    name=fields.Char(string="Nom")
    etat = fields.Selection([
        ('disponible', "Disponible"),
        ('mission', "En Mission"),
        ('indisponible', "Indisponible"),
    ], default='disponible')