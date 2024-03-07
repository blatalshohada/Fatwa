from odoo import models, fields, api
import re
from datetime import date, datetime
from datetime import timedelta
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

def clean_html(raw_html):
    """
    Utility function to clean text of HTML tags.
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


class MessageCronJob(models.Model):
    _name = 'message.cron.job'
    
    @api.model
    def check_new_messages(self):
        _logger.info('Running check_new_messages cron job...')
        message_records = self.env['mail.message'].search([('date', '>=', fields.Datetime.to_string(fields.Datetime.now() - timedelta(minutes=5)))])

        for record in message_records:

            email_body = record.body

            if isinstance(email_body, bytes):
                email_body = email_body.decode('utf-8')  # or another appropriate encoding

            if not isinstance(email_body, str):
                email_body = str(email_body)


            # Define the regular expression pattern for user name
            pattern = r'اسم المستخدم: (.+?)(?=\nاسم المستخدم:|$)'

            # Search for the pattern in the Arabic text
            match = re.search(pattern, email_body, re.MULTILINE)

            partner_name = ''
            if match:
                partner_name = match.group(1)
                print("user name ------------->", partner_name)
            else:
                print("Pattern not found in the text.")


            # Define the regular expression pattern email
            pattern2 = r'البريد الإلكتروني للمستخدم: (.+?)(?=\nالبريد الإلكتروني للمستخدم:|$)'

            # Search for the pattern in the Arabic text
            match2 = re.search(pattern2, email_body, re.MULTILINE)

            partner_email = ''
            if match2:
                partner_email = match2.group(1)
                print("email--------------->", partner_email)
            else:
                print("Pattern not found in the text.")

            partner_name = clean_html(partner_name)
            partner_email = clean_html(partner_email)
            # Now create a new res.partner record
            partner_vals = {
                'name': partner_name,
                'email': partner_email,
                # Add other necessary fields
            }

            partner = self.env['res.partner'].search([('email', '=', partner_email)], limit=1)
            ticket = self.env['helpdesk.ticket'].browse(record.res_id)
            if ticket.exists():
                if not partner:
                    partner = self.env['res.partner'].create(partner_vals)
                    ticket.partner_id = partner.id
                    ticket.partner_email = partner.email
                else:
                    ticket.partner_id = partner.id
                    ticket.partner_email = partner.email


        return True
        