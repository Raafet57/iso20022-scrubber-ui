from __future__ import annotations

import uuid
from pathlib import Path
from textwrap import dedent
from typing import Dict, List

SAMPLES_DIR = Path(__file__).parent / "samples"


def write_file(name: str, content: str) -> None:
    path = SAMPLES_DIR / name
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def build_pacs008(data: Dict) -> str:
    inter_xml = "".join(
        f"""
        <IntrmyAgt{i+1}>
          <FinInstnId>
            <BICFI>{bic}</BICFI>
          </FinInstnId>
        </IntrmyAgt{i+1}>
        """
        for i, bic in enumerate(data.get("intermediaries", []))
    )
    fx_xml = ""
    if data.get("fx_rate"):
        fx_xml = f"""
        <FxInf>
          <XchgRate>{data['fx_rate']}</XchgRate>
          <CtrctId>{data.get('fx_contract', 'FX-AUTO')}</CtrctId>
        </FxInf>
        """
    rem_strd = ""
    if data.get("structured_ref"):
        rem_strd = f"""
        <Strd>
          <CdtrRefInf>
            <Ref>{data['structured_ref']}</Ref>
          </CdtrRefInf>
        </Strd>
        """
    rem_unstrd = "".join(
        f"<Ustrd>{line}</Ustrd>" for line in data.get("remittance", [])
    )
    ultimate_dbtr = ""
    if data.get("ultimate_debtor"):
        ultimate_dbtr = f"""
        <UltmtDbtr>
          <Nm>{data['ultimate_debtor']}</Nm>
        </UltmtDbtr>
        """
    ultimate_cdtr = ""
    if data.get("ultimate_creditor"):
        ultimate_cdtr = f"""
        <UltmtCdtr>
          <Nm>{data['ultimate_creditor']}</Nm>
        </UltmtCdtr>
        """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>{data['msg_id']}</MsgId>
      <CreDtTm>{data['created']}</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <SttlmInf>
        <SttlmMtd>{data.get('settlement_method', 'INDA')}</SttlmMtd>
      </SttlmInf>
    </GrpHdr>
    <CdtTrfTxInf>
      <PmtId>
        <InstrId>{data['instr_id']}</InstrId>
        <EndToEndId>{data['end_to_end']}</EndToEndId>
        <TxId>{data['tx_id']}</TxId>
        <UETR>{data['uetr']}</UETR>
      </PmtId>
      <PmtTpInf>
        <SvcLvl>
          <Cd>{data.get('service_level', 'SEPA')}</Cd>
        </SvcLvl>
        <ReqdExctnDt>{data.get('req_exec', data['created'][:10])}</ReqdExctnDt>
      </PmtTpInf>
      <IntrBkSttlmAmt Ccy="{data['currency']}">{data['amount']}</IntrBkSttlmAmt>
      <ChrgBr>{data.get('charge', 'SHA')}</ChrgBr>
      {fx_xml}
      {ultimate_dbtr}
      <Dbtr>
        <Nm>{data['debtor_name']}</Nm>
        <PstlAdr>
          <StrtNm>{data['debtor_addr'][0]}</StrtNm>
          <TwnNm>{data['debtor_addr'][1]}</TwnNm>
          <Ctry>{data['debtor_addr'][2]}</Ctry>
          <PstCd>{data['debtor_addr'][3]}</PstCd>
        </PstlAdr>
      </Dbtr>
      <DbtrAcct>
        <Id>
          <IBAN>{data['debtor_iban']}</IBAN>
        </Id>
      </DbtrAcct>
      <DbtrAgt>
        <FinInstnId>
          <BICFI>{data['debtor_bic']}</BICFI>
        </FinInstnId>
      </DbtrAgt>
      {inter_xml}
      <CdtrAgt>
        <FinInstnId>
          <BICFI>{data['creditor_bic']}</BICFI>
        </FinInstnId>
      </CdtrAgt>
      <Cdtr>
        <Nm>{data['creditor_name']}</Nm>
        <PstlAdr>
          <StrtNm>{data['creditor_addr'][0]}</StrtNm>
          <TwnNm>{data['creditor_addr'][1]}</TwnNm>
          <Ctry>{data['creditor_addr'][2]}</Ctry>
          <PstCd>{data['creditor_addr'][3]}</PstCd>
        </PstlAdr>
      </Cdtr>
      {ultimate_cdtr}
      <CdtrAcct>
        <Id>
          <IBAN>{data['creditor_iban']}</IBAN>
        </Id>
      </CdtrAcct>
      <RmtInf>
        {rem_unstrd}
        {rem_strd}
      </RmtInf>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>
