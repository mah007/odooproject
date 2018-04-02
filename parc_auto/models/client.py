# -*- coding: utf-8 -*-

from odoo import models, fields, api


class client(models.Model):
    _name='parcauto.client'
    name = fields.Char(string="client")
    client_id=fields.Char('Client N°' , required=True)
    nom=fields.Char(required=True)
    adresse_cli=fields.Char(required=True)
    ville_cli=fields.Char(required=True)
    pays_cli=fields.Char(required=True)
    demande_ids = fields.One2many(
        'parcauto.demande', 'demande_id', string="Demandes")

    @api.model
    def create(self, vals):
        dem = self.env['ir.sequence'].next_by_code('client.sequence') or '/'
        vals['client_id'] = dem
        return super(client, self).create(vals)