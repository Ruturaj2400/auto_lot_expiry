from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Ye field settings page par dikhegi
    expiry_notification_user_id = fields.Many2one(
        'res.users',
        string="Expiry Notification User",
        config_parameter='expiry_notification_user_id', # Yahi key database mein save hogi
        help="Select the user who will receive the expiry notifications."
    )