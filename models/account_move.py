# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    batch_id = fields.Many2one(comodel_name='stock.picking.batch', related='stock_move_id.batch_id', string="Lote")
    fleet_id = fields.Many2one(comodel_name='fleet.vehicle', related='stock_move_id.fleet_id', string="Vehiculo")