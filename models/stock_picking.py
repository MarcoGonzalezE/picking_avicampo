# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Picking(models.Model):
    _inherit = 'stock.picking'
	
    farm_id = fields.Many2one(comodel_name='stock.picking.farm', string='Granja')
    batch_id = fields.Many2one(comodel_name='stock.picking.batch', string="Lote")
    operator_id = fields.Many2one(comodel_name='stock.picking.operator', string="Operador")
    sello = fields.Char(string="Sello", translate=True)
    ticket = fields.Char(string="Ticket",translate=True)
    date_trans = fields.Datetime(string="Fecha Salida", translate=True)
    date_delivery = fields.Datetime(string="Fecha Entrega",translate=True)
    folio = fields.Char(string="Folio", translate=True)


class PickingMove(models.Model):
    _inherit = 'stock.move'

    batch_id = fields.Many2one(comodel_name='stock.picking.batch', string="Lote")
    procurement_id = fields.Many2one()

    @api.model
    def _prepare_account_move_line(self, qty, cost,credit_account_id, debit_account_id):
        res = super(PickingMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
        for line in res:
            line[2]['batch_id'] = self.batch_id.id
        return res