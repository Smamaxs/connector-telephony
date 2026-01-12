# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


class VoipOcaCall(models.Model):
    _inherit = "res.partner"

    def format_partner(self, partner_ids=None):
        """
        Return a serializable dict for a partner.
        This method can be called in two ways:
        - As an instance method: partner.format_partner() -> formats that partner
        - As an RPC on the model: env['res.partner'].format_partner([id]) -> formats partner with id
        """
        # Determine partner record
        partner = None
        if partner_ids:
            # partner_ids is expected to be a list like [id]
            try:
                pid = partner_ids[0]
            except Exception:
                pid = None
            if pid:
                partner = self.browse(pid)
        else:
            # called on a recordset
            partner = self

        # If no partner (empty recordset), return an empty mapping
        if not partner or not partner.exists():
            return {}

        # Work with first record only
        partner = partner[0]

        return {
            "id": partner.id,
            "type": "partner",
            "displayName": partner.display_name,
            "email": partner.email or "",
            "landlineNumber": getattr(partner, "phone", "") or "",
            "name": partner.name or "",
        }

    @api.model
    def voip_get_contacts(self, _search, offset, limit):
        domain = [("phone", "!=", False)]
        if _search:
            search_fields = ["name", "phone", "email"]
            search_domain = expression.OR(
                [[(field, "ilike", _search)] for field in search_fields]
            )
            domain = expression.AND([domain, search_domain])
        contacts = self.search(domain, offset=offset, limit=limit)
        return [contact.format_partner() for contact in contacts]

    def get_activity_main_partner_id(self):
        """Override to return the partner itself."""
        return self
