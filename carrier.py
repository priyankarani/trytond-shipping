# -*- coding: utf-8 -*-
"""
    carrier.py

"""
from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.transaction import Transaction
from trytond import backend
from trytond.pyson import Eval, Bool

__all__ = ['Carrier']
__metaclass__ = PoolMeta


class Carrier:
    "Carrier"
    __name__ = 'carrier'

    currency = fields.Function(
        fields.Many2One(
            'currency.currency', 'Currency', states={
                'invisible': Bool(Eval('hide_currency'))
            }, depends=['hide_currency']
        ), 'get_currency'
    )
    hide_currency = fields.Function(
        fields.Boolean("Hide Currency ?"), 'on_change_with_hide_currency'
    )

    @fields.depends('carrier_cost_method')
    def on_change_with_hide_currency(self, name=None):
        return self._get_hide_currency()

    def _get_hide_currency(self):
        """
        Downstream module can implement this method to hide or show currency
        field accordingly
        """
        return True

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().cursor

        super(Carrier, cls).__register__(module_name)

        table = TableHandler(cursor, cls, module_name)

        # Remove currency field
        if table.column_exist('currency'):
            table.drop_column('currency')

    def get_currency(self, name):
        """
        Downstream module can implement this method to return respective
        currency
        """
        Company = Pool().get('company.company')

        company_id = Transaction().context.get('company')
        if company_id:
            return Company(company_id).currency.id

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
