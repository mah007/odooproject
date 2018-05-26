# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ordremission(models.Model):
    _name='parcauto.ordremission'
    name = fields.Char(string='Ordre')
    ordre_id = fields.Char('Ordre Mission N°')

    state = fields.Selection([
        ('draft', "Draft"),
        ('submitted', "Submitted"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ])

    chauffeur_id=fields.Many2one('parcauto.chauffeur', string="Chauffeur")
    # demande_id=fields.Many2one('parcauto.demande', 'Colis',required=True)
    vehicule_id=fields.Many2one('parcauto.vehicule',ondelete='set null', string="Véhicule",required=True, index=True)
    demande_ids = fields.One2many('parcauto.demande', 'ordremission_id', string="Demandes")


    @api.model
    def create(self, vals):
        ordre = self.env['ir.sequence'].next_by_code('ordremission.sequence') or '/'
        vals['ordre_id'] = ordre
        return super(ordremission, self).create(vals)


    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_submit(self):
        self.state = 'submitted'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def write(self, vals):
        chauffeur = self.chauffeur_id
        chauffeur.etat = 'mission'
        return True





