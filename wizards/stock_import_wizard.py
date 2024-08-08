import base64
import xlrd
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

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

        for rowx in range(1, sheet.nrows):  # Comienza desde la fila 2
            row = sheet.row(rowx)
            
            # Convertir la fecha a cadena en el formato esperado
            if isinstance(row[2].value, float):
                date_value = xlrd.xldate_as_datetime(row[2].value, book.datemode)
                scheduled_date = date_value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                scheduled_date = row[2].value

            picking_type_id = self._get_picking_type_id('internal')  # Obtener el picking_type_id adecuado, aquí se asume 'internal'

            picking_data = {
                'location_id': self._get_location_id(row[0].value),
                'location_dest_id': self._get_location_id(row[1].value),
                'scheduled_date': scheduled_date,
                'origin': row[10].value,
                'priority': '1',  # Asumiendo prioridad normal si no hay campo en el Excel
                'picking_type_id': picking_type_id,
            }
            picking = self.env['stock.picking'].create(picking_data)
            
            move_data = {
                'product_id': self._get_product_id(row[3].value),
                'product_uom_qty': float(row[13].value),
                'product_uom': self._get_uom_id(row[4].value),
                'picking_id': picking.id,
                'location_id': self._get_location_id(row[0].value),
                'location_dest_id': self._get_location_id(row[1].value),
                'name': row[3].value,
            }
            self.env['stock.move'].create(move_data)

    def _get_location_id(self, name):
        location = self.env['stock.location'].search([('name', '=', name)], limit=1)
        if not location:
            location = self.env['stock.location'].create({'name': name})
        return location.id

    def _get_product_id(self, name):
        product_code = name.split('] ')[1].split(' ')[0]
        product = self.env['product.product'].search([('default_code', '=', product_code)], limit=1)
        if not product:
            product = self.env['product.product'].create({'name': name})
        return product.id

    def _get_uom_id(self, name):
        uom = self.env['uom.uom'].search([('name', '=', name)], limit=1)
        if not uom:
            uom = self.env['uom.uom'].create({'name': name})
        return uom.id

    def _get_picking_type_id(self, code):
        picking_type = self.env['stock.picking.type'].search([('code', '=', code)], limit=1)
        if not picking_type:
            picking_type = self.env['stock.picking.type'].create({'code': code, 'name': code})
        return picking_type.id