"""


def build_pacs009(data: Dict) -> str:
    inter_xml = "".join(
        f"""
        <IntermediaryAgt{i+1}>
          <FinInstnId>
            <BICFI>{bic}</BICFI>
          </FinInstnId>
        </IntermediaryAgt{i+1}>
        """
        for i, bic in enumerate(data.get("intermediaries", []))
    )
    rem_xml = "".join(
        f"<Ustrd>{line}</Ustrd>" for line in data.get("remittance", [])
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.009.001.08">
  <FICdtTrf>
    <GrpHdr>
      <MsgId>{data['msg_id']}</MsgId>
      <CreDtTm>{data['created']}</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <TtlIntrBkSttlmAmt Ccy="{data['currency']}">{data['amount']}</TtlIntrBkSttlmAmt>
      <SttlmInf>
        <SttlmMtd>{data.get('settlement_method', 'INDA')}</SttlmMtd>
      </SttlmInf>
    </GrpHdr>
    <CdtTrfTxInf>
      <PmtId>
        <InstrId>{data['instr_id']}</InstrId>
        <EndToEndId>{data['end_to_end']}</EndToEndId>
        <TxId>{data['tx_id']}</TxId>
        <UETR>{data['uetr']}</UETR>
      </PmtId>
      <ChrgBr>{data.get('charge', 'SHA')}</ChrgBr>
      <DbtrAgt>
        <FinInstnId>
          <BICFI>{data['debtor_agent']}</BICFI>
        </FinInstnId>
      </DbtrAgt>
      {inter_xml}
      <CdtrAgt>
        <FinInstnId>
          <BICFI>{data['creditor_agent']}</BICFI>
        </FinInstnId>
      </CdtrAgt>
      <Cdtr>
        <Nm>{data['creditor_name']}</Nm>
      </Cdtr>
      <CdtrAcct>
        <Id>
          <IBAN>{data['creditor_iban']}</IBAN>
        </Id>
      </CdtrAcct>
      <RmtInf>
        {rem_xml}
      </RmtInf>
    </CdtTrfTxInf>
  </FICdtTrf>
</Document>
"""


def build_camt053(data: Dict) -> str:
    entries_xml = ""
    for entry in data["entries"]:
        entries_xml += f"""
        <Ntry>
          <Amt Ccy="{entry['currency']}">{entry['amount']}</Amt>
          <CdtDbtInd>{entry['cd_indicator']}</CdtDbtInd>
          <BookgDt><Dt>{entry['booking_date']}</Dt></BookgDt>
          <ValDt><Dt>{entry['value_date']}</Dt></ValDt>
          <AcctSvcrRef>{entry['reference']}</AcctSvcrRef>
          <NtryDtls>
            <TxDtls>
              <RltdPties>
                <Cdtr>
                  <Nm>{entry.get('creditor', 'N/A')}</Nm>
                </Cdtr>
              </RltdPties>
              <RmtInf>
                <Ustrd>{entry.get('remittance', '')}</Ustrd>
              </RmtInf>
            </TxDtls>
          </NtryDtls>
        </Ntry>
        """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.10">
  <BkToCstmrStmt>
    <GrpHdr>
      <MsgId>{data['msg_id']}</MsgId>
      <CreDtTm>{data['created']}</CreDtTm>
    </GrpHdr>
    <Stmt>
      <Id>{data['statement_id']}</Id>
      <CreDtTm>{data['created']}</CreDtTm>
      <Acct>
        <Id>
          <IBAN>{data['iban']}</IBAN>
        </Id>
        <Ownr>
          <Nm>{data['owner']}</Nm>
        </Ownr>
      </Acct>
      <Bal>
        <Tp><CdOrPrtry><Cd>CLBD</Cd></CdOrPrtry></Tp>
        <Amt Ccy="{data['closing_currency']}">{data['closing_amount']}</Amt>
        <CdtDbtInd>CRDT</CdtDbtInd>
        <Dt><Dt>{data['closing_date']}</Dt></Dt>
      </Bal>
      {entries_xml}
    </Stmt>
  </BkToCstmrStmt>
