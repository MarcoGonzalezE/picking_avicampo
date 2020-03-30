# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class AccountMoveLine(models.Model):
#     _inherit = "account.move.line"

#     batch_id = fields.Many2one(comodel_name='stock.picking.batch', string="Lote")

    # @api.multi
    # @api.depends()

# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'

#     @api.multi
#     def _prepare_stock_moves(self.):
#         rec = super(PurchaseOrderLine,self)._prepare_stock_moves()
#         template = {
#             'batch_id' : self.batch_id.id,
#         }