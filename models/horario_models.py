# -*- coding: utf-8 -*-
import base64
import shutil
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AsistenciasHorario(models.Model):
    _name = 'asistencias.horario'
    hora_inicio = fields.Char(string="Hora de inicio")
    hora_fin = fields.Char(string="Hora de Fin")
    paralelo= fields.Selection(
        [('a', 'A'), ('b', 'B')],
        string="Paralelo")

    dia_semana = fields.Selection(
        [('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'), ('4', 'Jueves'), ('5', 'Viernes')], string="Día al que pertenece")
    ciclo = fields.Selection(
        [('1', 'Primero'), ('2', 'Segundo'), ('3', 'Tercero'), ('4', 'Cuarto'), ('5', 'Quinto'), ('6', 'Sexto'),
         ('7', 'Séptimo'), ('8', 'Octavo'), ('9', 'Noveno'), ('10', 'Décimo'), ('egre', 'Egresado')], string="Ciclo")
    docente_name = fields.Many2one('asistencias.docente', 'Docente')
    carrera_name = fields.Many2one('asistencias.carrera', 'Carrera')
    materia_name = fields.Many2one('asistencias.materia', 'Materia')