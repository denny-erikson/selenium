import json
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import re


env_dir = os.path.expanduser("~")
download_dir = os.path.join(env_dir, 'Downloads')

project_dir = os.path.dirname(os.path.abspath(__file__))
destination_dir = os.path.join(project_dir, 'files')

# Dicionário para mapeamento de months em português
months = {
    '01': 'JANEIRO', '02': 'FEVEREIRO', '03': 'MARÇO',
    '04': 'ABRIL', '05': 'MAIO', '06': 'JUNHO',
    '07': 'JULHO', '08': 'AGOSTO', '09': 'SETEMBRO',
    '10': 'OUTUBRO', '11': 'NOVEMBRO', '12': 'DEZEMBRO'
}

# Dicionário para mapeamento de filiais com base no CNPJ
cnpj_branches = {
    '62438841000132': "NR SAM",
    '62438841000647': "NR SAP",
    '62438841000485': "NR SP"
}

# Função para criar o caminho baseado no XML
def extract_and_create_path(xml_path, destination_dir):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def find_cpf_or_cnpj(path):
      return root.find(f'{path}CPF').text if root.find(f'{path}CPF') is not None else root.find(f'{path}CNPJ').text if root.find(f'{path}CNPJ') is not None else None


    cnpj_receiver = root.find('.//{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}CNPJ').text
    cnpj_provider = find_cpf_or_cnpj('.//{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}')
    corporate_reason = root.find('.//{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}xNome').text
    invoice_number = root.find('.//{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}nNF').text
    issue_date = root.find('.//{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}dhEmi').text

    corporate_reason = re.sub(r'[^a-zA-Z0-9]', ' ', corporate_reason)

    issue_date = datetime.fromisoformat(issue_date)
    month_in_portuguese = months[issue_date.strftime("%m")]
    formatted_date = f"{issue_date.strftime('%Y')}/{month_in_portuguese}/{issue_date.strftime('%d')}"

    branch = cnpj_branches.get(cnpj_receiver[:14], "Outra Filial")
    folder_name = f"NF {invoice_number} - {corporate_reason}"
    file_name = f"NF {invoice_number} - {corporate_reason}.xml"
    full_path = os.path.join(destination_dir, branch, formatted_date, folder_name, file_name)
    payload = {
        "cnpj_receiver": cnpj_receiver,
        "cnpj_provider": cnpj_provider,
        "corporate_reason": corporate_reason,
        "invoice_number": invoice_number,
        "issue_date": formatted_date,
        "branch": branch
    }

    return full_path, invoice_number, corporate_reason, payload


full_path, invoice_number, corporate_reason, payload = extract_and_create_path(r'files\\31240916907746000113558900452757091979903950.xml', destination_dir)

print(f"""
    [full_path]: {full_path}

    [invoice_number]: {invoice_number}

    [corporate_reason]: {corporate_reason}

    [payload]: {json.dumps(payload, indent=4)}
""")