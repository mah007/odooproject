# -*- coding: utf-8 -*-

from odoo import models, fields, api
import geocoder


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

    chauffeur_id=fields.Many2one('parcauto.chauffeur', string="Chauffeur",domain=[('etat', '=', 'disponible')])
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
        record = super(ordremission, self).write(vals)
        id_chauffeur = self.chauffeur_id.id
        if id_chauffeur:
            query = "UPDATE parcauto_chauffeur SET etat = 'mission' WHERE id = " + str(id_chauffeur)
            self._cr.execute(query)
            self._cr.execute("commit")
        return record

    @api.multi
    def locate_demands(self):
        id_om = self.id
        query = "SELECT demande_id,adresse FROM parcauto_demande WHERE ordremission_id = " + str(id_om)
        self._cr.execute(query)

        loc_temp = []
        for res in self.env.cr.fetchall():
            loc_temp.append(res)

        self._cr.execute("rollback")

        url = "about:blank"

        if loc_temp:
            names = [i[0] for i in loc_temp]
            addresses = [i[1] for i in loc_temp]

            param = "['Agence',33.573110,-7.589843,1]"

            for x in range(len(names)):
                g = geocoder.google(addresses[x],key="AIzaSyBBtu9B2Imf_V5sSVlHeI8lWulzDQvpzyI")
                astr = ",['"+str(names[x])+"',"+str(g.latlng[0])+","+str(g.latlng[1])+","+str((x+2))+"]"
                param += astr

            param += ",['Agence',33.573110,-7.589843,"+str(len(names)+2)+"]"


            url = '/parcauto/gmdirection?locations='+param

        self._cr.execute("rollback")

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }




