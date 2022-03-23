#-*- coding: utf-8 -*-

from odoo import models, fields, api
'''
class AsistenciasEstudiante(models.Model):
     _name = 'asistencias.estudiante'
     nombres = fields.Char(string="Nombres", required=True)
     apellidos = fields.Char(string="Apellidos", required=True)
     foto = fields.Binary(string="Foto")
     ciclo = fields.Selection([('1','Primero'),('2','Segundo'),('3','Tercero'),('4','Cuarto'),('5','Quinto'),('6','Sexto'),
                               ('7','Séptimo'),('8','Octavo'), ('9','Noveno'),('10','Décimo'), ('egre','Egresado')], string="Ciclo")

     docente_id= fields.Many2one("asistencias.docente" ,string='Docente de Laboratorio')

class AsistenciasDocente(models.Model):
     _name = 'asistencias.docente'
     nombres = fields.Char(string="Nombres", required=True)
     apellidos = fields.Char(string="Apellidos", required=True)
     foto = fields.Binary(string="Fotografía", required=True)
     estudiante_id= fields.One2many("asistencias.estudiante", 'docente_id')

class AsistenciasLaboratorio(models.Model):
     _name = 'asistencias.laboratorio'
     nombre = fields.Char(string="Nombre", required=True)'''


#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:

