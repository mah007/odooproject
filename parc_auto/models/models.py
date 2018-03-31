# -*- coding: utf-8 -*-

from odoo import models, fields, api



class agence(models.Model):
    _name='parcauto.agence'

    name=fields.Char(required=True)
    nombre_vehicule = fields.Integer(compute='_count_vehicules')
    descriprion = fields.Char(required=True)
    longtitude = fields.Char(required=True)
    laltitude = fields.Char(required=True)
    adresse = fields.Char(required=True)
    ville = fields.Char(required=True)
    pays = fields.Char(required=True)

    vehicule_ids = fields.One2many(
        'parcauto.vehicule', 'agence_id', string="Vehicules")

    @api.one
    def _count_vehicules(self):
        self.nombre_vehicule = len(self.vehicule_ids)

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


class demande(models.Model):
    _name='parcauto.demande'
    name = fields.Char(string="demande")
    demande_id=fields.Char('Demande N°' , required=True)

    client_id = fields.Many2one('parcauto.client', ondelete='set null', string="Client", index=True, required=True)

    colis=fields.Char(required=True)
    poids_total=fields.Integer(compute='_sum_poids_total')
    volume_total=fields.Integer(required=True)
    prix_total=fields.Integer(compute='_sum_prix_total')
    ville=fields.Char(required=True)
    pays = fields.Char(required=True)
    destination = fields.Char( required=True)
    produit_id = fields.Many2one('parcauto.produit', ondelete='set null', string="produit", index=True, required=True)
    p_prix_unit = fields.Integer(related='produit_id.prix_unit')
    p_poids_unit = fields.Integer(related='produit_id.poids_unit')

    @api.one
    def _sum_prix_total(self):
        self.prix_total = self.volume_total * self.p_prix_unit

    @api.one
    def _sum_poids_total(self):
        self.poids_total = self.volume_total * self.p_poids_unit

    @api.model
    def create(self, vals):
        dem = self.env['ir.sequence'].next_by_code('demande.sequence') or '/'
        vals['demande_id'] = dem
        return super(demande, self).create(vals)



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












