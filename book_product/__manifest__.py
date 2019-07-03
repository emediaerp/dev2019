# -*- coding: utf-8 -*-
{'name': "Product Book",
 'summary': """
       This module to customize product module to fit book requirements""",
 'description': """
            This module to customize product module to fit book requirements
    """,
 'author': "Mahmoud Elmenshawy",
 'website': "https://www.linkedin.com/in/mahmoudelmenshawy/",
 'category': 'HR',
 'version': '0.1',
 'depends': ['purchase','sale_management'],
 'data': [
     'data/data.xml',
     'security/security.xml',
     'security/ir.model.access.csv',
     'views/company_views.xml',
     'views/product_settings_views.xml',
     'views/product_views.xml',
 ],
 'demo': []
 }
