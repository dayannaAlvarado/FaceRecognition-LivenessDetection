# -*- coding: utf-8 -*-
import base64
import shutil
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AsistenciasMateria(models.Model):
    _name = 'asistencias.materia'
    _rec_name = "nombres"
    nombres = fields.Char(string="Nombre de la Materia", required=True)
    carrera_name = fields.Many2one('asistencias.carrera', 'Carrera a la que pertenece')
    horario_id = fields.One2many('asistencias.horario', 'materia_name')
    estudiante_id = fields.One2many('asistencias.estudiante', 'materia_name')

    def action_listar(self):
        if self.nombres:
            for carrera in  self.carrera_name:
                print(carrera)