</Document>
"""


def build_simple(doc: str) -> str:
    return doc


def uuid_str() -> str:
    return str(uuid.uuid4())


def main() -> None:
    scenarios: List[Dict[str, str]] = []

    pacs008_data = [
        {
            "filename": "bulk-pacs008-asia-urgent.xml",
            "msg_id": "ASIA-URGENT-001",
            "created": "2025-03-21T04:05:00+07:00",
            "amount": "1450000.75",
            "currency": "THB",
            "charge": "OUR",
            "debtor_name": "Harmony Industrial Thai",
            "debtor_addr": ["99 Narathiwas Road", "Bangkok", "TH", "10120"],
            "debtor_bic": "HMBKTH2BXXX",
            "debtor_iban": "TH12009988001234567890",
            "creditor_name": "Mega Components SDN BHD",
            "creditor_addr": ["12 Jalan Bangsar", "Kuala Lumpur", "MY", "59000"],
            "creditor_bic": "MEGAHKHHXXX",
            "creditor_iban": "MY12MEGA00001234005678",
            "instr_id": "TH-PRIO-001",
            "end_to_end": "INV-TH-778",
            "tx_id": "HMBKTH-PRIO-001",
            "uetr": uuid_str(),
            "intermediaries": ["BKTRUS33XXX"],
            "remittance": ["Urgent tooling prepayment"],
        },
        {
            "filename": "bulk-pacs008-eur-cover.xml",
            "msg_id": "EU-COVER-092",
            "created": "2025-02-11T09:00:00+01:00",
            "amount": "250000.00",
            "currency": "EUR",
            "charge": "SHA",
            "debtor_name": "BNP Paribas Brussels",
            "debtor_addr": ["16 Rue Royale", "Brussels", "BE", "1000"],
            "debtor_bic": "BNPAFRPPBXL",
            "debtor_iban": "BE56001100445566",
            "creditor_name": "Harmony Nordic AB",
            "creditor_addr": ["Sveavägen 15", "Stockholm", "SE", "11157"],
            "creditor_bic": "HARMSESSXXX",
            "creditor_iban": "SE4780000456789001234567",
            "instr_id": "BNP-COVER-092",
            "end_to_end": "SE-PO-7782",
            "tx_id": "BNPAFRPPBXL-2025-92",
            "uetr": uuid_str(),
            "intermediaries": ["DEUTDEFFXXX", "HMBKUS44GAR"],
            "remittance": ["Cover for purchase order 7782"],
        },
        {
            "filename": "bulk-pacs008-fx-multicurrency.xml",
            "msg_id": "FX-MULTI-303",
            "created": "2025-01-18T15:30:00Z",
            "amount": "875000.00",
            "currency": "USD",
            "charge": "SHA",
            "fx_rate": "1.0875",
            "fx_contract": "FX-USD-EUR-303",
            "debtor_name": "EuroTech Manufacturing GmbH",
            "debtor_addr": ["Industriestrasse 5", "Munich", "DE", "80331"],
            "debtor_bic": "EURODEMMXXX",
            "debtor_iban": "DE12500105170648489890",
            "creditor_name": "Pacific Rim Logistics",
            "creditor_addr": ["8 Harbour Drive", "Singapore", "SG", "117540"],
            "creditor_bic": "PRIMSGSGXXX",
            "creditor_iban": "SG58PRIM000000156545",
            "instr_id": "EURO-FX-303",
            "end_to_end": "FX-PO-1188",
            "tx_id": "EURODEMM-FX-303",
            "uetr": uuid_str(),
            "intermediaries": ["CITIUS33XXX"],
            "remittance": ["FX payment for PO1188"],
        },
        {
            "filename": "bulk-pacs008-gbp-priority.xml",
            "msg_id": "GBP-PRIORITY-014",
            "created": "2025-03-03T11:20:00+00:00",
            "amount": "1125000.00",
            "currency": "GBP",
            "charge": "OUR",
            "debtor_name": "Harmony Treasury UK",
            "debtor_addr": ["5 Bishopsgate", "London", "GB", "EC2N4AJ"],
            "debtor_bic": "HMBKGB2LXXX",
            "debtor_iban": "GB12HMBK40127688990011",
            "creditor_name": "Auckland Infrastructure Ltd",
            "creditor_addr": ["45 High Street", "Auckland", "NZ", "1010"],
            "creditor_bic": "ANZBNZ22XXX",
            "creditor_iban": "NZ26ANZB0000001234567",
            "instr_id": "GBP-PRIO-14",
            "end_to_end": "CAPEX-NZ-14",
            "tx_id": "HMBKGB2L-PRIO-14",
            "uetr": uuid_str(),
            "intermediaries": ["ANZBNZ22XXX"],
            "remittance": ["Bridge financing tranche 14"],
        },
        {
            "filename": "bulk-pacs008-structured-remittance.xml",
            "msg_id": "STRUCT-077",
            "created": "2025-04-02T08:00:00+02:00",
            "amount": "65000.25",
            "currency": "EUR",
            "charge": "SHA",
            "debtor_name": "BNP Paribas Chartres",
            "debtor_addr": ["12 Rue du Docteur Mazet", "Chartres", "FR", "28000"],
            "debtor_bic": "BNPAFRPPCHS",
            "debtor_iban": "FR7610096000301234567890188",
            "creditor_name": "AVIO S.P.A.",
            "creditor_addr": ["VIA MAURO MACCHI 27", "MILANO", "IT", "20124"],
            "creditor_bic": "AVIOITM1XXX",
            "creditor_iban": "IT40X0100501600000001234567",
            "instr_id": "STRUCT-077",
            "end_to_end": "RF18539007520034000011",
            "tx_id": "BNPAFRPPCHS-077",
            "uetr": uuid_str(),
            "intermediaries": ["BNPAFRPPCRT"],
            "remittance": [],
            "structured_ref": "RF18539007520034000011",
        },
        {
            "filename": "bulk-pacs008-weekend.xml",
            "msg_id": "WEEKEND-029",
            "created": "2025-04-05T10:12:00-03:00",
            "amount": "98000.00",
            "currency": "BRL",
            "charge": "SHA",
            "debtor_name": "Harmonia Importacao LTDA",
            "debtor_addr": ["Av Paulista 55", "São Paulo", "BR", "01310-100"],
            "debtor_bic": "BRASBRRJXXX",
            "debtor_iban": "BR15000099990000123451",
            "creditor_name": "Lisboa Trading SA",
            "creditor_addr": ["Rua Augusta 14", "Lisbon", "PT", "1100-053"],
            "creditor_bic": "BCOMPTPLXXX",
            "creditor_iban": "PT50003300004567890123456",
            "instr_id": "BR-PT-029",
            "end_to_end": "IMP-029",
            "tx_id": "BRASBRRJ-029",
            "uetr": uuid_str(),
            "intermediaries": ["BCOMPTPLXXX"],
            "remittance": ["Weekend customs fees"],
        },
        {
            "filename": "bulk-pacs008-missing-remittance.xml",
            "msg_id": "NO-REM-101",
            "created": "2025-02-22T17:00:00Z",
            "amount": "425000.00",
            "currency": "USD",
            "debtor_name": "Midwest Holdings",
            "debtor_addr": ["455 Main Street", "Chicago", "US", "60601"],
            "debtor_bic": "MDWESTUSXXX",
            "debtor_iban": "US89MDWE00004567890123",
            "creditor_name": "Pacific Digital Corp",
            "creditor_addr": ["888 Howard Street", "San Francisco", "US", "94103"],
            "creditor_bic": "SVBKUS6SXXX",
            "creditor_iban": "US07SVBK00000012000001",
            "instr_id": "MDW-101",
            "end_to_end": "MDWE2E101",
            "tx_id": "MDWESTUS-101",
            "uetr": uuid_str(),
            "intermediaries": [],
            "remittance": [],
        },
        {
            "filename": "bulk-pacs008-highcharges.xml",
            "msg_id": "CHARGES-222",
            "created": "2025-01-12T09:15:00+08:00",
            "amount": "310000.00",
            "currency": "USD",
            "charge": "OUR",
            "debtor_name": "Harmony Bank Manila",
            "debtor_addr": ["23 Ayala Avenue", "Makati", "PH", "1226"],
            "debtor_bic": "HMBKPHMMXXX",
            "debtor_iban": "PH56HMBK00000078901234",
            "creditor_name": "Sydney Harbour Services",
            "creditor_addr": ["48 Barangaroo", "Sydney", "AU", "2000"],
            "creditor_bic": "WPACAU2SXXX",
            "creditor_iban": "AU12099998887776665000",
            "instr_id": "MAN-222",
            "end_to_end": "SYD-222",
            "tx_id": "HMBKPHMM-222",
            "uetr": uuid_str(),
            "intermediaries": ["CITIUS33XXX", "WPACAU2SXXX"],
            "remittance": ["Maritime services retainer"],
        },
        {
            "filename": "bulk-pacs008-sme-payroll.xml",
            "msg_id": "PAYROLL-045",
            "created": "2025-03-28T06:30:00+02:00",
            "amount": "78000.00",
            "currency": "EUR",
            "charge": "SHA",
            "debtor_name": "Harmony SME Payroll",
            "debtor_addr": ["5 Avenue d'Italie", "Paris", "FR", "75013"],
            "debtor_bic": "HMBKFRPPXXX",
            "debtor_iban": "FR1420041010050500013M02606",
            "creditor_name": "Nordic Payroll Hub",
            "creditor_addr": ["2 Fredrikinkatu", "Helsinki", "FI", "00120"],
            "creditor_bic": "NDEAFIHHXXX",
            "creditor_iban": "FI2112345600000785",
            "instr_id": "PAY-045",
            "end_to_end": "PAYROLL-BATCH-045",
            "tx_id": "HMBKFRPP-045",
            "uetr": uuid_str(),
            "intermediaries": ["BNPAFRPPXXX"],
            "remittance": ["SME payroll batch 45"],
        },
        {
            "filename": "bulk-pacs008-latam-trade.xml",
            "msg_id": "LATAM-TRADE-019",
            "created": "2025-02-05T13:45:00-05:00",
            "amount": "2100000.00",
            "currency": "USD",
            "debtor_name": "Andes Commodities",
            "debtor_addr": ["Av Libertadores 500", "Bogota", "CO", "110111"],
            "debtor_bic": "ANDESCCOBXX",
            "debtor_iban": "CO1230000000123456789",
            "creditor_name": "Lisbon Metals SA",
            "creditor_addr": ["Rua do Comércio 20", "Lisbon", "PT", "1100-003"],
            "creditor_bic": "BESZPTPLXXX",
            "creditor_iban": "PT50002700000012345678921",
            "instr_id": "LATAM-19",
            "end_to_end": "SHIPMENT-19",
            "tx_id": "ANDESCCO-19",
            "uetr": uuid_str(),
            "intermediaries": ["CITIUS33XXX", "BESZPTPLXXX"],
            "remittance": ["Concentrate shipment 19"],
        },
        {
            "filename": "bulk-pacs008-uat-test.xml",
            "msg_id": "UAT-008-001",
            "created": "2025-03-12T12:00:00Z",
            "amount": "1234.56",
            "currency": "USD",
            "debtor_name": "Test Sender Inc",
            "debtor_addr": ["123 Test Lane", "Test City", "US", "12345"],
            "debtor_bic": "TESTUS33XXX",
            "debtor_iban": "US00TEST00000012345678",
            "creditor_name": "Test Receiver Ltd",
            "creditor_addr": ["789 Example Road", "Example City", "GB", "E1 1AA"],
            "creditor_bic": "EXAMGB21XXX",
            "creditor_iban": "GB29EXAM60161331926819",
            "instr_id": "UAT-001",
            "end_to_end": "UAT-E2E-001",
            "tx_id": "TESTUS33-001",
            "uetr": uuid_str(),
            "intermediaries": [],
            "remittance": ["Sample narrative for UAT"],
            "ultimate_debtor": "Sample Holdings",
            "ultimate_creditor": "Sample Subsidiary",
        },
    ]

    for data in pacs008_data:
        write_file(data["filename"], build_pacs008(data))

    pacs009_data = [
        {
            "filename": "bulk-pacs009-cover-chf.xml",
            "msg_id": "CH-COVER-001",
            "created": "2025-03-01T10:10:00+01:00",
            "amount": "9500000.00",
            "currency": "CHF",
            "debtor_agent": "UBSWCHZHXXX",
            "creditor_agent": "CITIUS33XXX",
            "creditor_name": "Citibank N.A. Treasury",
            "creditor_iban": "US33CITI000000987654",
            "instr_id": "UBS-COVER-001",
            "end_to_end": "UBS-COVER-001",
            "tx_id": "UBSWCHZH-001",
            "uetr": uuid_str(),
            "intermediaries": ["UBSWCHZHXXX"],
            "remittance": ["Cover payment for USD leg"],
        },
        {
            "filename": "bulk-pacs009-asia-multi-hop.xml",
            "msg_id": "ASIA-MH-004",
            "created": "2025-02-10T18:30:00+09:00",
            "amount": "45000000.00",
            "currency": "JPY",
            "debtor_agent": "HMBKJPJTXXX",
            "creditor_agent": "NDEAFIHHXXX",
            "creditor_name": "Nordic Bank Helsinki",
            "creditor_iban": "FI2112345600000777",
            "instr_id": "HMBKJPJT-004",
            "end_to_end": "CORRIDOR-JP-FI",
            "tx_id": "HMBKJPJT-MH-004",
            "uetr": uuid_str(),
            "intermediaries": ["HMBKUS44GAR", "CITIUS33XXX"],
            "remittance": ["Japan to Finland liquidity move"],
        },
        {
            "filename": "bulk-pacs009-serial-usd.xml",
            "msg_id": "SERIAL-USD-015",
            "created": "2025-03-04T08:00:00-05:00",
            "amount": "125000000.00",
            "currency": "USD",
            "debtor_agent": "HMBKUS44GAR",
            "creditor_agent": "ANZBNZ22XXX",
            "creditor_name": "ANZ New Zealand",
            "creditor_iban": "NZ20ANZB0000002222333",
            "instr_id": "SERIAL-015",
            "end_to_end": "SERIAL-015",
            "tx_id": "HMBKUS44-SERIAL-015",
            "uetr": uuid_str(),
            "intermediaries": ["CITIUS33XXX"],
            "remittance": ["Serial payment 15"],
        },
        {
            "filename": "bulk-pacs009-latam-eur.xml",
            "msg_id": "LATAM-EUR-020",
            "created": "2025-01-15T16:00:00-03:00",
            "amount": "7800000.00",
            "currency": "EUR",
            "debtor_agent": "BRASBRRJXXX",
            "creditor_agent": "BNPAFRPPXXX",
            "creditor_name": "BNP Paribas Paris",
            "creditor_iban": "FR7630006000011234567890189",
            "instr_id": "LATAM-EUR-020",
            "end_to_end": "LATAM-EUR-020",
            "tx_id": "BRASBRRJ-LATAM-020",
            "uetr": uuid_str(),
            "intermediaries": ["CITIUS33XXX", "BNPAFRPPXXX"],
            "remittance": ["LatAm treasury EUR positions"],
        },
        {
            "filename": "bulk-pacs009-weekend.xml",
            "msg_id": "WKND-009-03",
            "created": "2025-04-06T05:45:00+05:30",
            "amount": "65000000.00",
            "currency": "INR",
            "debtor_agent": "PUNBINBBXXX",
            "creditor_agent": "SBININBBXXX",
            "creditor_name": "State Bank of India",
            "creditor_iban": "IN45SBIN00001122334455",
            "instr_id": "WKND-03",
            "end_to_end": "WKND-03",
            "tx_id": "PUNBINBB-WKND-03",
            "uetr": uuid_str(),
            "intermediaries": ["HMBKUS44GAR"],
            "remittance": ["Weekend clearing buffer"],
        },
        {
            "filename": "bulk-pacs009-africa-hvl.xml",
            "msg_id": "AF-HVL-090",
            "created": "2025-02-25T09:10:00+02:00",
            "amount": "22000000.00",
            "currency": "USD",
            "debtor_agent": "PRUDMAMCXXX",
            "creditor_agent": "SCBLGB2LXXX",
            "creditor_name": "Standard Chartered London",
            "creditor_iban": "GB12SCBL40201777777777",
            "instr_id": "AF-HVL-090",
            "end_to_end": "AF-HVL-090",
            "tx_id": "PRUDMAMC-090",
            "uetr": uuid_str(),
            "intermediaries": ["CITIUS33XXX"],
            "remittance": ["High value USD sweep"],
        },
    ]

    for data in pacs009_data:
        write_file(data["filename"], build_pacs009(data))

    camt053_data = [
        {
            "filename": "bulk-camt053-asia-multi-entry.xml",
            "msg_id": "C53-ASIA-001",
            "created": "2025-03-18T05:30:00+07:00",
            "statement_id": "ASIA-DAILY-001",
            "iban": "TH12009988001234567890",
            "owner": "Harmony Industrial Thai",
            "closing_amount": "1450000.75",
            "closing_currency": "THB",
            "closing_date": "2025-03-17",
            "entries": [
                {
                    "amount": "+250000.00",
                    "currency": "THB",
                    "cd_indicator": "CRDT",
                    "booking_date": "2025-03-17",
                    "value_date": "2025-03-17",
                    "reference": "ASIA-REF-001",
                    "remittance": "Inbound manufacturing receipt",
                    "creditor": "Bangkok Components Co. Ltd.",
                },
                {
                    "amount": "-125000.00",
                    "currency": "THB",
                    "cd_indicator": "DBIT",
                    "booking_date": "2025-03-17",
                    "value_date": "2025-03-17",
                    "reference": "ASIA-REF-002",
                    "remittance": "Payroll tranche",
                    "creditor": "Payroll Services",
                },
            ],
        },
        {
            "filename": "bulk-camt053-eur-weekend.xml",
            "msg_id": "C53-EUR-014",
            "created": "2025-03-16T23:45:00+01:00",
            "statement_id": "EU-DAILY-014",
            "iban": "FR7610096000301234567890188",
            "owner": "BNP Paribas Chartres",
            "closing_amount": "58200.75",
            "closing_currency": "EUR",
            "closing_date": "2025-03-14",
            "entries": [
                {
                    "amount": "-52000.00",
                    "currency": "EUR",
                    "cd_indicator": "DBIT",
                    "booking_date": "2025-03-14",
                    "value_date": "2025-03-14",
                    "reference": "BNP-CHS-00078319",
                    "remittance": "Payroll batch March",
                    "creditor": "Harmony Payroll Services",
                },
                {
                    "amount": "+125000.00",
                    "currency": "EUR",
                    "cd_indicator": "CRDT",
                    "booking_date": "2025-03-14",
                    "value_date": "2025-03-14",
                    "reference": "BNP-CHS-00078320",
                    "remittance": "Consulting fees",
                    "creditor": "ACME Consulting",
                },
            ],
        },
        {
            "filename": "bulk-camt053-us-multicurrency.xml",
            "msg_id": "C53-US-020",
            "created": "2025-03-19T05:40:00Z",
            "statement_id": "HARMONY-DAILY-2025-03-19",
            "iban": "US98HMBK09120446200111",
            "owner": "First Southeast Bank Harmony",
            "closing_amount": "2150000.00",
            "closing_currency": "USD",
            "closing_date": "2025-03-18",
            "entries": [
                {
                    "amount": "-250000.00",
                    "currency": "USD",
                    "cd_indicator": "DBIT",
                    "booking_date": "2025-03-18",
                    "value_date": "2025-03-18",
                    "reference": "HMBK-REF-120",
                    "remittance": "Payroll batch",
                    "creditor": "Harmony Payroll",
                },
                {
                    "amount": "+90000.00",
                    "currency": "USD",
                    "cd_indicator": "CRDT",
                    "booking_date": "2025-03-18",
                    "value_date": "2025-03-18",
                    "reference": "HMBK-REF-121",
                    "remittance": "Inbound receipts",
                    "creditor": "Midwest Holdings",
                },
                {
                    "amount": "-17500.50",
                    "currency": "USD",
                    "cd_indicator": "DBIT",
                    "booking_date": "2025-03-18",
                    "value_date": "2025-03-18",
                    "reference": "HMBK-REF-122",
                    "remittance": "Utility settlement",
                    "creditor": "Utility Provider",
                },
            ],
        },
        {
            "filename": "bulk-camt053-latam.xml",
            "msg_id": "C53-LATAM-010",
            "created": "2025-02-28T21:00:00-03:00",
            "statement_id": "LATAM-DAILY-010",
            "iban": "CO1230000000123456789",
            "owner": "Andes Commodities",
            "closing_amount": "780000.00",
            "closing_currency": "USD",
            "closing_date": "2025-02-28",
            "entries": [
                {
                    "amount": "+500000.00",
                    "currency": "USD",
                    "cd_indicator": "CRDT",
                    "booking_date": "2025-02-28",
                    "value_date": "2025-02-28",
                    "reference": "LATAM-REF-010A",
                    "remittance": "Inbound concentrate payment",
                    "creditor": "Lisbon Metals SA",
                },
                {
                    "amount": "-320000.00",
                    "currency": "USD",
                    "cd_indicator": "DBIT",
                    "booking_date": "2025-02-28",
                    "value_date": "2025-02-28",
                    "reference": "LATAM-REF-010B",
                    "remittance": "Shipping costs",
                    "creditor": "Logistics Partner",
                },
            ],
        },
        {
            "filename": "bulk-camt053-uat.xml",
            "msg_id": "C53-UAT-001",
            "created": "2025-03-10T00:00:00Z",
            "statement_id": "UAT-STATEMENT-1",
            "iban": "GB12HMBK40127688990011",
            "owner": "Harmony Treasury UK",
            "closing_amount": "1125000.00",
            "closing_currency": "GBP",
            "closing_date": "2025-03-09",
            "entries": [
                {
                    "amount": "+125000.00",
                    "currency": "GBP",
                    "cd_indicator": "CRDT",
                    "booking_date": "2025-03-09",
                    "value_date": "2025-03-09",
                    "reference": "UAT-REF-001",
                    "remittance": "Inbound FX leg",
                    "creditor": "Test Sender Inc",
                }
            ],
        },
    ]

    for data in camt053_data:
        write_file(data["filename"], build_camt053(data))

    additional_docs = {
        "bulk-camt052-intraday.xml": build_simple(
            """<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.052.001.08">
  <BkToCstmrAcctRpt>
    <GrpHdr>
      <MsgId>INTRADAY-20250320-01</MsgId>
      <CreDtTm>2025-03-20T08:45:00+02:00</CreDtTm>
    </GrpHdr>
    <Rpt>
      <Id>INTRA-01</Id>
      <CreDtTm>2025-03-20T08:30:00+02:00</CreDtTm>
      <Acct>
        <Id>
          <IBAN>IT40X0100501600000001234567</IBAN>
        </Id>
        <Ownr>
          <Nm>AVIO S.P.A.</Nm>
        </Ownr>
      </Acct>
      <Ntry>
        <Amt Ccy="EUR">-45000.00</Amt>
        <CdtDbtInd>DBIT</CdtDbtInd>
        <BookgDt><Dt>2025-03-20</Dt></BookgDt>
        <ValDt><Dt>2025-03-20</Dt></ValDt>
        <AcctSvcrRef>INTRA-REF-01</AcctSvcrRef>
        <NtryDtls>
          <TxDtls>
            <RmtInf><Ustrd>Intraday supplier payout</Ustrd></RmtInf>
          </TxDtls>
        </NtryDtls>
      </Ntry>
    </Rpt>
  </BkToCstmrAcctRpt>
