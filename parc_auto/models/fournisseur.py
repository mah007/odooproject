# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fournisseur(models.Model):

    _name='parcauto.fournisseur'
    name=fields.Char(string="Nom", required=True)
    adresse=fields.Char(string="Adresse", required=True)
    fournisseur_id=fields.Char(string="Id", required=True)
    pneu_ids = fields.One2many('parcauto.pneu', 'fournisseur_id', string="Pneu")


    @api.model
    def create(self, vals):
        ordre = self.env['ir.sequence'].next_by_code('fournisseur.sequence') or '/'
        vals['fournisseur_id'] = ordre
        return super(fournisseur, self).create(vals)
