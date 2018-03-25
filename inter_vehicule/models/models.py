# -*- coding: utf-8 -*-

from odoo import models, fields, api



class vehicule(models.Model):
    _name='inter_vehicule.vehicule'

    #sequence = fields.Char('Sequence', readonly=True)

    sequence_id = fields.Char('Sequence', readonly=True)
    bloque = fields.Integer(required=True, default=0)
    is_manager= fields.Boolean(compute="_check_user_group")

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('inter_vehicule.sequence') or '/'
        vals['sequence_id'] = seq
        return super(vehicule, self).create(vals)

    famille_id=fields.Many2one('inter_vehicule.famille',
    ondelete='set null', string="Famille", index=True)
    matricule_id=fields.Many2one('inter_vehicule.matricule',
                                 ondelete='set null', string="Matricule", index=True)




    anomalie=fields.Char(required=True)



    piece_id = fields.Many2one('inter_vehicule.piece',
                                 ondelete='set null', string="Piece", index=True)
    quantite = fields.Integer(required=True)
    cout_piece = fields.Integer(required=True)
    prestation=fields.Char(required=True)
    total_ht=fields.Float(compute='_total_ht' , store=True)
    total_ttc=fields.Float(compute='_total_ttc' , store=True)
    #tax_id = fields.Many2one('account.tax', 'repair_operation_line_tax', 'repair_operation_line_id', 'tax_id', 'Taxes')
    #tax_id = fields.Many2one('account.invoice.tax', string='Taxes')

    @api.depends('cout_piece','quantite')
    def _total_ht(self):
        self.total_ht = self.cout_piece * self.quantite

    @api.depends('total_ht')
    def _total_ttc(self):
        self.total_ttc = 1.196 * self.total_ht

    @api.multi
    def blocker_saisie(self):
        self.bloque = 1

    @api.one
    def _check_user_group(self):
        self.is_manager = self.env.user.has_group('inter_vehicule.group_manager')


class famille(models.Model):
    _name='inter_vehicule.famille'

    name=fields.Char(required=True)


class piece(models.Model):
    _name='inter_vehicule.piece'

    name=fields.Char(required=True)

class matricule(models.Model):
    _name='inter_vehicule.matricule'

    name=fields.Char(required=True)
    marque=fields.Char(required=True)
    model=fields.Char(required=True)
    etat=fields.Selection([
        ('disponible', "Disponible"),
        ('mission', "En Mission"),
        ('reparation', "En Réparation"),
    ], default='disponible')

    @api .multi
    def action_disponible(self):
        self.state = 'disponible'

    @api.multi
    def action_mission(self):
            self.state = 'mission'

    @api.multi
    def action_reparation(self):
            self.state = 'reparation'


