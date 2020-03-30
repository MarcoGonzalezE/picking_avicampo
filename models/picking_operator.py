# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockPickingOperator(models.Model):
    _name = 'stock.picking.operator'
    _description = 'Informacion del operador'    

    name = fields.Char(string='Nombre', required=True, translate=True)
    description = fields.Text(string='Descripcion', translate=True)