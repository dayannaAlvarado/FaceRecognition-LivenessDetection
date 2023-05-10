# -*- coding: utf-8 -*-
{
    'name': "asistencias",

    'summary': """
       Modulo de registro de Asistencias con reconocimiento facial""",

    'description': """
        Long description of module's purpose  1...
    """,

    'author': "Dayanna Alvarado",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        #'views/views.xml',
        'security/ir.model.access.csv',
        'security/asistencias_security.xml',
        'views/estudiante_views.xml',
        'views/docente_view.xml',
        'views/registro_views.xml',
        'views/carrera_views.xml',
        'views/materia_views.xml',
        'views/horario_views.xml',
        'views/reporte_views.xml',
        'views/usuario_views.xml',
        'views/menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
}
