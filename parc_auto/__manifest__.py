# -*- coding: utf-8 -*-
{
    'name': "Parc Auto",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sara Hanyn",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Fleet & Vehicules Routing Management',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/menu_view.xml',
        'views/client_view.xml',
        #'views/agence_view.xml',
        'views/vehicule_view.xml',
        'views/chauffeur_view.xml',
        'views/demande_view.xml',
        'views/ordremission_view.xml',
        'views/produit_view.xml',
        'views/cvrptrigger_view.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'workflow/ordremission_workflow.xml'#,
        #'views/tree_view_asset.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    #'qweb':  [
    #    'static/src/xml/tree_view_button.xml'
    #],
}