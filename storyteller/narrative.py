from __future__ import annotations

from typing import Any, Dict, List


def _format_amount(node: Dict[str, Any]) -> str:
    if not node or not node.get("value"):
        return "an unspecified amount"
    try:
        value = float(node["value"])
        formatted = f"{value:,.2f}"
    except ValueError:
        formatted = node["value"]
    currency = node.get("currency")
    return f"{formatted} {currency}".strip() if currency else formatted


def _name(actor: Dict[str, Any] | None) -> str:
    if not actor or not actor.get("name"):
        return "an unspecified party"
    return actor["name"]


def generate_narrative(payload: Dict[str, Any], mode: str = "narrative") -> str:
    message_type = payload["message_type"]
    if message_type == "camt.053":
        return _statement_narrative(payload, mode)
    return _payment_narrative(payload, mode)


def _payment_narrative(payload: Dict[str, Any], mode: str) -> str:
    actors = payload.get("actors", {})
    financial = payload.get("financial", {})
    timeline = payload.get("timeline", {})
    references = payload.get("references", {})
    remittance = payload.get("remittance", {})
    route = payload.get("route", {})

    debtor = _name(actors.get("debtor") or actors.get("debtor_agent"))
    creditor = _name(actors.get("creditor"))
    amount = _format_amount(financial.get("settlement_amount"))
    charge = financial.get("charge_bearer") or "unspecified"
    created = timeline.get("created") or timeline.get("requested_execution")
    uetr = references.get("uetr")
    purpose = ", ".join(remittance.get("unstructured", [])) or (
        ", ".join(remittance.get("structured", [])) or "no remittance information"
    )

    if mode == "concise":
        lines = [
            f"Payer: {debtor}",
            f"Beneficiary: {creditor}",
            f"Amount: {amount}",
            f"Charge bearer: {charge}",
            f"Created: {created or 'n/a'}",
            f"UETR: {uetr or 'n/a'}",
            f"Purpose: {purpose}",
            f"Intermediaries: {', '.join(filter(None, route.get('intermediaries', []))) or 'none'}",
        ]
        return "\n".join(f"- {line}" for line in lines)

    narrative = (
        f"{debtor} is sending {amount} to {creditor}. "
        f"The request was created on {created or 'an unknown date'}, with charge bearer set to {charge}. "
        f"Routing involves {route.get('intermediaries', []) or 'no intermediary banks specified'}. "
        f"Purpose: {purpose}. "
    )
    if uetr:
        narrative += f"The transaction UETR is {uetr}. "
    return narrative.strip()


def _statement_narrative(payload: Dict[str, Any], mode: str) -> str:
    account = payload.get("account", {})
    entries = payload.get("entries", [])
    closing = payload.get("closing_balance", {})
    owner = _name(account.get("owner"))
    iban = account.get("iban") or "unspecified account"
    closing_str = _format_amount(
        {"value": closing.get("amount"), "currency": closing.get("currency")}
    )
    date = closing.get("date") or payload.get("generated_at")

    if mode == "concise":
        lines = [
            f"Account owner: {owner}",
            f"IBAN: {iban}",
            f"Closing balance: {closing_str} on {date or 'n/a'}",
            f"Entries: {len(entries)}",
        ]
        return "\n".join(f"- {line}" for line in lines)

    sample_entries = entries[:3]
    entry_texts: List[str] = []
    for entry in sample_entries:
        entry_amount = f"{entry.get('amount')} {entry.get('currency') or ''}".strip()
        entry_texts.append(
            f"{entry.get('credit_debit')} entry of {entry_amount} on {entry.get('booking_date')} "
            f"(ref {entry.get('reference') or 'n/a'})"
        )
    entry_sentence = "; ".join(entry_texts) if entry_texts else "no booked entries described"

    return (
        f"Statement for {owner} ({iban}) reports a closing balance of {closing_str} on {date or 'n/a'}. "
        f"The file lists {len(entries)} entries; examples include {entry_sentence}."
    )
