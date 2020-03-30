# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	batch = fields.Many2one(comodel_name='stock.picking.batch', string="Lote")	
	fleet = fields.Many2one(comodel_name='fleet.vehicle', string="Vehiculo")
	order_id = fields.Many2one()
	partner_id = fields.Many2one()
	product_id = fields.Many2one()
	name = fields.Text()
	date_planned = fields.Datetime()
	fleet_id = fields.Many2one()
	batch_id = fields.Many2one()
	location_dest_id = fields.Many2one()
	product_uom = fields.Many2one()
	price_unit = fields.Float()
	taxes_id = fields.Many2many()
	price_subtotal = fields.Monetary()
	state = fields.Selection()
