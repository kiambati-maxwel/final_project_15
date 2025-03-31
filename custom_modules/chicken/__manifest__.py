# -*- coding: utf-8 -*-
{
    'name': "Poultry Farm",
    'description': "Long description of module's purpose",
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/chicken_batch_views.xml',
        'views/chicken_cull_views.xml',
        'views/chicken_cull_sequence.xml',
        'views/chicken_eggs_views.xml',
        'views/chicken_feeding_views.xml',
        'views/chicken_vaccination_views.xml',
        'views/chicken_batch_menus.xml',
        'reports/chicken_batch_report.xml',
    ],
'assets': {
        'web.assets_backend': [
            'chicken/static/src/scss/custom_tree_styles.scss'
        ]
}
}
