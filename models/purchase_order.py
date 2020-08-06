# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero, float_compare


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

    # @api.multi
    # def _prepare_stock_moves(self, picking):
    #     rec = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
    #     res = []
    #     for r in rec:
    #         if self.batch == True:
    #             tmp = template.copy()
    #             tmp.update({
    #                 'picking_id': picking.id,
    #                 'batch_id': self.batch.id,
    #             })
    #             res.append(tmp)
    #     return res

    @api.multi
    def _prepare_stock_moves(self, picking):
        rec = super(PurchaseOrderLine,self)._prepare_stock_moves(picking)
        for rec in self:
            self.ensure_one()
            res = []
            if self.product_id.type not in ['product','consu']:
                return res
            qty = 0.0
            price_unit = self._get_stock_move_price_unit()
            for move in self.move_ids.filtered(lambda x: x.state != 'cancel'):
                qty += move.product_qty
            template = {
                'name': self.name or '',
                'product_id': self.product_id.id,
                'product_uom': self.product_uom.id,
                'date': self.order_id.date_order,
                'date_expected': self.date_planned,
                'location_id': self.order_id.partner_id.property_stock_supplier.id,
                'location_dest_id': self.order_id._get_destination_location(),
                'picking_id': picking.id,
                'partner_id': self.order_id.dest_address_id.id,
                'move_dest_id': False,
                'state': 'draft',
                'purchase_line_id': self.id,
                'company_id': self.order_id.company_id.id,
                'price_unit': price_unit,
                'picking_type_id': self.order_id.picking_type_id.id,
                'group_id': self.order_id.group_id.id,
                'procurement_id': False,
                'origin': self.order_id.name,
                'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
                'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
                'batch_id': self.batch.id,
                'fleet_id': self.fleet.id,
            }
            diff_quantity = self.product_qty - qty
            for procurement in self.procurement_ids.filtered(lambda p: p.state != 'cancel'):
                sum_existing_moves = sum(x.product_qty for x in procurement.move_ids if x.state != 'cancel')
                existing_proc_qty = procurement.product_id.uom_id._compute_quantity(sum_existing_moves, procurement.product_uom)
                procurement_qty = procurement.product_uom._compute_quantity(procurement.product_qty, self.product_uom) - existing_proc_qty
                if float_compare(procurement_qty, 0.0, precision_rounding=procurement.product_uom.rounding) > 0 and float_compare(diff_quantity, 0.0, precision_rounding=self.product_uom.rounding) > 0:
                    tmp = template.copy()
                tmp.update({
                    'product_uom_qty': min(procurement_qty, diff_quantity),
                    'move_dest_id': procurement.move_dest_id.id,  # move destination is same as procurement destination
                    'procurement_id': procurement.id,
                    'propagate': procurement.rule_id.propagate,
                })
                res.append(tmp)
                diff_quantity -= min(procurement_qty, diff_quantity)
            if float_compare(diff_quantity, 0.0, precision_rounding=self.product_uom.rounding) > 0:
                template['product_uom_qty'] = diff_quantity
                res.append(template)
        return res