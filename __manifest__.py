{
    'name': 'Stock Picking Importer',
    'version': '1.0',
    'depends': ['base', 'stock', 'base_import'],
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'category': 'Warehouse',
    'description': 'Import stock picking records from Excel.',
    'data': [
        'security/ir.model.access.csv',
        'wizards/stock_import_wizard_view.xml',

    ],
}
