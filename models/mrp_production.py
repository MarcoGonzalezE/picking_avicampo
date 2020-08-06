from odoo import models, fields, api

class MrpProduction(models.Model):
	_inherit = 'mrp.production'

	name = fields.Char()

	@api.multi
	def _suma_movimientos(self):
		movimientos = self.env['account.move.line'].search([('name','=', self.name)])
		a = 0
		suma = 0
		for m in movimientos:
			if m.account_id[a] == m.account_id[a+1]:
				suma = + m.debit
		return suma





#SQL
# select concat(aa.code, ' ',aa.name), sum(aml.debit), sum(aml.credit)
# from account_move_line aml
# inner join account_account aa ON aa.id = aml.account_id
# where aml.name = 'MO/013394'
# group by aa.code, aa.name