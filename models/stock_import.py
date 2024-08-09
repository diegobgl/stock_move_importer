from odoo import models, fields, api

class StockPickingImport(models.TransientModel):
    _name = 'stock.picking.import'
    _description = 'Stock Picking Import'

    file = fields.Binary('File', required=True)
    filename = fields.Char('File Name')



# class StockPicking(models.Model):
#     _inherit = 'stock.picking'

#     def button_validate(self):
#         res = super(StockPicking, self).button_validate()
#         self.ensure_account_moves()
#         return res

#     def ensure_account_moves(self):
#         # Ajusta 'move_lines' si tiene un nombre diferente en tu modelo
#         move_lines_field = 'move_lines'  # Cambia esto si es necesario

#         if not hasattr(self, move_lines_field):
#             raise UserError(f"El modelo stock.picking no tiene el campo '{move_lines_field}'. Verifica el nombre del campo.")

#         for picking in self:
#             moves = getattr(picking, move_lines_field).filtered(lambda m: m.state == 'done')
#             if moves:
#                 self.create_account_move(moves)

#     def create_account_move(self, moves):
#         for move in moves:
#             if not move.account_move_ids:
#                 move._create_account_move_line()
