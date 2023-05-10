# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
import  pdb
class Usuario(models.Model):
    _name = 'asistencias.usuario'
    _description="Informacion de los Usuarios del sistema"
    @api.model
    def create(self,vals):
        """
         Este metodo esta rediseñado para agregar el usuario con nombre de usuario y contraseña
        """
        if vals.get('pid', _('New')) == _('New'):
            vals['pid']= self.env['ir.sequence'].next_by_code('asistencias.usuario') or _('New')
        if vals.get('pid', False):
            vals['login']  = vals['pid']
            vals['password'] = vals['cedula']
        else:
            raise except_orm(_("Error"),_(''' PID NO VALIDO PARA GUARDAR EN EL REGISTRO'''))
        if vals.get('cmp_id', False):
            company_vals={
                'company_ids': [(4, vals.get("cmp_id"))],
                'company_id': vals.get('cmp_id')
            }
            vals.update(company_vals)
        res = super (Usuario, self).create(vals)
        #para iniciar el debug
        #pdb.set_trace()
        emp_gpr=self.env.ref('base.group_user')


        if res.tipo_usuario=='docente':
            grupo= self.env.ref("asistencias.group_asistencias_docente")
            new_grp_list=[grupo.id, emp_gpr.id]
            res.user_id.write({'groups_id' : [(6,0, new_grp_list)]})
            return res;
        if res.tipo_usuario=='admin':
            grupo= self.env.ref("asistencias.group_asistencias_admin")
            new_grp_list=[grupo.id, emp_gpr.id]
            res.user_id.write({'groups_id' : [(6,0, new_grp_list)]})
            return res;

    user_id= fields.Many2one ('res.users','User ID', ondelete="cascade", required=True,  delegate=True)
    usuario_name= fields.Char(string= 'Nombres', related='user_id.name', required=True)
    usuario_id= fields.Many2one('asistencias.usuario', 'Name')
    tipo_usuario= fields.Selection([
        ('docente', 'Docente'),
        ('admin', 'Admin'),
    ], string='Seleccione el tipo de usuario', required=True, default="docente", track_visibility="onchange"
    )
    imagen= fields.Binary()
    apellidos= fields.Char(string="Apellidos")
    pid= fields.Char("Usuario", required=True, default=lambda self: _('') )
    fecha_nacimiento = fields.Date('Fecha de Nacimiento ')
    telefono_convencional = fields.Char('Teléfono  convencional')
    telefono_celular = fields.Char('Teléfono  celular')
    cedula = fields.Char(string='Cédula', size=10, required=True)

    _sql_constraints =[
        ('cedula', 'unique(cedula)',"El usuario ya fue registrado con este número de cédula" )
    ]




