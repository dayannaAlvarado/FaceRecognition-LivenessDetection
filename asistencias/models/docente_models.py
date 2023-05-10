# -*- coding: utf-8 -*-
import base64
import shutil
from odoo import models, fields, api


class AsistenciasDocente(models.Model):
    _name = 'asistencias.docente'
    _rec_name = "nombres"
    nombres = fields.Char(string="Nombres y Apellidos", required=True)
    #apellidos = fields.Char(string="Apellidos", required=True)
    correo = fields.Char(string="Dirección de Correo")
    foto = fields.Image(required=True)
    rol = fields.Selection(
        [('Docente', 'Docente')],default = 'Docente',
        string="Rol")

    identificacion = fields.Char(string="Identificación", required=True, size=10)
    _sql_constraints = [
        ('def_identification_unique', 'unique(identificacion)', 'Identificación ya registrada en el sistema!')]
    estudiante_id = fields.One2many('asistencias.estudiante', 'docente_name','Estudiantes')
    horario_id = fields.One2many('asistencias.horario', 'docente_name','Docente')
    carrera_name = fields.Many2one('asistencias.carrera', 'Carrera')


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