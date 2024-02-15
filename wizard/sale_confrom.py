from odoo import api, fields, models


class SaleConfirmWizard(models.TransientModel):
    _name = 'sale.confirm.wizard'

    name = fields.Char(string='Warning')

    def sale_order_submit_button(self):
        context = self.env.context
        record = self.env['sale.order'].browse(context.get('active_id'))
        warning = {
            'name': 'warning',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.confirm.wizard',
            'view_id': self.env.ref('context_practice.sale_order_confirm_wizard_form_view').id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {}
        }
        if context.get('trust_not'):
            record.partner_id.untrustworthy = False
        if not record.opportunity_id:
            if context.get('context_opportunity'):
                warning['context'] = {'opportunity_id': True,
                                      'context_opportunity': False,
                                      'trust_not': False,
                                      'active_id': record.id,
                                      "amount_total": True,
                                      'total_amount': True}
                return warning
        if record.amount_total == float(0.0):
            if context.get('total_amount'):
                warning['context'] = {'trust_not': False,
                                      'active_id': record.id,
                                      "amount_total_msg": True,
                                      'amount_total': True,
                                      'opportunity_id': False,
                                      'total_amount': False}
                return warning

            else:
                print('hello')
                record.with_context({'opportunity': False, 'amount_total': False}).action_confirm()
        else:
            print('hello')
            record.with_context({'opportunity': False, 'amount_total': False}).action_confirm()

    @api.model
    def default_get(self, fields):
        context = self.env.context
        res = super(SaleConfirmWizard, self).default_get(fields)
        if context.get('trust_not'):
            res['name'] = '"This customer is untrustworthy. Are you sure you want to proceed?".'
        elif context.get('opportunity_id'):
            res['name'] = 'Opportunity NATHI'
        elif context.get('amount_total_msg'):
            res['name'] = 'Amount total 0.0'
        return res
