# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class AccountInvoiceLine(models.Model):
	_name = 'account.invoice.line'
	_inherit ='account.invoice.line'

	batch_id = fields.Many2one('stock.picking.batch', string="Lote")

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	purchase_id = fields.Many2one()

	def _prepare_invoice_line_from_po_line(self, line):
		rec = super(AccountInvoice,self)._prepare_invoice_line_from_po_line(line)
		for rec in self:
			if line.product_id.purchase_method == 'purchase':
				qty = line.product_qty - line.qty_invoiced
			else:
				qty = line.qty_received - line.qty_invoiced
			if float_compare(qty, 0.0, precision_rounding=line.product_uom.rounding) <= 0:
				qty = 0.0
			taxes = line.taxes_id
			invoice_line_tax_ids = line.order_id.fiscal_position_id.map_tax(taxes)
			invoice_line = self.env['account.invoice.line']
			data = {
	            'purchase_line_id': line.id,
	            'name': line.order_id.name+': '+line.name,
	            'origin': line.order_id.origin,
	            'batch_id': line.batch.id,
	            'uom_id': line.product_uom.id,
	            'product_id': line.product_id.id,
	            'account_id': invoice_line.with_context({'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
	            'price_unit': line.order_id.currency_id.with_context(date=self.date_invoice).compute(line.price_unit, self.currency_id, round=False),
	            'quantity': qty,
	            'discount': 0.0,
	            'account_analytic_id': line.account_analytic_id.id,
	            'analytic_tag_ids': line.analytic_tag_ids.ids,
	            'invoice_line_tax_ids': invoice_line_tax_ids.ids
	        }
			account = invoice_line.get_invoice_line_account('in_invoice', line.product_id, line.order_id.fiscal_position_id, self.env.user.company_id)
			if account:
				data['account_id'] = account.id
		return data


	#TODO: Envio de LOTE de lineas de factura al asiento contable
	#DETALLE: EL asiento contable de factura de proveedor hace una sumatoria del producto, por el cual no puede ser dirigido el lote al asiento.
	
	# @api.model
	# def invoice_line_move_line_get(self):
	# 	rec = super(AccountInvoice, self).invoice_line_move_line_get()
	# 	for rec in self:
	# 		res = []
	# 		for line in self.invoice_line_ids:
	# 			if line.quantity==0:
	# 				continue
	# 			tax_ids = []
	# 			for tax in line.invoice_line_tax_ids:
	# 				tax_ids.append((4, tax.id, None))
	# 				for child in tax.children_tax_ids:
	# 					if child.type_tax_use != 'none':
	# 						tax_ids.append((4, child.id, None))
	# 			analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

	# 			move_line_dict = {
	#                 'invl_id': line.id,
	#                 'type': 'src',
	#                 'name': line.name.split('\n')[0][:64],
	#                 'price_unit': line.price_unit,
	#                 'quantity': line.quantity,
	#                 'price': line.price_subtotal,
	#                 'account_id': line.account_id.id,
	#                 'product_id': line.product_id.id,
	# 				'batch_id': line.batch_id.id,
	#                 'uom_id': line.uom_id.id,
	#                 'account_analytic_id': line.account_analytic_id.id,
	#                 'tax_ids': tax_ids,
	#                 'invoice_id': self.id,
	#                 'analytic_tag_ids': analytic_tag_ids
	#             }
	# 			res.append(move_line_dict)
	# 		print(res)
	# 		return res