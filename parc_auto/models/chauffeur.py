# -*- coding: utf-8 -*-

from odoo import models, fields, api

class chauffeur(models.Model):
    _name='parcauto.chauffeur'
    name=fields.Char(string="Nom",required=True)
    fname=fields.Char(string="Prénom",required=True)
    etat = fields.Selection([
        ('disponible', "Disponible"),
        ('mission', "En Mission"),
        ('indisponible', "Indisponible"),
    ], default='disponible',required=True)
    login=fields.Char(string="Login",required=True)