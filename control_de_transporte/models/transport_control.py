from odoo import api, models, fields
from datetime import datetime, timedelta

class TransportControl(models.Model):
    _name = 'transport.control'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Pedido de Venta',
        required=True,
    )

    empresa_cargadora = fields.Many2one(
        'res.partner',
        string='Empresa Cargadora',
        domain=[('is_company', '=', True)],
        tracking=True
    )
    conductor = fields.Many2one(
        'res.partner',
        string='Conductor',
        domain=[('is_company', '=', False)],
        tracking=True
    )
    matricula_vehiculo = fields.Char(
        string='Matrícula Vehículo',
        tracking=True
    )
    matricula_semirremolque = fields.Char(
        string='Matrícula Semirremolque',
        tracking=True
    )
    empresa_expedidora = fields.Many2one(
        'res.partner',
        string='Empresa Expedidora',
        domain=[('is_company', '=', True)],
        tracking=True
    )
    operador_transporte = fields.Many2one(
        'res.partner',
        string='Operador de transporte',
        domain=[('is_company', '=', False)],
        tracking=True
    )
    empresa_destinataria = fields.Many2one(
        'res.partner',
        string='Empresa Destinataria',
        domain=[('is_company', '=', True)],
        tracking=True
    )
    reservas_y_observaciones = fields.Char(
        string="Reservas y observaciones",
        tracking=True
    )
    lugar_carga = fields.Char(
        string='Lugar de Carga',
        tracking=True
    )
    hora_llegada_carga = fields.Datetime(
        string='Hora de Llegada',
        tracking=True
    )
    hora_salida_carga = fields.Datetime(
        string='Hora de Salida',
        tracking=True
    )
    lugar_entrega = fields.Char(
        string='Lugar de Entrega',
        tracking=True
    )
    hora_llegada_entrega = fields.Datetime(
        string='Hora de Llegada',
        tracking=True
    )
    hora_salida_entrega = fields.Datetime(
        string='Hora de Salida',
        tracking=True
    )
    descripcion_mercancia = fields.Char(
        string="Descripción",
        tracking=True
    )
    peso = fields.Integer(
        string="Peso aproximado (Tns.)",
        tracking=True
    )
    km_llegada = fields.Float(
        string="Km. LLegada",
        tracking=True
    )
    km_salida = fields.Float(
        string="Km. Salida",
        tracking=True
    )
    km_total = fields.Float(
        string="Total km",
        compute='_compute_km_total',
        store=True,
    )
    hora_firma_remitente = fields.Datetime(
        string='Hora de Firma del Remitente',
        tracking=True
    )
    hora_firma_destinatario = fields.Datetime(
        string='Hora de Firma del Destinatario',
        tracking=True
    )
    firma_remitente = fields.Binary(
        'Firma del Remitente',
    )
    dni_remitente = fields.Char(
        "DNI del Remitente",
        tracking=True
    )
    nombre_remitente = fields.Char(
        "Nombre del Remitente",
        tracking=True
    )
    firma_destinatario = fields.Binary(
        'Firma del Destinatario',
    )
    dni_destinatario = fields.Char(
        "DNI del Destinatario",
        tracking=True
    )
    nombre_destinatario = fields.Char(
        "Nombre del Destinatario",
        tracking=True
    )
    firma_transportista = fields.Binary(
        'Firma del Transportista',
    )
    dni_transportista = fields.Char(
        "DNI del Transportista",
        tracking=True
    )
    nombre_transportista = fields.Char(
        "Nombre del Transportista",
        tracking=True
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



