from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "task"

    purchase_count = fields.Integer(
        string='Purchase Count'
    )
    button_hide = fields.Boolean(
        string='button_hide'
    )
    second_name = fields.Char(
        string="Second Task"
    )

    def action_confirm(self):
        context = {'active_model': 'sale.order', 'active_id': self.id}
        warning = {
            'name': 'warning',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.confirm.wizard',
            'view_id': self.env.ref('context_practice.sale_order_confirm_wizard_form_view').id,
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

    def create_purchase_record(self):
        purchase_record_for_count = self.env['purchase.order'].search([('unique', '=', self.name)])
        self.purchase_count = len(list(rec.id for rec in purchase_record_for_count))
        if "view_purchase" not in self.env.context:
            self.button_hide = True
            purchase_record = self.env['purchase.order'].create({
                'partner_id': self.partner_id.id,
                'unique': self.name
            })
            for rec in self.order_line:
                purchase_record.update({
                    'order_line': [(fields.Command.create({
                        'product_id': rec.product_id.id,
                        'product_qty': rec.product_uom_qty,
                        'price_unit': rec.price_unit,
                        'taxes_id': rec.tax_id.id
                    }))]
                })
            return {
                'name': "Purchase",
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'purchase.order',
                'res_id': purchase_record.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }

        elif self.env.context.get('view_purchase'):
            purchase_record = self.env['purchase.order'].search([('unique', '=', self.name)])
            return {
                'name': "Purchase",
                'view_mode': 'tree,form',
                'view_id': False,
                'view_type': 'tree',
                'res_model': 'purchase.order',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', list(rec.id for rec in purchase_record))]
            }

    def action_purchase_record(self):
        return self.with_context({'view_purchase': True}).create_purchase_record()

    def action_field_write(self):
        context = self.env.context.get('second_name')
        if not context:
            self.second_name = "Test"

    @api.constrains('order_line')
    def hide_button(self):
        self.button_hide = False