</Document>"""
        ),
        "bulk-camt054-credit.xml": build_simple(
            """<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.054.001.08">
  <BkToCstmrDbtCdtNtfctn>
    <GrpHdr>
      <MsgId>CREDIT-ADV-20250320</MsgId>
      <CreDtTm>2025-03-20T12:05:00+01:00</CreDtTm>
    </GrpHdr>
    <Ntfctn>
      <Id>BNPA-CREDIT-2025-03-20</Id>
      <CreDtTm>2025-03-20T12:00:00+01:00</CreDtTm>
      <Acct>
        <Id><IBAN>FR7610096000301234567890188</IBAN></Id>
        <Ownr><Nm>BNP PARIBAS CHALON</Nm></Ownr>
      </Acct>
      <Ntry>
        <Amt Ccy="EUR">150000.00</Amt>
        <CdtDbtInd>CRDT</CdtDbtInd>
        <BookgDt><Dt>2025-03-20</Dt></BookgDt>
        <ValDt><Dt>2025-03-20</Dt></ValDt>
        <NtryDtls>
          <TxDtls>
            <Refs><TxId>BNPAFRPPCHL-150</TxId></Refs>
            <RmtInf><Ustrd>Credit advice for energy purchase</Ustrd></RmtInf>
          </TxDtls>
        </NtryDtls>
      </Ntry>
    </Ntfctn>
  </BkToCstmrDbtCdtNtfctn>
