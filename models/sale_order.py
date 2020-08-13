# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_is_zero, float_compare
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	name = fields.Text()
	order_id = fields.Many2one()
	product_id = fields.Many2one()
	product_uom_qty = fields.Float()
	product_uom = fields.Many2one()
	customer_lead = fields.Float()
	batch_id = fields.Many2one()

	@api.multi
	def _prepare_order_line_procurement(self, group_id=False):
		rec = super(SaleOrderLine,self)._prepare_order_line_procurement()
		self.ensure_one()
		rec.update({
	           'name': self.name,
	           'origin': self.order_id.name,
	           'date_planned': datetime.strptime(self.order_id.date_order, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(days=self.customer_lead),
	           'product_id': self.product_id.id,
	           'product_qty': self.product_uom_qty,
	           'product_uom': self.product_uom.id,
	           'company_id': self.order_id.company_id.id,
	           'group_id': group_id,
	           'sale_line_id': self.id,
	           'batch_id': self.batch_id.id,
	       })
		return rec


class ProcurementOrder(models.Model):
	_inherit = 'procurement.order'

	sale_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', copy=False)
	batch_id = fields.Many2one('stock.picking.batch', string="Lote")

	def _get_stock_move_values(self):
		rec = super(ProcurementOrder,self)._get_stock_move_values()
		group_id = False
		if self.rule_id.group_propagation_option == 'propagate':
			group_id = self.group_id.id
		elif self.rule_id.group_propagation_option == 'fixed':
			group_id = self.rule_id.group_id.id
		date_expected = (datetime.strptime(self.date_planned, DEFAULT_SERVER_DATETIME_FORMAT) - relativedelta(
				days=self.rule_id.delay or 0)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
		qty_done = sum(self.move_ids.filtered(lambda move: move.state == 'done').mapped('product_uom_qty'))
		qty_left = max(self.product_qty - qty_done, 0)
		rec.update({
			'name': self.name[:2000],
			'company_id': self.rule_id.company_id.id or self.rule_id.location_src_id.company_id.id or self.rule_id.location_id.company_id.id or self.company_id.id,
			'product_id': self.product_id.id,
			'product_uom': self.product_uom.id,
			'product_uom_qty': qty_left,
			'partner_id': self.rule_id.partner_address_id.id or (self.group_id and self.group_id.partner_id.id) or False,
			'location_id': self.rule_id.location_src_id.id,
			'location_dest_id': self.location_id.id,
			'move_dest_id': self.move_dest_id and self.move_dest_id.id or False,
			'procurement_id': self.id,
			'rule_id': self.rule_id.id,
			'procure_method': self.rule_id.procure_method,
			'origin': self.origin,
			'picking_type_id': self.rule_id.picking_type_id.id,
			'group_id': group_id,
			'route_ids': [(4, route.id) for route in self.route_ids],
			'warehouse_id': self.rule_id.propagate_warehouse_id.id or self.rule_id.warehouse_id.id,
			'date': date_expected,
			'date_expected': date_expected,
			'propagate': self.rule_id.propagate,
			'priority': self.priority,
			'batch_id' : self.batch_id.id
		})
		return rec