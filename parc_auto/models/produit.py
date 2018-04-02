# -*- coding: utf-8 -*-

from odoo import models, fields, api


class produit(models.Model):
    _name='parcauto.produit'
    name=fields.Char(string='Produits')
    produit_id=fields.Char('Produit N°' , required=True)
    prix_unit = fields.Integer(required=True)
    poids_unit= fields.Integer(required=True)

    @api.model
    def create(self, vals):
        prod = self.env['ir.sequence'].next_by_code('produit.sequence') or '/'
        vals['produit_id'] = prod
        return super(produit, self).create(vals)