</Document>"""
        ),
        "bulk-pacs002-reject.md07.xml": build_simple(
            """<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.002.001.12">
  <FIToFIPmtStsRpt>
    <GrpHdr>
      <MsgId>REJECT-MD07-20250321</MsgId>
      <CreDtTm>2025-03-21T11:11:00Z</CreDtTm>
    </GrpHdr>
    <OrgnlGrpInfAndSts>
      <OrgnlMsgId>ASIA-URGENT-001</OrgnlMsgId>
      <OrgnlMsgNmId>pacs.008.001.08</OrgnlMsgNmId>
      <TxSts>RJCT</TxSts>
      <StsRsnInf>
        <Rsn><Cd>MD07</Cd></Rsn>
        <AddtlInf>Beneficiary refused duplicate credit</AddtlInf>
      </StsRsnInf>
    </OrgnlGrpInfAndSts>
    <TxInfAndSts>
      <OrgnlInstrId>TH-PRIO-001</OrgnlInstrId>
      <OrgnlEndToEndId>INV-TH-778</OrgnlEndToEndId>
      <TxSts>RJCT</TxSts>
      <StsRsnInf>
        <Rsn><Cd>MD07</Cd></Rsn>
        <Orgtr><Id><OrgId><BICOrBEI>HMBKTH2BXXX</BICOrBEI></OrgId></Id></Orgtr>
      </StsRsnInf>
    </TxInfAndSts>
  </FIToFIPmtStsRpt>
