# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import math
import json
import geocoder
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

class demande(models.Model):

    _name = 'parcauto.demande'
    name = fields.Char(string="demande")
    demande_id = fields.Char('Demande N°' , required=True)

    state = fields.Selection([
        ('paslivre', "Pas livrée"),
        ('encours', "En cours"),
        ('livre', "Livrée"),
    ], default='paslivre')

    volume_total = fields.Integer(required=True)

    adresse = fields.Char(related='client_id.adresse_cli', ondelete='set null', store=True)
    adr_temp = fields.Char(related='client_id.adresse_cli')

    date_demande = fields.Date(required=True)

    poids_total = fields.Integer(compute='_sum_poids_total',store=True)
    prix_total = fields.Integer(compute='_sum_prix_total',store=True)

    frais_livraison = fields.Float(compute='_sum_frais_livraison',store=True, string="Frais de livraison (DH)")

    client_id = fields.Many2one('parcauto.client', ondelete='set null', string="Client", index=True, required=True)
    produit_id = fields.Many2one('parcauto.produit', ondelete='set null', string="Produit", index=True, required=True)
    ordremission_id = fields.Many2one('parcauto.ordremission', ondelete='set null', string="Ordre Mission", index=True)

    p_prix_unit = fields.Integer(related='produit_id.prix_unit')
    p_poids_unit = fields.Integer(related='produit_id.poids_unit')


    # adresse client = adresse livraison
    # @api.depends('client_id','adr_temp')
    # def _sum_prix_total(self):
    # self.adresse = self.adr_temp

    # prix total
    @api.depends('volume_total', 'p_prix_unit')
    def _sum_prix_total(self):
        self.prix_total = self.volume_total * self.p_prix_unit

    # poids total
    @api.depends('volume_total', 'p_poids_unit')
    def _sum_poids_total(self):
        self.poids_total = self.volume_total * self.p_poids_unit

    # calcul frais de livraison
    @api.depends('volume_total', 'poids_total')
    def _sum_frais_livraison(self):
        frais = 0
        if(self.volume_total > 0 and self.volume_total < 10):
            frais += 15
        if(self.volume_total >= 10 and self.volume_total < 20):
            frais += 30
        if(self.volume_total >= 20 and self.volume_total < 40):
            frais += 45
        if(self.volume_total >= 40 and self.volume_total < 60):
            frais += 65
        if(self.volume_total >= 60 and self.volume_total < 90):
            frais += 90
        if(self.volume_total >= 90):
            frais += 1.2 * self.volume_total

        if (self.poids_total > 0 and self.poids_total < 10):
            frais += 15
        if (self.poids_total >= 10 and self.poids_total < 20):
            frais += 30
        if (self.poids_total >= 20 and self.poids_total < 40):
            frais += 45
        if (self.poids_total >= 40 and self.poids_total < 60):
            frais += 65
        if (self.poids_total >= 60 and self.poids_total < 100):
            frais += 90
        if (self.poids_total >= 100):
            frais += 1.1 * self.poids_total

        self.frais_livraison = frais

    # sequence
    @api.model
    def create(self, vals):
        dem = self.env['ir.sequence'].next_by_code('demande.sequence') or '/'
        vals['demande_id'] = dem
        record = super(demande, self).create(vals)
        if record.poids_total > 1000:
           raise exceptions.ValidationError('Total weight can not exceed 1000!')
        return record

    @api.multi
    def write(self, vals):
        record = super(demande, self).write(vals)
        if self.poids_total > 1000:
            raise exceptions.ValidationError('Total weight can not exceed 1000!')
        return record

    @api.multi
    def main(self):
        # Create the data.
        data = create_data_array(self)
        locations = data[0]
        demands = data[1]
        num_locations = len(locations)
        depot = 0  # The depot is the start and end point of each route.
        num_vehicles = 0
        self._cr.execute("SELECT COUNT(*) FROM parcauto_vehicule WHERE etat = 'disponible'")
        num_vehicles_t = self.env.cr.fetchall()
        num_vehicles = int(num_vehicles_t[0][0])
        self._cr.execute("rollback")
        sresult = ''

        # Create routing model.
        if num_locations > 0:
            routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot)
            search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

            # Callback to the distance function.
            dist_between_locations = CreateDistanceCallback(locations)
            dist_callback = dist_between_locations.Distance
            routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)

            # Put a callback to the demands.
            demands_at_locations = CreateDemandCallback(demands)
            demands_callback = demands_at_locations.Demand

            # Add a dimension for demand.
            slack_max = 0
            vehicle_capacity = 1000
            fix_start_cumul_to_zero = True
            demand = "Demand"
            routing.AddDimension(demands_callback, slack_max, vehicle_capacity,
                                 fix_start_cumul_to_zero, demand)

            # Solve, displays a solution if any.
            assignment = routing.SolveWithParameters(search_parameters)
            if assignment:
                # Display solution.
                # Solution cost.
                # print "Total distance of all routes: " + str(assignment.ObjectiveValue()) + "\n"

                for vehicle_nbr in range(num_vehicles):
                    index = routing.Start(vehicle_nbr)
                    index_next = assignment.Value(routing.NextVar(index))
                    route = ''
                    route_dist = 0
                    route_demand = 0

                    while not routing.IsEnd(index_next):
                        node_index = routing.IndexToNode(index)
                        node_index_next = routing.IndexToNode(index_next)
                        route += str(node_index) + ","
                        # Add the distance to the next node.
                        route_dist += dist_callback(node_index, node_index_next)
                        # Add demand.
                        route_demand += demands[node_index_next]
                        index = index_next
                        index_next = assignment.Value(routing.NextVar(index))

                    node_index = routing.IndexToNode(index)
                    node_index_next = routing.IndexToNode(index_next)
                    route += str(node_index) + "," + str(node_index_next)
                    route_dist += dist_callback(node_index, node_index_next)
                    sresult += route + "\n"
                    sresult = sresult.replace("0,","").replace(",0","").replace("0\n","").replace("0\r","")
                    fresult = sresult.split("\n")
                    fresult = fresult[:-1]
            else:
                raise exceptions.except_orm(_("Error"),_("No solution availabe :(, please provide another vehicles"))
        else:
            sresult += 'Specify an instance greater than 0.'

        # file = open("/vagrant/cvrpresult.tmp", "w")
        # file.write(json.dumps(fresult))
        # file.close()

        # les vehicules dispo
        vehicules_dispo = []

        self._cr.execute("SELECT id FROM parcauto_vehicule WHERE etat = 'disponible'")

        for veh in self.env.cr.fetchall():
            vehicules_dispo.append(int(veh[0]))

        self._cr.execute("rollback")

        # les demandes à livrer
        self._cr.execute("SELECT d.id,d.adresse "
                         "FROM parcauto_demande d "
                         "LEFT JOIN parcauto_ordremission om ON om.id = d.ordremission_id "
                         "WHERE d.state = 'paslivre' AND om.id IS NULL")

        loc_temp1 = []
        for res in self.env.cr.fetchall():
            loc_temp1.append(res)

        self._cr.execute("rollback")

        if loc_temp1 and vehicules_dispo:

            # tables de conversion entre id demande & index dans l'ordre de selection
            ordre_demandes = [int(x[0]) for x in loc_temp1]

            # max id ordre mission
            # self._cr.execute("SELECT MAX(id)+1 FROM parcauto_ordremission")

            # self._cr.execute("rollback")

            for elem in fresult:
                self._cr.execute("INSERT INTO parcauto_ordremission "
                                 "(create_uid, "
                                 "name, "
                                 "vehicule_id,"
                                 "ordre_id, "
                                 "write_uid, "
                                 "state, "
                                 "write_date, "
                                 "create_date) "
                                 "SELECT 1, "
                                 "       concat('OM-'::text,(Max(id)+1)::text), "
                                 "" + str(vehicules_dispo[0]) + ","
                                 "       concat('OM/'::text,(Max(id)+1)::text), "
                                 "       1, "
                                 "       'draft', "
                                 "       now() at time zone 'utc', "
                                 "       now() at time zone 'utc'  "
                                 "FROM parcauto_ordremission "
                                 "RETURNING Id")

                om_id_t = self.env.cr.fetchall()
                om_id = om_id_t[0][0]

                self._cr.execute("commit")

                # get wkf_id

                self._cr.execute("SELECT Id FROM wkf WHERE osv = 'parcauto.ordremission'")
                wkf_id_t = self.env.cr.fetchall()
                wkf_id = wkf_id_t[0][0]

                self._cr.execute("commit")

                #get wkf_activity

                self._cr.execute("SELECT Id FROM wkf_activity WHERE name = 'Draft'")
                wkf_act_t = self.env.cr.fetchall()
                wkf_act = wkf_act_t[0][0]

                self._cr.execute("commit")


                # wkf_instance
                self._cr.execute("INSERT INTO wkf_instance"
                                 "("
                                 "res_type,"
                                 "uid,"
                                 "wkf_id,"
                                 "state,"
                                 "res_id"
                                 ")"
                                 "VALUES"
                                 "("
                                 "'parcauto.ordremission',"
                                 "1,"
                                 "" + str(wkf_id) +","
                                 "'active',"
                                 ""+ str(om_id) +""
                                 ")"
                                 "RETURNING Id")

                wkf_inst_t = self.env.cr.fetchall()
                wkf_inst_id = wkf_inst_t[0][0]

                self._cr.execute("commit")

                # wkf_workitem
                self._cr.execute("INSERT INTO wkf_workitem"
                                 "("
                                 "act_id,"
                                 "inst_id,"
                                 "subflow_id,"
                                 "state"
                                 ")"
                                 "VALUES"
                                 "("
                                 ""+ str(wkf_act) +","
                                 ""+ str(wkf_inst_id) +","
                                 "NULL,"
                                 "'complete'"
                                 ");")

                self._cr.execute("commit")

                # le vehicule passe en état mission
                self._cr.execute("UPDATE parcauto_vehicule SET etat='enmission' WHERE Id = " + str(vehicules_dispo[0]))
                self._cr.execute("commit")

                vehicules_dispo.pop(0)

                te = elem.split(",")
                te = map(int, te)
                for el in te:
                    query = "UPDATE parcauto_demande SET ordremission_id = " + str(om_id) + " , state = 'encours' WHERE Id = " + str(ordre_demandes[el-1])
                    self._cr.execute(query)
                    print query
                    self._cr.execute("commit")
                raise exceptions.Warning('Vehicle routing succesfuly calculated!')

        else:
            raise exceptions.except_orm(_("Alert"), _("no orders to deliver or vehicule routing has been already calculated"))






