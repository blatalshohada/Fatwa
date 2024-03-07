from bidi.algorithm import get_display
import re

txt = """ سؤال من عبدالله الجابري
        السلام عليكم ورحمة الله وبركاته

        اسم المستخدم: عبدالله الجابري

        البريد الإلكتروني للمستخدم: yazed1388@gmail.com

        بلد المستخدم: السعودية

        سؤال المستخدم: الصلاة لمن يعاني من سلس البول ويصلى بكلوت حفائص ويجد فيها بول .

        عمومية السؤال: خاص """

display_text = get_display(txt)

print(display_text)

# Define the regular expression pattern email
pattern2 = r'اسم المستخدم: (.+?)(?=\nاسم المستخدم:|$)'

# Search for the pattern in the Arabic text
match2 = re.search(pattern2, txt, re.MULTILINE)

partner_email = ''
if match2:
        partner_email = match2.group(1)
        print("email--------------->", partner_email)
else:
        print("Pattern not found in the text.")



@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


from odoo import models, fields, api
import re
from odoo.exceptions import UserError

class MessageCronJob(models.Model):
    _name = 'message.cron.job'
    
    @api.model
    def check_new_messages(self):
        message_records = self.env['mail.message'].search([('create_date', '>=', fields.Datetime.to_string(fields.Datetime.now() - timedelta(minutes=5)))])
        
        for record in message_records:
            body = record.body
            username_match = re.search(r'اسم المستخدم: (.+)$', body, re.MULTILINE)
            email_match = re.search(r'البريد الإلكتروني للمستخدم: (.+)$', body, re.MULTILINE)
            
            if username_match and email_match:
                username = username_match.group(1).strip()
                email = email_match.group(1).strip()
                
                partner = self.env['res.partner'].search([('email', '=', email)], limit=1)
                if not partner:
                    partner = self.env['res.partner'].create({'name': username, 'email': email})
                else:
                    raise UserError('Partner with email %s already exists.' % email)
                    
        return True

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


from odoo import models, fields, api
import re

class CustomMailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):

        # Call the super method to create the mail.message record
        new_message = super(CustomMailMessage, self).create(vals)
  
        email_body = """ سؤال من عبدالله الجابري
                        السلام عليكم ورحمة الله وبركاته

                        اسم المستخدم: عبدالله الجابري

                        البريد الإلكتروني للمستخدم: yazed1388@gmail.com

                        بلد المستخدم: السعودية

                        سؤال المستخدم: الصلاة لمن يعاني من سلس البول ويصلى بكلوت حفائص ويجد فيها بول .

                        عمومية السؤال: خاص """            

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

        
        # Now create a new res.partner record
        partner_vals = {
            'name': partner_name,
            'email': partner_email,
            # Add other necessary fields
        }
        # self.env['res.partner'].create(partner_vals)
        
        # Return the new mail.message record
        return new_message


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

