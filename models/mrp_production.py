from odoo import models, fields, api

class MrpProduction(models.Model):
	_inherit = 'mrp.production'

	name = fields.Char()
	move_ids = fields.One2many('mrp.production.stock.move', 'name', string="Movimientos Productos")
	account_move_ids = fields.One2many('mrp.production.account.move', 'name', string="Movimientos Cuenta")

	def movimientos(self):
		self._suma_movimientos()

	@api.multi
	def _suma_movimientos(self):
		self._query_productos()
		self._query_cuentas()

	def _query_productos(self):
		query_producto="""Select aml.product_id, round(sm.product_uom_qty,6) as qty, round(sum(aml.debit),2) as debit, round(sum(aml.credit),2) as credit
						from mrp_production mp
						inner join stock_move sm ON sm.raw_material_production_id = mp.id or sm.production_id = mp.id
						inner join account_move_line aml ON aml.stock_move_id = sm.id
						where mp.name in (%s)
						group by aml.product_id, sm.product_uom_qty"""
		params = [self.name]
		self.env.cr.execute(query_producto, tuple(params))
		res = self.env.cr.dictfetchall()

		self.move_ids = False
		sumatoria = []
		for r in res:
			sumatoria.append((0,0,r))
		self.move_ids = sumatoria

	def _query_cuentas(self):
		query_cuenta="""Select aml.account_id as account, round(sum(aml.debit),2) as debit, round(sum(aml.credit),2) as credit
						from mrp_production mp
						inner join stock_move sm ON sm.raw_material_production_id = mp.id or sm.production_id = mp.id
						inner join account_move_line aml ON aml.stock_move_id = sm.id
						where mp.name in (%s)
						group by aml.account_id"""
		params = [self.name]
		self.env.cr.execute(query_cuenta, tuple(params))
		res = self.env.cr.dictfetchall()
		self.account_move_ids = False
		sumatoria = []
		for r in res:
			sumatoria.append((0,0,r))
		self.account_move_ids = sumatoria

class MrpProductionAccountMove(models.Model):
	_name = 'mrp.production.account.move'

	name = fields.Many2one('mrp.production', string="Produccion ID")
	debit = fields.Float('Debito')
	credit = fields.Float('Credito')
	account = fields.Many2one('account.account', string="Cuenta")

class MrpProductionStockMove(models.Model):
	_name = 'mrp.production.stock.move'

	name = fields.Many2one('mrp.production', string="Produccion ID")
	product_id = fields.Many2one('product.product', string="Producto")
	qty = fields.Float(string="Cantidad")
	debit = fields.Float('Debito')
	credit = fields.Float('Credito')

		





#SQL
# select concat(aa.code, ' ',aa.name), sum(aml.debit), sum(aml.credit)
# from account_move_line aml
# inner join account_account aa ON aa.id = aml.account_id
# where aml.name = 'MO/013394'
# group by aa.code, aa.name