{
    'name': "Smart Report",
    'version': "15.0.0.0",
    'author': "SMART",
    'category': "Tools",
    'summary': "Custom report in accounting",
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'views/res_config_settings_views.xml',
        'views/pdf_report.xml'
    ],
    'demo': [],
    'depends': ['account_accountant',],
    'assets': {
        'web.assets_backend': [
            '/smart_report/static/src/js/smart_dynamic_report.js',
        ],
        'web.assets_qweb': [
            '/smart_report/static/src/xml/smart_dynamic_report.xml'
        ],
    },
    'installable': True,
}
