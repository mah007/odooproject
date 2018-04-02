# -*- coding: utf-8 -*-

from odoo import models, fields, api

class vehicule(models.Model) :
    _name='parcauto.vehicule'
    name = fields.Char(string="vehicule")
    sequence_id = fields.Char('Sequence', readonly=True)
    etat = fields.Selection([
        ('disponible', "Disponible"),
        ('mission', "En Mission"),
        ('reparation', "En Réparation"),
    ], default='disponible')

    matricule = fields.Char(required=True)
    marque = fields.Char(required=True)
    modele = fields.Char(required=True)

    age= fields.Char(required=True , string="Age(Ans)")
    compteur = fields.Char(required=True , string="Compteur(Km)")

    agence_id = fields.Many2one('parcauto.agence', ondelete='set null', string="Agence", index=True, required=True)


    activity = fields.Selection([
        ('mes', "Messagerie"),
        ('dt', "DT"),
        ('dg', "DG"),
    ], default='mes' , string='Activités')


    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('vehicule.sequence') or '/'
        vals['sequence_id'] = seq
        return super(vehicule, self).create(vals)


    @api.multi
    def action_disponible(self):
        self.state = 'disponible'

    @api.multi
    def action_mission(self):
        self.state = 'mission'

    @api.multi
    def action_reparation(self):
        self.state = 'reparation'

    @api.multi
    def action_mes(self):
        self.state = 'messagerie'

    @api.multi
    def action_dt(self):
        self.state = 'dt'

    @api.multi
    def action_dg(self):
        self.state = 'dg'