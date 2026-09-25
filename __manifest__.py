{
    'name': 'Inventory Product Updates',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Automatic Lot generation and Product Duration classification',
    'description': """
        - Automatic Lot generation based on PO number.
        - Long-Term and Short-Term product classification in Inventory tab.
        - Dedicated Scheduled Actions for product types.
    """,
    'author': 'Folklor',
    'depends': ['base', 'stock', 'purchase', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/schedule_action.xml',
        'views/res_config_setting.xml',
        'views/product_template.xml',
        'views/stock_quant_views.xml',
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
