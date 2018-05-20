# -*- coding: utf-8 -*-

from odoo import models, fields, api


class client(models.Model):
    _name='parcauto.client'

    name = fields.Char(required=True , string="Nom")
    prenom = fields.Char(required=True , string="Prénom")
    client_id=fields.Char(invisible="1")
    adresse_cli=fields.Char(required=True ,string="Adresse")

    demande_ids = fields.One2many('parcauto.demande', 'demande_id', string="Demandes")


    @api.model
    def create(self, vals):
        dem = self.env['ir.sequence'].next_by_code('client.sequence') or '/'
        vals['client_id'] = dem
        return super(client, self).create(vals)