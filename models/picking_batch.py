# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPickingBatch(models.Model):
    _name = 'stock.picking.batch'
    _description = 'Informacion del lote'    

    name = fields.Char(string='Nombre', required=True, translate=True)
    state = fields.Selection([('disable','Desactivado'),('enable','Activado')],default="enable")
    description = fields.Text(string='Descripcion', translate=True)

