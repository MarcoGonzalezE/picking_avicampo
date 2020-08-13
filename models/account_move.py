# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    batch_id = fields.Many2one(comodel_name='stock.picking.batch', string="Lote", store=True)
    fleet_id = fields.Many2one(comodel_name='fleet.vehicle', string="Vehiculo", store=True)
    stock_move_id = fields.Many2one()