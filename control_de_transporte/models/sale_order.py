from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    transport_control_ids = fields.One2many(
        'transport.control',
        'sale_order_id',
        string='Controles de Transporte'
    )

    transport_control_count = fields.Integer(
        string='Controles de Transporte',
        compute='_compute_transport_control_count'
    )

    @api.depends('transport_control_ids')
    def _compute_transport_control_count(self):
        for order in self:
            order.transport_control_count = len(order.transport_control_ids)

    def action_view_transport_controls(self):
        self.ensure_one()
        action = self.env.ref('control_de_transporte.action_transport_control')

        action_domain = [('sale_order_id', '=', self.id)]
        action.context = {'default_sale_order_id': self.id}
        action.domain = action_domain

        return action.read()[0]
