# -*- coding: utf-8 -*-
{
    'name': "Costeo Avicampo",
    'summary': """
            Grupo Alvamex
         """,
    'description': """
        Modulo para las operaciones de inventario \n
        Permite agregar informacion de: \n
        - Chofer \n
        - No. Sello \n
        - Ticket \n
        - Lote \n
        - Granja \n
        - Fecha de transferencia de salida \n
        - Fecha de entregada en granja \n
        - Folio del traspaso, 
    """,

    'author': "Marco Gonzalez",
    'website': "http://www.grupoalvamex.com",
    'category': 'Inventory operations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','purchase', 'sale', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'views/stock_picking_batch.xml',
        'views/stock_picking_operator.xml',
        'views/purchase_order_line.xml',
        'views/account_move.xml',
        'views/mrp_production.xml',
        'views/account_invoice_line.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}