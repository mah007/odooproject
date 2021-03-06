# -*- coding: utf-8 -*-
from odoo import http

class ParcAuto(http.Controller):
     @http.route('/parcauto/gmdirection', auth='public', website=True)
     def index(self, **kw):
         return """
                <html> 
                    <head> 
                    <title>Routing des commandes</title> 
                    <style> 
                        html, 
                        body, 
                        #map { 
                          height: 100%; 
                          width: 100%; 
                          margin: 0px; 
                          padding: 0px 
                        }	 
                    </style> 
                    </head> 
                <body> 
                 
                <div id="map"></div> 
                <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBBtu9B2Imf_V5sSVlHeI8lWulzDQvpzyI"></script> 
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script> 
                 
                <script> 
                var geocoder; 
                var map; 
                var directionsDisplay; 
                var directionsService = new google.maps.DirectionsService(); 
                 
                url_string = window.location.href; 
                url = new URL(url_string); 
                locationst = url.searchParams.get("locations"); 
                 
                locations = []; 
                 
                var locarray = locationst.split('],['); 
                 
                for(var i=0; i<locarray.length;i++) 
                { 
                    tloc = locarray[i].replace('[','').replace(']','').split(','); 
                    tarr = [tloc[0], parseFloat(tloc[1]), parseFloat(tloc[2]), parseInt(tloc[3])]; 
                    locations.push(tarr); 
                } 
                 
                function initialize() { 
                  directionsDisplay = new google.maps.DirectionsRenderer(); 
                 
                 
                  var map = new google.maps.Map(document.getElementById('map'), { 
                    zoom: 10, 
                    center: new google.maps.LatLng(-33.92, 151.25), 
                    mapTypeId: google.maps.MapTypeId.ROADMAP 
                  }); 
                  directionsDisplay.setMap(map); 
                  var infowindow = new google.maps.InfoWindow(); 
                 
                  var marker, i; 
                  var request = { 
                    travelMode: google.maps.TravelMode.DRIVING 
                  }; 
                  for (i = 0; i < locations.length; i++) { 
                    marker = new google.maps.Marker({ 
                      position: new google.maps.LatLng(locations[i][1], locations[i][2]), 
                      map: map 
                    }); 
                 
                    google.maps.event.addListener(marker, 'click', (function(marker, i) { 
                      return function() { 
                        infowindow.setContent(locations[i][0]); 
                        infowindow.open(map, marker); 
                      } 
                    })(marker, i)); 
                    if (i == 0) request.origin = marker.getPosition(); 
                    else if (i == locations.length - 1) request.destination = marker.getPosition(); 
                    else { 
                      if (!request.waypoints) request.waypoints = []; 
                      request.waypoints.push({ 
                        location: marker.getPosition(), 
                        stopover: true 
                      }); 
                    } 
                 
                  } 
                  directionsService.route(request, function(result, status) { 
                    if (status == google.maps.DirectionsStatus.OK) { 
                      directionsDisplay.setDirections(result); 
                    } 
                  }); 
                } 
                google.maps.event.addDomListener(window, "load", initialize); 
                </script> 
                 
                </body> 
                </html>
                """
#     @http.route('/parc_auto/parc_auto/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('parc_auto.listing', {
#             'root': '/parc_auto/parc_auto',
#             'objects': http.request.env['parc_auto.parc_auto'].search([]),
#         })

#     @http.route('/parc_auto/parc_auto/objects/<model("parc_auto.parc_auto"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('parc_auto.object', {
#             'object': obj
#         })