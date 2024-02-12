from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "task"

    def action_confirm(self):
        # print('==========================================',self.amount_total)
        context = {'active_model': 'sale.order', 'active_id': self.id,}
        warning = {
            'name': 'warning',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.confrom.wizard',
            'view_id': self.env.ref('context_task.sale_order_confrom_wizard_form_view').id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': context
        }
        if self.partner_id.untrustworthy:
            context['trust_not'] = True
            context['context_opportunity'] = True
            context['total_amount'] = True
            return warning
        if not self.opportunity_id:
            if 'opportunity' not in self.env.context:
                context['opportunity_id'] = True
                context['total_amount'] = True
                context['context_opportunity'] = False
                return warning
        if self.amount_total == float(0.0):
            if self.env.context.get('amount_total'):
                context['amount_total'] = False
                context['context_opportunity'] = False
                context['amount_total_msg'] = True
                return warning
            elif 'amount_total' not in self.env.context:
                context['amount_total'] = False
                context['amount_total_msg'] = True
                context['context_opportunity'] = False
                return warning

        return super(SaleOrder, self).action_confirm()
