# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

    'summary': """Manage trainings""",

    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Test',
    'version': '0.1',


    'depends': ['base', 'board'],


    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/openacademy.xml',
		'views/partner.xml',
        'views/session_board.xml',
        'reports.xml'
    ],

    'demo': [
    ],

}