</Document>"""
        ),
        "bulk-pacs004-return.xml": build_simple(
            """<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.004.001.11">
  <PmtRtr>
    <GrpHdr>
      <MsgId>RETURN-20250321</MsgId>
      <CreDtTm>2025-03-21T12:05:00Z</CreDtTm>
      <TtlRtrdIntrBkSttlmAmt Ccy="USD">25000.00</TtlRtrdIntrBkSttlmAmt>
    </GrpHdr>
    <OrgnlGrpInf>
      <OrgnlMsgId>FX-MULTI-303</OrgnlMsgId>
      <OrgnlMsgNmId>pacs.008.001.08</OrgnlMsgNmId>
    </OrgnlGrpInf>
    <TxInf>
      <OrgnlInstrId>EURO-FX-303</OrgnlInstrId>
      <RtrId>RETURN-EURO-15</RtrId>
      <RtrdIntrBkSttlmAmt Ccy="USD">25000.00</RtrdIntrBkSttlmAmt>
      <ChrgBr>SHA</ChrgBr>
      <RtrRsnInf>
        <Rsn><Cd>AC06</Cd></Rsn>
        <AddtlInf>Closed account</AddtlInf>
      </RtrRsnInf>
    </TxInf>
  </PmtRtr>
</Document>"""
        ),
    }

    for name, xml in additional_docs.items():
        write_file(name, xml)

    print("Sample generation complete.")


if __name__ == "__main__":
    main()
