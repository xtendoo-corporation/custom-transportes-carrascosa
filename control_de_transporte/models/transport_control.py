from odoo import api, models, fields
from datetime import datetime, timedelta
from odoo import _
import qrcode
import base64
import io


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
    qr_code = fields.Binary(
        string="Código QR",
        readonly=True
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

    def action_send_report_email(self):
        self.ensure_one()

        template = self.env.ref('control_de_transporte.email_template_transport_control', False)
        if not template:
            raise ValueError("La plantilla de correo no existe")

        compose_form = self.env.ref("mail.email_compose_message_wizard_form", False)
        ctx = dict(
            default_model="transport.control",
            default_res_ids=[self.id],
            default_use_template=bool(template),
            default_template_id=template.id if template else False,
            default_composition_mode="comment",
            user_id=self.env.user.id,
        )

        return {
            "name": _("Enviar Correo Electrónico"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

    def _get_pdf_report(self):
        report_action = self.env.ref('control_de_transporte.action_transport_control_report')
        pdf, _ = report_action.sudo()._render_qweb_pdf([self.id])
        return pdf

    def action_view_report_pdf(self):
        self.ensure_one()
        report_url = self.get_report_url()
        self.generate_qr_code(report_url)
        return {
            'type': 'ir.actions.act_url',
            'url': report_url,
            'target': 'new',
        }

    def get_report_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        report_name = 'control_de_transporte.report_transport_control_template'
        return f"{base_url}/report/pdf/{report_name}/{self.id}"

    def generate_qr_code(self, data):
        """Genera un código QR y lo almacena en el campo qr_code."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        self.qr_code = base64.b64encode(img_byte_arr.read())

    @api.model
    def create(self, vals):
        record = super(TransportControl, self).create(vals)
        report_url = record.get_report_url()
        record.generate_qr_code(report_url)
        return record

    @api.onchange(
        'sale_order_id', 'empresa_cargadora', 'conductor', 'matricula_vehiculo',
        'matricula_semirremolque', 'empresa_expedidora', 'operador_transporte',
        'empresa_destinataria', 'reservas_y_observaciones', 'lugar_carga',
        'hora_llegada_carga', 'hora_salida_carga', 'lugar_entrega',
        'hora_llegada_entrega', 'hora_salida_entrega', 'descripcion_mercancia',
        'peso', 'km_llegada', 'km_salida', 'hora_firma_remitente',
        'hora_firma_destinatario', 'firma_remitente', 'dni_remitente',
        'nombre_remitente', 'firma_destinatario', 'dni_destinatario',
        'nombre_destinatario', 'firma_transportista', 'dni_transportista',
        'nombre_transportista'
    )
    def _onchange_fields_update(self):
        for record in self:
            report_url = record.get_report_url()
            record.generate_qr_code(report_url)

