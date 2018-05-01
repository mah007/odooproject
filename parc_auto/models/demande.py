# -*- coding: utf-8 -*-

from odoo import models, fields, api

class demande(models.Model):
    _name='parcauto.demande'
    name = fields.Char(string="demande")
    demande_id=fields.Char('Demande N°' , required=True)
    client_id = fields.Many2one('parcauto.client', ondelete='set null', string="Client", index=True, required=True)
    poids_total=fields.Integer(compute='_sum_poids_total',store=True)
    volume_total=fields.Integer(required=True)
    prix_total=fields.Integer(compute='_sum_prix_total',store=True)
    ville=fields.Many2one('parcauto.ville', ondelete='set null', string="Ville", index=True, required=True)
    destination = fields.Char(required=True)
    produit_id = fields.Many2one('parcauto.produit', ondelete='set null', string="Produit", index=True, required=True)
    p_prix_unit = fields.Integer(related='produit_id.prix_unit')
    p_poids_unit = fields.Integer(related='produit_id.poids_unit')

    @api.depends('volume_total','p_prix_unit')
    def _sum_prix_total(self):
        self.prix_total = self.volume_total * self.p_prix_unit

    @api.depends('volume_total', 'p_poids_unit')
    def _sum_poids_total(self):
        self.poids_total = self.volume_total * self.p_poids_unit

    @api.model
    def create(self, vals):
        dem = self.env['ir.sequence'].next_by_code('demande.sequence') or '/'
        vals['demande_id'] = dem
        return super(demande, self).create(vals)