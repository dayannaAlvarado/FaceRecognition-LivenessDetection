# -*- coding: utf-8 -*-
# from odoo import http
from odoo import http
from odoo.http import request
from odoo.http import Response




#class Asistencias(http.Controller):


#     @http.route('/asistencias/asistencias/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asistencias/asistencias/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asistencias.listing', {
#             'root': '/asistencias/asistencias',
#             'objects': http.request.env['asistencias.asistencias'].search([]),
#         })

#     @http.route('/asistencias/asistencias/objects/<model("asistencias.asistencias"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asistencias.object', {
#             'object': obj
#         })
