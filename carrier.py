# -*- coding: utf-8 -*-
"""
    carrier.py

"""
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Bool
from trytond.model import fields, ModelSQL, ModelView
from trytond.transaction import Transaction

__all__ = ['Carrier', 'CarrierService']
__metaclass__ = PoolMeta


class Carrier:
    "Carrier"
    __name__ = 'carrier'

    currency = fields.Many2One('currency.currency', 'Currency', required=True)

    @staticmethod
    def default_currency():
        Company = Pool().get('company.company')

        company = Transaction().context.get('company')
        if company:
            return Company(company).currency.id

    def get_rates(self):
        """
        Expects a list of tuples as:
            [
                (
                    <display method name>, <rate>, <currency>, <metadata>,
                    <write_vals>
                )
                ...
            ]

        Downstream shipping modules can implement this to get shipping rates.
        """
        # TODO: Remove this method in next version and use `get_shipping_rates`
        # method in sale instead
        return []  # pragma: no cover


class CarrierService(ModelSQL, ModelView):
    "Carrier Service"
    __name__ = 'carrier.service'

    active = fields.Boolean('Active', select=True)
    name = fields.Char('Name', required=True, select=True, readonly=True)
    value = fields.Char('Value', required=True, select=True, readonly=True)
    method_type = fields.Selection(
        'get_method_type', 'Type', select=True, readonly=True,
        states={'required': Bool(Eval('is_method_type_required'))},
        depends=['is_method_type_required']
    )
    display_name = fields.Char('Display Name', select=True)
    source = fields.Selection(
        'get_source', 'Source', required=True, readonly=True
    )

    is_method_type_required = fields.Function(
        fields.Boolean("Is Method Type Required ?"),
        'on_change_with_is_method_type_required'
    )

    def on_change_with_is_method_type_required(self, name=None):
        return True

    @classmethod
    def get_method_type(cls):
        """
        Get the method type
        """
        return [(None, '')]

    @classmethod
    def get_source(cls):
        """
        Get the source
        """
        return []

    @staticmethod
    def default_active():
        return True
