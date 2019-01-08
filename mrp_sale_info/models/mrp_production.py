# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2018 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale Line',
        related='move_prod_procurement_id.sale_line_id')
    move_prod_procurement_id = fields.Many2one(
        comodel_name='procurement.order', compute='_compute_move_prod_procurement_id', store=True
    )
    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order',
        readonly=True, store=True,
        compute='_compute_sale_id')
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Customer',
        store=True,
        related='sale_id.partner_id')
    commitment_date = fields.Datetime(
        related='sale_id.commitment_date',
        string='Commitment Date', store=True)

    @api.multi
    @api.depends('move_prod_procurement_id.sale_line_id')
    def _compute_sale_id(self):
        for record in self:
            if record.move_prod_procurement_id and record.move_prod_procurement_id.sale_line_id:
                record.sale_id = record.move_prod_procurement_id.sale_line_id.order_id.id
            else:
                record.sale_id = False

    @api.multi
    @api.depends('move_prod_id')
    def _compute_move_prod_procurement_id(self):
        def get_parent_move(move_obj):
            if move_obj.move_dest_id:
                return get_parent_move(move_obj.move_dest_id)
            return move_obj

        for record in self:
            if record.move_prod_id:
                parent_move_obj = get_parent_move(record.move_prod_id)
                if parent_move_obj and parent_move_obj.procurement_id and parent_move_obj.procurement_id:
                    record.move_prod_procurement_id = parent_move_obj.procurement_id.id
