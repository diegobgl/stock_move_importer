from odoo import models, fields, api

class StockPickingImport(models.TransientModel):
    _name = 'stock.picking.import'
    _description = 'Stock Picking Import'

    file = fields.Binary('File', required=True)
    filename = fields.Char('File Name')
