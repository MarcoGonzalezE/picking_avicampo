from odoo import models, fields, api

class MrpProduction(models.Model):
	_inherit = 'mrp.production'

	name = fields.Char()
	move_ids = fields.One2many('mrp.production.account.move', 'name', string="Movimientos")	

	def movimientos(self):
		self._suma_movimientos()

	@api.multi
	def _suma_movimientos(self):
		self.move_ids = False
		sumatoria = []
		move = self.env['stock.move'].search([('name','=',self.name)])
		print(move)
		for m in move:
			account = self.env['account.move.line'].search([('stock_move_id','=',m.id),('debit','>','0')])
			for a in account:
				sumatoria.append((0,0,{'product_id':a.product_id,'qty':a.quantity,'price_total':a.debit}))
				print(sumatoria)
		self.move_ids = sumatoria

		# movimientos = self.env['account.move.line'].search([('name','=', self.name)])
		# a = 0
		# suma = 0
		# for m in movimientos:
		# 	if m.account_id[a] == m.account_id[a+1]:
		# 		suma = + m.debit
		# return suma

class MrpProductionAccountMove(models.Model):
	_name = 'mrp.production.account.move'

	name = fields.Many2one('mrp.production', string="Produccion ID")
	product_id = fields.Many2one('product.product', string="Producto")
	qty = fields.Float(string="Cantidad")
	price_total = fields.Float('Precio')
		





#SQL
# select concat(aa.code, ' ',aa.name), sum(aml.debit), sum(aml.credit)
# from account_move_line aml
# inner join account_account aa ON aa.id = aml.account_id
# where aml.name = 'MO/013394'
# group by aa.code, aa.name