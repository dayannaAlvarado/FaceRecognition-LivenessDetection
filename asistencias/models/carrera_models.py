# -*- coding: utf-8 -*-
import base64
import shutil
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AsistenciasCarrera(models.Model):
    _name = 'asistencias.carrera'
    _rec_name = 'nombres'
    nombres = fields.Char(string="Nombre de la Carrera", required=True)
    horario_id = fields.One2many('asistencias.horario', 'carrera_name')
    docente_id = fields.One2many('asistencias.docente', 'carrera_name', 'Carrera')
    estudiante_id = fields.One2many('asistencias.estudiante', 'carrera_name')
    carrera_id = fields.One2many('asistencias.materia', 'carrera_name')
