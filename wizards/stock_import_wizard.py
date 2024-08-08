import base64
import xlrd
from odoo import models, fields, api
from odoo.exceptions import UserError

class StockImportWizard(models.TransientModel):
    _name = 'stock.import.wizard'
    _description = 'Stock Import Wizard'

    file = fields.Binary('File', required=True)
    filename = fields.Char('File Name')

    def import_file(self):
        if not self.file:
            raise UserError("Please upload a file.")

        file_data = base64.b64decode(self.file)
        book = xlrd.open_workbook(file_contents=file_data)
        sheet = book.sheet_by_index(0)

        priority_map = {
            'Low': '0',
            'Normal': '1',
            'High': '2'
        }

        for rowx in range(3, sheet.nrows):  # Comienza desde la fila 4
            row = sheet.row(rowx)
            
            picking_data = {
                'partner_id': self._get_partner_id(row[2].value),
                'scheduled_date': row[8].value,
                'location_id': self._get_location_id(row[13].value),
                'location_dest_id': self._get_location_id(row[12].value),
                'picking_type_id': self._get_picking_type_id(row[11].value),
                'origin': row[5].value,
                'priority': priority_map.get(row[9].value, '1'),  # Convertir prioridad
            }
            picking = self.env['stock.picking'].create(picking_data)

            move_data = {
                'product_id': self._get_product_id(row[11].value),
                'product_uom_qty': float(row[14].value),
                'product_uom': self._get_uom_id(row[11].value),
                'picking_id': picking.id,
                'location_id': self._get_location_id(row[13].value),
                'location_dest_id': self._get_location_id(row[12].value),
                'name': row[10].value,
            }
            self.env['stock.move'].create(move_data)

    def _get_partner_id(self, name):
        partner = self.env['res.partner'].search([('name', '=', name)], limit=1)
        if not partner:
            partner = self.env['res.partner'].create({'name': name})
        return partner.id

    def _get_location_id(self, name):
        location = self.env['stock.location'].search([('name', '=', name)], limit=1)
        if not location:
            location = self.env['stock.location'].create({'name': name})
        return location.id

    def _get_picking_type_id(self, code):
        picking_type = self.env['stock.picking.type'].search([('code', '=', code)], limit=1)
        if not picking_type:
            picking_type = self.env['stock.picking.type'].create({'code': code, 'name': code})
        return picking_type.id

    def _get_product_id(self, name):
        product = self.env['product.product'].search([('name', '=', name)], limit=1)
        if not product:
            product = self.env['product.product'].create({'name': name})
        return product.id

    def _get_uom_id(self, name):
        uom = self.env['uom.uom'].search([('name', '=', name)], limit=1)
        if not uom:
            uom = self.env['uom.uom'].create({'name': name})
        return uom.id
