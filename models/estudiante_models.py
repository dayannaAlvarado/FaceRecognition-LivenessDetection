# -*- coding: utf-8 -*-
import base64
import os
import shutil
from odoo import models, fields, api
from os import remove

from odoo.exceptions import ValidationError


class AsistenciasEstudiante(models.Model):
    _name = 'asistencias.estudiante'
    _rec_name = 'identificacion'
    nombres = fields.Char(string="Nombres", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    identificacion = fields.Char(string="Identificación", required=True, size=10)
    _sql_constraints = [
        ('def_identification_unique', 'unique(identificacion)', 'Identificación ya registrada en el sistema!')]
    foto = fields.Image(required=True)
    correo = fields.Char(string="Dirección de Correo")
    ciclo = fields.Selection(
        [('1', 'Primero'), ('2', 'Segundo'), ('3', 'Tercero'), ('4', 'Cuarto'), ('5', 'Quinto'), ('6', 'Sexto'),
         ('7', 'Séptimo'), ('8', 'Octavo'), ('9', 'Noveno'), ('10', 'Décimo'), ('egre', 'Egresado')], string="Ciclo")
    carrera_name = fields.Many2one('asistencias.carrera', 'Carrera')
    materia_name = fields.Many2one('asistencias.materia', 'Materia')
    docente_name = fields.Many2one('asistencias.docente', 'Docente')
    registro_id = fields.One2many('asistencias.registro', 'estudiante_name')

    def action_fotos(self):
        if self.foto:
            image_64_decode = base64.decodebytes(self.foto)
            nombre_local_imagen = self.identificacion + ".jpg"  # El nombre con el que queremos guardarla
            image_result = open(nombre_local_imagen, 'wb')  # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            source = "C:/Program Files (x86)/Odoo 13.0/server/" + nombre_local_imagen
            destination = "C:/Program Files (x86)/Odoo 13.0/server/odoo/addons/asistencias/images/" + nombre_local_imagen
            shutil.copy(source, destination)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Success'),
                    'message': 'Fotografía descargada exitosamente\n',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                }
            }

