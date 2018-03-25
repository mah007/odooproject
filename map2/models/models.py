# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customer(models.Model):
     _name = 'map2.customer'

     name = fields.Char(string="Name", required=True)
     address = fields.Text(required=True)

     @api.multi
     def locate_customer(self): return {
         "type": "ir.actions.act_url",
         "url": "static/map/googlemap.html?longitude=" + self.address + "&key=AIzaSyAZkVmtvhuKp9U34DlKIicoW3CVEAuM0zM",
         "target": "new",
     }