def distance(x1, y1, x2, y2):
    # Manhattan distance
    dist = abs(x1 - x2) + abs(y1 - y2)

    return dist


class CreateDistanceCallback(object):
    """Create callback to calculate distances between points."""

    def __init__(self, locations):
        """Initialize distance array."""
        size = len(locations)
        self.matrix = {}

        for from_node in xrange(size):
            self.matrix[from_node] = {}
            for to_node in xrange(size):
                x1 = locations[from_node][0]
                y1 = locations[from_node][1]
                x2 = locations[to_node][0]
                y2 = locations[to_node][1]
                self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

    def Distance(self, from_node, to_node):
        return int(self.matrix[from_node][to_node])


# Demand callback
class CreateDemandCallback(object):
    """Create callback to get demands at each location."""

    def __init__(self, demands):
        self.matrix = demands

    def Demand(self, from_node, to_node):
        return self.matrix[from_node]


def create_data_array(self):
    locations = [[float(33.573110), float(-7.589843)]]
    self._cr.execute("SELECT d.id,d.adresse "
                     "FROM parcauto_demande d "
                     "LEFT JOIN parcauto_ordremission om ON om.id = d.ordremission_id "
                     "WHERE d.state = 'paslivre' AND om.id IS NULL")
    loc_temp = []
    for res in self.env.cr.fetchall():
        loc_temp.append(res)

    if loc_temp:

        g = geocoder.mapquest([i[1] for i in loc_temp], method='batch', key='2M3DloLAMyAYBjIdZFBpS7HejnT00e8r')

        for result in g:
            locations.append([float(result.latlng[0]), float(result.latlng[1])])

        ##############

        self._cr.execute("rollback")

        demands = [0]
        self._cr.execute("SELECT d.poids_total "
                         "FROM parcauto_demande d "
                         "LEFT JOIN parcauto_ordremission om ON om.id = d.ordremission_id "
                         "WHERE d.state = 'paslivre' AND om.id IS NULL")
        for res in self.env.cr.fetchall():
            demands.append(int(res[0]))
        data = [locations, demands]

    else:
        data = [[], []]
    return data