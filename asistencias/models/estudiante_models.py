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
    rol = fields.Selection(
        [('Estudiante', 'Estudiante')], default='Estudiante',
        string="Rol")
    _sql_constraints = [
        ('def_identification_unique', 'unique(identificacion)', 'Identificación ya registrada en el sistema!')]
    foto = fields.Image(required=True)
    correo = fields.Char(string="Dirección de Correo")
    ciclo = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('4', '5'), ('6', '6'),
         ('7', '7'), ('8', '8'), ('8', '9'), ('10', '10')], string="Ciclo")
    paralelo= fields.Selection([('A','A'), ('B','B')], string="Paralelo")

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

