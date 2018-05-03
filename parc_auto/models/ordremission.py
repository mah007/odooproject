# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math
import geocoder
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

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
    chauffeur_id=fields.Many2one('parcauto.chauffeur', 'Chauffeur',required=True)
    agence_dep=fields.Many2one('parcauto.agence', 'Agence Départ',required=True)
    agence_arr = fields.Many2one('parcauto.agence', 'Agence Arrivée',required=True)
    client_id=fields.Many2one('parcauto.client', 'Clients',required=True)
    produit_id=fields.Many2one('parcauto.produit', 'Colis',required=True)
    vehicule_id=fields.Many2one('parcauto.vehicule',ondelete='set null', string="Véhicule",required=True, index=True)


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
    def main(self):
        # Create the data.
        data = create_data_array(self)
        locations = data[0]
        demands = data[1]
        num_locations = len(locations)
        depot = 0  # The depot is the start and end point of each route.
        num_vehicles = 5
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
                        route += str(node_index) + " -> "
                        # Add the distance to the next node.
                        route_dist += dist_callback(node_index, node_index_next)
                        # Add demand.
                        route_demand += demands[node_index_next]
                        index = index_next
                        index_next = assignment.Value(routing.NextVar(index))

                    node_index = routing.IndexToNode(index)
                    node_index_next = routing.IndexToNode(index_next)
                    route += str(node_index) + " -> " + str(node_index_next)
                    route_dist += dist_callback(node_index, node_index_next)
                    sresult += "Route for vehicle " + str(vehicle_nbr) + " : " + route + "\n"
                    sresult += "Distance of route " + str(vehicle_nbr) + " : " + str(route_dist)
                    sresult += "\nDemand met by vehicle " + str(vehicle_nbr) + " : " + str(route_demand) + "\n\n"
            else:
                sresult += 'No solution found.'
        else:
            sresult += 'Specify an instance greater than 0.'
        file = open("/vagrant/cvrpresult.tmp", "w")
        file.write(sresult)
        file.close()

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
  self._cr.execute("SELECT id,destination FROM parcauto_demande")
  loc_temp = []
  for res in self.env.cr.fetchall():
    loc_temp.append(res)

  g = geocoder.mapquest([i[1] for i in loc_temp], method='batch', key='2M3DloLAMyAYBjIdZFBpS7HejnT00e8r')

  for result in g:
    locations.append([float(result.latlng[0]), float(result.latlng[1])])

  ##############

  self._cr.execute("rollback")

  demands = [0]
  self._cr.execute("SELECT poids_total FROM parcauto_demande")
  for res in self.env.cr.fetchall():
    demands.append(int(res[0]))

  data = [locations, demands]
  return data






