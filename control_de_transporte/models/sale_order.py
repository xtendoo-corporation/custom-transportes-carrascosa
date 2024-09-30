from odoo import api, models, fields
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    empresa_cargadora = fields.Many2one(
        'res.partner',
        string='Empresa Cargadora',
        domain=[('is_company', '=', True)]
    )
    conductor = fields.Many2one(
        'res.partner',
        string='Conductor',
        domain=[('is_company', '=', False)]
    )
    matricula_vehiculo = fields.Char(
        string='Matrícula Vehículo'
    )
    matricula_semirremolque = fields.Char(
        string='Matrícula Semirremolque'
    )
    empresa_expedidora = fields.Many2one(
        'res.partner',
        string='Empresa Expedidora',
        domain=[('is_company', '=', True)]
    )
    operador_transporte = fields.Many2one(
        'res.partner',
        string='Operador de transporte',
        domain=[('is_company', '=', False)]
    )
    empresa_destinataria = fields.Many2one(
        'res.partner',
        string='Empresa Destinataria',
        domain=[('is_company', '=', True)]
    )
    reservas_y_observaciones = fields.Char(
        string="Reservas y observaciones"
    )
    lugar_carga = fields.Char(
        string='Lugar de Carga'
    )
    hora_llegada_carga = fields.Datetime(
        string='Hora de Llegada'
    )
    hora_salida_carga = fields.Datetime(
        string='Hora de Salida'
    )
    lugar_entrega= fields.Char(
        string='Lugar de Entrega'
    )
    hora_llegada_entrega = fields.Datetime(
        string='Hora de Llegada'
    )
    hora_salida_entrega = fields.Datetime(
        string='Hora de Salida'
    )
    descripcion_mercancia = fields.Char(
        string="Descripción"
    )
    peso = fields.Integer(
        string="Peso aproximado (Tns.)"
    )
    km_llegada = fields.Float(
        string="Km. LLegada"
    )
    km_salida = fields.Float(
        string="Km. Salida"
    )
    km_total = fields.Float(
        string="Total km",
        compute='_compute_km_total',
        store=True
    )
    hora_firma_remitente = fields.Datetime(
        string='Hora de Firma del Remitente'
    )
    hora_firma_destinatario = fields.Datetime(
        string='Hora de Firma del Destinatario'
    )
    firma_remitente = fields.Binary(
        'Firma del Remitente',
    )
    firma_destinatario = fields.Binary(
        'Firma del Destinatario',
    )
    firma_transportista = fields.Binary(
        'Firma del Transportista',
    )

    @api.depends('km_llegada', 'km_salida')
    def _compute_km_total(self):
        for order in self:
            order.km_total = order.km_llegada + order.km_salida

    @api.onchange('firma_remitente')
    def _onchange_firma_remitente(self):
        if self.firma_remitente:
            self.hora_firma_remitente = datetime.now()

    @api.onchange('firma_destinatario')
    def _onchange_firma_destinatario(self):
        if self.firma_destinatario:
            self.hora_firma_destinatario = datetime.now()

