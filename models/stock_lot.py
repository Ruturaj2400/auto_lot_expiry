from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_assign(self, *args, **kwargs):
        res = super(StockMove, self)._action_assign(*args, **kwargs) 
        for move in self:
            if move.product_id.tracking == 'lot' and move.origin:
                for line in move.move_line_ids:
                    if not line.lot_id:
                        lot = self.env['stock.lot'].search([
                            ('name', '=', move.origin),
                            ('product_id', '=', move.product_id.id),
                            ('company_id', '=', move.company_id.id)
                        ], limit=1)
                        if not lot:
                            lot = self.env['stock.lot'].create({
                                'name': move.origin,
                                'product_id': move.product_id.id,
                                'company_id': move.company_id.id,
                            })
                        line.lot_id = lot.id
                        line.lot_name = move.origin
        return res
class StockLot(models.Model):
    _inherit = 'stock.lot'

    def _cron_send_expiry_notifications(self):
        user_id = int(self.env['ir.config_parameter'].sudo().get_param('expiry_notification_user_id') or self.env.ref('base.user_admin').id)
        user_record = self.env['res.users'].browse(user_id)
        rules = {
            'long': [365, 30, 15, 7],
            'short': [2, 1, 0]
        }
        lots = self.search([('expiration_date', '!=', False)])
        today = fields.Date.today()

        for lot in lots:
            term = lot.product_id.duration_type
            if not term:
                continue
            
            days_list = rules.get(term, [])
            for days in days_list:
                expiry_date = fields.Date.to_date(lot.expiration_date)
                trigger_date = expiry_date - timedelta(days=days)
                
                if trigger_date == today:
                    summary = f"Expiry Alert: {lot.name} (Due in {days} days)"
                    existing = self.env['mail.activity'].search([
                        ('res_id', '=', lot.id),
                        ('res_model_id', '=', self.env.ref('stock.model_stock_lot').id),
                        ('summary', '=', summary),
                        ('date_deadline', '=', today)
                    ])
                    
                    if not existing:
                        self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('product_expiry.mail_activity_type_alert_date_reached').id,
                            'res_model_id': self.env.ref('stock.model_stock_lot').id,
                            'res_id': lot.id,
                            'user_id': user_id,
                            'summary': summary,
                            'note': f"Alert: Product {lot.product_id.name} expires in {days} days.",
                            'date_deadline': today,
                        })
                        
                        recipient_email = user_record.email or user_record.partner_id.email
                        if recipient_email:
                            self.env['mail.mail'].sudo().create({
                                'subject': f"Expiry Alert: {lot.name}",
                                'body_html': f"""
                                    <p>Hello,</p>
                                    <p>Product <strong>{lot.product_id.name}</strong> (Lot: {lot.name}) expires in {days} days.</p>
                                    <p>Expiry Date: {lot.expiration_date}</p>
                                    <p>Please take action.</p>
                                """,
                                'email_from': self.env.company.email or 'noreply@example.com',
                                'email_to': recipient_email,
                                'auto_delete': False,
                            }).send()