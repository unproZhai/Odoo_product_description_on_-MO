# -*- coding: utf-8 -*-


from odoo import api
from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_line = fields.One2many('sale.order.line', 'order_id', 'Order Lines')
    product_description = fields.Char(string="Product Description",compute="compute_sale_order")

    @api.multi
    def compute_sale_order(self):
        mto_route = self.env.ref('stock.route_warehouse0_mto')
        for production in self:
            line = self.find_line_id(production)
            if line:
                production.sale_line = line
                production.product_description = line.name
            # if production.move_dest_ids:
            #     move_dest_ids = production.move_dest_ids
            #     if move_dest_ids.move_dest_ids:
            #         delivery_id = move_dest_ids.move_dest_ids
            #         if delivery_id.move_dest_ids:
            #             picking_id=delivery_id.move_dest_ids
            #             # production.sale_order_line_id=picking_id.sale_line_id.id
            #             # production.product_description=picking_id.sale_line_id.display_name
                # else:
                #     production.sale_order_line_id = move_dest_ids.sale_line_id.id
                #     production.product_description = move_dest_ids.name

    @api.multi
    def find_line_id(self, production):
        if not production:
            return False
        if production.move_dest_ids.sale_line_id:
            return production.move_dest_ids.sale_line_id
        return self.find_line_id(production.move_dest_ids)

    
