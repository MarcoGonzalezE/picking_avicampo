# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Picking(models.Model):
    _inherit = 'stock.picking'
	
	#def _get_order_farm(self):
     #   return self.env['stock.picking.farm'].search([], limit=1)

    farm_id = fields.Many2one(comodel_name='stock.picking.farm', string='Granja')
	
	#def _get_picking_batch(self):
    #    return self.env['stock.picking.batch'].search([], limit=1)

    batch_id = fields.Many2one(comodel_name='stock.picking.batch', string="Lote")
	
	#def _get_picking_operator(self):
    #    return self.env['stock.picking.operator'].search([], limit=1)

    operator_id = fields.Many2one(comodel_name='stock.picking.operator', string="Operador") 

    sello = fields.Char(string="Sello", translate=True)
    ticket = fields.Char(string="Ticket",translate=True)
    date_trans = fields.Datetime(string="Fecha Salida", translate=True)
    date_delivery = fields.Datetime(string="Fecha Entrega",translate=True)
    folio = fields.Char(string="Folio", translate=True)

    # @api.multi
    # @api.depends('move_lines')
    # def _batch_stock_move(self):
    #     for move in self.move_lines:
    #         sale = self.env['sale.order'].search([('name','=', move.origin)])
    #         print(sale.name)
    #         #sale_line = self.env['sale.order.line'].search([('order_id','=',sale.id),('product_id','=', self.product_id),('product_uom_qty','=', self.product_uom_qty)])
    #         for x in sale:
    #             sale_line = self.env['sale.order.line'].search([('order_id', '=', x.id)])
    #             print(sale_line.batch_id.name)
    #             if sale_line.batch_id.name != 'NA':
    #                 if sale_line.product_id == move.product_id and sale_line.product_uom_qty == move.product_uom_qty:
    #                     move.batch_id = sale_line.batch_id


class PickingMove(models.Model):
    _inherit = 'stock.move'

    batch_id = fields.Many2one(comodel_name='stock.picking.batch', string="Lote")
    #batch_id = fields.Many2one(comodel_name='stock.picking.batch', string="Lote", compute="_batch_sale")
    procurement_id = fields.Many2one()

    # @api.multi
    # @api.depends('procurement_id')
    # def _batch_procurement(self):
    #     if self.procurement_id:
    #         self.batch_id = self.procurement_id.sale_line_id.batch_id

    # @api.multi
    # @api.depends('origin','product_id')
    # def _batch_sale(self):
    #     # picking = self.env['stock.picking'].search([('id', '=', self.picking_id)])
    #     # print(picking.name)
    #     for r in self:
    #         if r.origin.find('SO') == -1:
    #             print('ENTRO A COMPRAS')
    #         else:
    #             sale = self.env['sale.order'].search([('name','=', r.origin)])
    #             print(sale.name)
    #             #sale_line = self.env['sale.order.line'].search([('order_id','=',sale.id),('product_id','=', self.product_id),('product_uom_qty','=', self.product_uom_qty)])
    #             for x in sale:
    #                 sale_line = self.env['sale.order.line'].search([('order_id', '=', x.id)])
    #                 for line in sale_line:
    #                     if line.batch_id.name != 'NA':
    #                         if line.product_id == r.product_id and line.product_uom_qty == r.product_uom_qty and line.warehouse_id == r.warehouse_id:
    #                             r.batch_id = line.batch_id


    # def _prepare_procurement_from_move(self):
    #     rec = super(PickingMove,self)._prepare_procurement_from_move()
    #     for rec in self:
    #         origin = (self.group_id and (self.group_id.name + ":") or "") + (self.rule_id and self.rule_id.name or self.origin or self.picking_id.name or "/")
    #         group_id = self.group_id and self.group_id.id or False
    #         if self.rule_id:
    #             if self.rule_id.group_propagation_option == 'fixed' and self.rule_id.group_id:
    #                 group_id = self.rule_id.group_id.id
    #             elif self.rule_id.group_propagation_option == 'none':
    #                 group_id = False
    #         return {
    #             'name': self.rule_id and self.rule_id.name or "/",
    #             'origin': origin,
    #             'company_id': self.company_id.id,
    #             'date_planned': self.date_expected,
    #             'product_id': self.product_id.id,
    #             'product_qty': self.product_uom_qty,
    #             'product_uom': self.product_uom.id,
    #             'location_id': self.location_id.id,
    #             'move_dest_id': self.id,
    #             'group_id': group_id,
    #             'route_ids': [(4, x.id) for x in self.route_ids],
    #             'warehouse_id': self.warehouse_id.id or (self.picking_type_id and self.picking_type_id.warehouse_id.id or False),
    #             'priority': self.priority,
    #             'batch_id': self.batch_id,
    #         }