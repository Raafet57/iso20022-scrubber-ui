from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET


def _strip_tag(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def _get_ns(element: ET.Element) -> Dict[str, str]:
    tag = element.tag
    if not tag.startswith("{"):
        return {"ns": ""}
    uri = tag[1:].split("}")[0]
    return {"ns": uri}


def _text(node: Optional[ET.Element], default: str = "") -> str:
    if node is None or node.text is None:
        return default
    return node.text.strip()


def parse_message(xml_text: str) -> Dict[str, Any]:
    root = ET.fromstring(xml_text)
    ns = _get_ns(root)
    if not list(root):
        raise ValueError("Invalid ISO 20022 payload: empty Document")
    document = list(root)[0]
    message_tag = _strip_tag(document.tag)

    if message_tag == "FIToFICstmrCdtTrf":
        return _extract_pacs008(document, ns)
    if message_tag == "FICdtTrf":
        return _extract_pacs009(document, ns)
    if message_tag == "BkToCstmrStmt":
        return _extract_camt053(document, ns)

    raise ValueError(f"Unsupported ISO 20022 message: {message_tag}")


def _actor(node: Optional[ET.Element], ns: Dict[str, str]) -> Optional[Dict[str, str]]:
    if node is None:
        return None
    parts: List[str] = []
    addr = node.find("ns:PstlAdr", ns)
    if addr is not None:
        for child in addr:
            value = _text(child)
            if value:
                parts.append(value)
    name = _text(node.find("ns:Nm", ns))
    if not name:
        bic = node.find("ns:FinInstnId/ns:BICFI", ns)
        name = _text(bic)
    return {
        "name": name,
        "address": ", ".join(parts) if parts else None,
    }


def _extract_pacs008(document: ET.Element, ns: Dict[str, str]) -> Dict[str, Any]:
    tx = document.find("ns:CdtTrfTxInf", ns)
    if tx is None:
        raise ValueError("pacs.008 missing CdtTrfTxInf")

    def find(path: str) -> Optional[ET.Element]:
        return tx.find(path, ns)

    amount = find("ns:IntrBkSttlmAmt")
    instructed_amount = find("ns:InstdAmt")
    timeline = {
        "created": _text(document.find("ns:GrpHdr/ns:CreDtTm", ns)),
        "requested_execution": _text(tx.find("ns:PmtTpInf/ns:ReqdExctnDt", ns)),
        "settlement": _text(find("ns:SttlmDt")),
    }
    references = {
        "instruction": _text(tx.find("ns:PmtId/ns:InstrId", ns)),
        "end_to_end": _text(tx.find("ns:PmtId/ns:EndToEndId", ns)),
        "transaction": _text(tx.find("ns:PmtId/ns:TxId", ns)),
        "uetr": _text(tx.find("ns:PmtId/ns:UETR", ns)),
    }

    remittance = {"unstructured": [], "structured": []}
    rem = find("ns:RmtInf")
    if rem is not None:
        remittance["unstructured"] = [
            _text(node) for node in rem.findall("ns:Ustrd", ns) if _text(node)
        ]
        for struct in rem.findall("ns:Strd", ns):
            ref = _text(struct.find("ns:CdtrRefInf/ns:Ref", ns))
            if ref:
                remittance["structured"].append(ref)

    intermediaries = []
    for i in range(1, 4):
        bic = _text(find(f"ns:IntrmyAgt{i}/ns:FinInstnId/ns:BICFI"))
        if bic:
            intermediaries.append(bic)

    route = {
        "debtor_agent": _text(find("ns:DbtrAgt/ns:FinInstnId/ns:BICFI")),
        "creditor_agent": _text(find("ns:CdtrAgt/ns:FinInstnId/ns:BICFI")),
        "intermediaries": intermediaries,
    }

    return {
        "message_type": "pacs.008",
        "actors": {
            "debtor": _actor(find("ns:Dbtr"), ns),
            "ultimate_debtor": _actor(find("ns:UltmtDbtr"), ns),
            "creditor": _actor(find("ns:Cdtr"), ns),
            "ultimate_creditor": _actor(find("ns:UltmtCdtr"), ns),
        },
        "financial": {
            "settlement_amount": {
                "value": _text(amount),
                "currency": amount.get("Ccy") if amount is not None else None,
            },
            "instructed_amount": {
                "value": _text(instructed_amount),
                "currency": instructed_amount.get("Ccy")
                if instructed_amount is not None
                else None,
            },
            "charge_bearer": _text(find("ns:ChrgBr")),
        },
        "timeline": timeline,
        "references": references,
        "remittance": remittance,
        "route": route,
        "charges": [
            {
                "amount": _text(node.find("ns:Amt", ns)),
                "currency": node.find("ns:Amt", ns).get("Ccy")
                if node.find("ns:Amt", ns) is not None
                else None,
                "agent": _text(node.find("ns:Agt/ns:FinInstnId/ns:BICFI", ns)),
            }
            for node in tx.findall("ns:ChrgsInf", ns)
        ],
    }


def _extract_pacs009(document: ET.Element, ns: Dict[str, str]) -> Dict[str, Any]:
    tx = document.find("ns:CdtTrfTxInf", ns)
    if tx is None:
        raise ValueError("pacs.009 missing CdtTrfTxInf")

    amount = document.find("ns:GrpHdr/ns:TtlIntrBkSttlmAmt", ns)
    timeline = {
        "created": _text(document.find("ns:GrpHdr/ns:CreDtTm", ns)),
        "settlement": _text(document.find("ns:GrpHdr/ns:SttlmInf/ns:SttlmDt", ns)),
    }

    references = {
        "instruction": _text(tx.find("ns:PmtId/ns:InstrId", ns)),
        "end_to_end": _text(tx.find("ns:PmtId/ns:EndToEndId", ns)),
        "transaction": _text(tx.find("ns:PmtId/ns:TxId", ns)),
        "uetr": _text(tx.find("ns:PmtId/ns:UETR", ns)),
    }

    intermediaries = []
    for i in range(1, 4):
        bic = _text(tx.find(f"ns:IntermediaryAgt{i}/ns:FinInstnId/ns:BICFI", ns))
        if bic:
            intermediaries.append(bic)

    return {
        "message_type": "pacs.009",
        "actors": {
            "debtor_agent": _actor(tx.find("ns:DbtrAgt", ns), ns),
            "creditor_agent": _actor(tx.find("ns:CdtrAgt", ns), ns),
            "creditor": _actor(tx.find("ns:Cdtr", ns), ns),
        },
        "financial": {
            "settlement_amount": {
                "value": _text(amount),
                "currency": amount.get("Ccy") if amount is not None else None,
            },
            "charge_bearer": _text(tx.find("ns:ChrgBr", ns)),
        },
        "timeline": timeline,
        "references": references,
        "route": {
            "intermediaries": intermediaries,
        },
        "remittance": {
            "unstructured": [
                _text(node)
                for node in tx.findall("ns:RmtInf/ns:Ustrd", ns)
                if _text(node)
            ]
        },
    }


def _extract_camt053(document: ET.Element, ns: Dict[str, str]) -> Dict[str, Any]:
    stmt = document.find("ns:Stmt", ns)
    if stmt is None:
        raise ValueError("camt.053 missing Stmt element")

    entries: List[Dict[str, Any]] = []
    for entry in stmt.findall("ns:Ntry", ns):
        amount_node = entry.find("ns:Amt", ns)
        entries.append(
            {
                "amount": _text(amount_node),
                "currency": amount_node.get("Ccy") if amount_node is not None else None,
                "credit_debit": _text(entry.find("ns:CdtDbtInd", ns)),
                "booking_date": _text(entry.find("ns:BookgDt/ns:Dt", ns)),
                "value_date": _text(entry.find("ns:ValDt/ns:Dt", ns)),
                "reference": _text(entry.find("ns:AcctSvcrRef", ns)),
                "remittance": _text(entry.find(".//ns:Ustrd", ns)),
            }
        )

    balance_node = stmt.find("ns:Bal/ns:Amt", ns)

    return {
        "message_type": "camt.053",
        "statement_id": _text(stmt.find("ns:Id", ns)),
        "account": {
            "iban": _text(stmt.find("ns:Acct/ns:Id/ns:IBAN", ns)),
            "owner": _actor(stmt.find("ns:Acct/ns:Ownr", ns), ns),
        },
        "closing_balance": {
            "amount": _text(balance_node),
            "currency": balance_node.get("Ccy") if balance_node is not None else None,
            "date": _text(stmt.find("ns:Bal/ns:Dt/ns:Dt", ns)),
        },
        "entries": entries,
        "generated_at": _text(stmt.find("ns:CreDtTm", ns)),
    }


def load_message(path: Path) -> Dict[str, Any]:
    return parse_message(Path(path).read_text())
