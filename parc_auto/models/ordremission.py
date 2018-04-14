# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ordremission(models.Model):
    _name='parcauto.ordremission'
    name = fields.Char(string='Ordre')
    ordre_id = fields.Char('Ordre Mission N°')

    current_user = fields.Many2one('res.users', compute='_get_current_user')

    state = fields.Selection([
        ('draft', "Draft"),
        ('submitted', "Submitted"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ])
    chauffeur_id=fields.Many2one('parcauto.chauffeur', 'Chauffeur')
    agence_dep=fields.Many2one('parcauto.agence', 'Agence Départ')
    agence_arr = fields.Many2one('parcauto.agence', 'Agence Arrivée')
    client_id=fields.Many2one('parcauto.client', 'Clients')
    produit_id=fields.Many2one('parcauto.produit', 'Colis')
    vehicule_id=fields.Many2one('parcauto.vehicule',ondelete='set null', string="Véhicule", index=True)


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

    @api.depends()
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user
        # i think this work too so you don't have to loop
        self.update({'current_user' : self.env.user.id})

class chauffeur(models.Model):
    _name='parcauto.chauffeur'
    name=fields.Char(string="Nom")


