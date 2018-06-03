# -*- coding: utf-8 -*-

from odoo import models, fields, api

class pneu(models.Model):

    _name='parcauto.pneu'
    name=fields.Char(string="Marque", required=True)
    duree_vie=fields.Integer(string="Durée de vie", required=True)
    width=fields.Integer(string="Largeur CM")
    diametre=fields.Integer(string="Diamètre CM")
    pneu_id=fields.Char(string="Id")
    date_acquisition=fields.Date(string="Date d'acquistion", required=True)
    montant_HT=fields.Char(string="Montant HT (dh)", required=True)
    vehicule_id = fields.Many2one('parcauto.vehicule', ondelete='set null', string="Véhicule", index=True)
    fournisseur_id = fields.Many2one('parcauto.fournisseur', ondelete='set null', string="Fournisseur", index=True, required=True)

    @api.model
    def create(self, vals):
        ordre = self.env['ir.sequence'].next_by_code('pneu.sequence') or '/'
        vals['pneu_id'] = ordre
        return super(pneu, self).create(vals)

