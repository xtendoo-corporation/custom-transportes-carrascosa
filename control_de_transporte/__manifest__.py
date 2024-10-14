{
    "name": "Control de Transporte Sale Order",
    "summary": "Extensión del pedido de venta",
    "version": "17.0.1.0.0",
    "description": "Extensión del pedido de venta Carrascosa",
    "company": "Xtendoo",
    "website": "http://www.xtendoo.es",
    "category": "Sales",
    "depends": ["sale","mail"],
    "license": "AGPL-3",
    "data": [
        "views/sale_order.xml",
        "views/transport_control.xml",
        "security/ir.model.access.csv",
        'reports/transport_control_report.xml',
        "data/mail_template_data.xml"
    ],
    "installable": True,
}
