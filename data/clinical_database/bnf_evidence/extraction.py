import json
import re
from pathlib import Path

import pymupdf

# paths
BASE_PATH = Path('/data/home/bt25094/dissertation/smr pipeline/data/clinical_database/bnf_evidence')

BNF_PDF_PATH = BASE_PATH / 'bnf_85.pdf'
BNF_OUTPUT_PATH = BASE_PATH / 'bnf_evidence.json'

START_PAGE = 1534
END_PAGE = 1778

# severity mapping
SEVERITY_MAP = {
    'r': 'severe',
    'o': 'moderate',
    'n': 'mild'
}

# text cleaning
def clean_text(text):
    return ' '.join(str(text).split()).strip()

def is_unwanted_line(line):
    line = clean_text(line).lower()

    unwanted = [
        'https://www.facebook.com/codemedicalapps/',
        '(books-courses-medical applications)',
        'algrawany',
        'interactions | appendix 1',
        'appendix 1 interactions',
        'bnf 85'
    ]

    if not line:
        return True

    if line == 'a1':
        return True

    if line.isdigit():
        return True

    return any(
        text in line
        for text in unwanted
    )

def save_json(data, path):
    with path.open('w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 2, ensure_ascii = False)

# page extraction
def extract_pages():
    document = pymupdf.open(str(BNF_PDF_PATH))

    lines = []

    for page_number in range(
        START_PAGE,
        END_PAGE + 1
    ):
        page = document[page_number - 1]

        text = page.get_text(
            'text',
            sort = False
        ) or ''

        for raw_line in text.splitlines():
            line = clean_text(raw_line)

            if is_unwanted_line(line):
                continue

            lines.append(
                {
                    'line': line,
                    'raw_line': raw_line,
                    'page': page_number
                }
            )

    document.close()

    return lines

# table extraction
def get_table_number(line):
    match = re.match(
        r'^Table\s*(\d{1,2})\b',
        line,
        flags = re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None

def extract_tables(lines):
    tables = []
    current = None

    for item in lines:
        line = item['line']

        if 'list of drug interactions' in line.lower():
            break

        table_number = get_table_number(line)

        if table_number:
            if current:
                tables.append(current)

            title = re.sub(
                r'^Table\s*\d{1,2}\s*',
                '',
                line,
                flags = re.IGNORECASE
            )

            current = {
                'table_number': table_number,
                'effect': clean_text(title).lower(),
                'text': [],
                'bnf_page': item['page']
            }

            continue

        if current:
            current['text'].append(item['raw_line'])

    if current:
        tables.append(current)

    for table in tables:
        explanation = []
        drugs = []

        for raw_line in table['text']:
            parts = [
                clean_text(part).lower()
                for part in re.split(
                    r'\s{2,}|\t+|,\s*',
                    raw_line
                )
                if clean_text(part)
            ]

            if len(parts) > 1:
                drugs.extend(parts)

            elif parts:
                text = parts[0]

                if (
                    text.endswith('.')
                    or len(text) > 70
                ):
                    explanation.append(text)

                else:
                    drugs.append(text)

        table['explanation'] = clean_text(' '.join(explanation))

        table['drugs'] = list(dict.fromkeys(drugs))

        del table['text']

    unique_tables = {}

    for table in tables:
        number = table['table_number']

        existing = unique_tables.get(number)

        if (
            existing is None
            or len(table['drugs']) > len(existing['drugs'])
        ):
            unique_tables[number] = table

    return [
        unique_tables[number]
        for number in sorted(
            unique_tables
        )
    ]

# interaction extraction
def get_metadata(text):
    match = re.search(
        r'\b([ron])\s+'
        r'(study|anecdotal|theoretical)\b',
        text,
        flags = re.IGNORECASE
    )

    if not match:
        return 'unknown', None

    return (
        SEVERITY_MAP[match.group(1).lower()],
        match.group(2).lower()
    )

def get_table_references(text):
    references = re.findall(
        r'\btable\s*(\d{1,2})',
        text,
        flags = re.IGNORECASE
    )

    return list(
        dict.fromkeys(
            f'table {number}'
            for number in references
        )
    )

def clean_interaction_text(text):
    text = re.sub(
        r'\b[ron]\s+'
        r'(study|anecdotal|theoretical)\b',
        '',
        text,
        flags = re.IGNORECASE
    )

    text = re.sub(
        r'\s*→?\s*(?:also\s+)?see\s+'
        r'table\s*\d{1,2}'
        r'(?:\s+p\.\s*\d+)?',
        '',
        text,
        flags = re.IGNORECASE
    )

    return clean_text(text)

def get_specific_drug(value):
    if not value:
        return value

    match = re.search(
        r'\(([^)]+)\)',
        value
    )

    if match:
        return clean_text(match.group(1))

    return clean_text(value)

def get_drugs(text):

    match = re.search(
        r'^(.*?)\s+can\s+cause.*?,\s+as\s+can\s+'
        r'(.+?)(?:;|\.|$)',
        text,
        flags = re.IGNORECASE
    )

    if match:
        return (
            clean_text(match.group(1)),
            clean_text(match.group(2))
        )

    match = re.search(
        r'^(.*?)\s+.*?\bwhen given with\s+'
        r'(.+?)(?:[.;]|$)',
        text,
        flags = re.IGNORECASE
    )

    if match:
        return (
            clean_text(match.group(1)),
            clean_text(match.group(2))
        )

    match = re.search(
        r'^Avoid\s+(?:concomitant\s+use\s+of\s+)?'
        r'(.+?)\s+(?:in patients taking|with)\s+'
        r'(.+?)(?:[.;]|$)',
        text,
        flags = re.IGNORECASE
    )

    if match:
        return (
            clean_text(match.group(1)),
            clean_text(match.group(2))
        )

    match = re.search(
        r'^(.*?)\s+'
        r'(?:is\s+predicted\s+to\s+|'
        r'are\s+predicted\s+to\s+|'
        r'has\s+been\s+reported\s+to\s+|'
        r'potentially\s+|'
        r'might\s+|'
        r'may\s+)?'
        r'(?:increase|increases|'
        r'decrease|decreases|'
        r'alter|alters|'
        r'affect|affects|'
        r'enhance|enhances|'
        r'oppose|opposes|'
        r'reduce|reduces|'
        r'cause|causes|'
        r'prolong|prolongs)'
        r'.*?\b(?:of|to)\s+'
        r'(.+?)(?:[.;]|$)',
        text,
        flags = re.IGNORECASE
    )

    if match:
        return (
            clean_text(match.group(1)),
            clean_text(match.group(2))
        )

    match = re.search(
        r'^(.*?)\s+.*?\b(?:efficacy|effect)\s+'
        r'(.+?)(?:[.;]|$)',
        text,
        flags = re.IGNORECASE
    )

    if match:
        return (
            clean_text(match.group(1)),
            clean_text(match.group(2))
        )

    match = re.search(
        r'^(?:With\s+standard-release\s+)?'
        r'(some orally administered drugs).*?'
        r'(exenatide|lixisenatide)',
        text,
        flags = re.IGNORECASE
    )

    if match:
        return (
            clean_text(match.group(1)),
            clean_text(match.group(2))
        )

    match = re.search(
        r'^(.*?)\s+.*?\bwith\s+'
        r'(.+?)(?:[.;]|$)',
        text,
        flags = re.IGNORECASE
    )

    if match:
        return (
            clean_text(match.group(1)),
            clean_text(match.group(2))
        )

    return None, None

def create_interaction_record(text, page):
    severity, evidence = get_metadata(text)
    table_references = get_table_references(text)

    interaction_text = clean_interaction_text(text)

    drug_a, drug_b = get_drugs(interaction_text)
    drug_a = get_specific_drug(drug_a)
    drug_b = get_specific_drug(drug_b)

    return {
        'drug_or_class_a': drug_a,
        'drug_or_class_b': drug_b,
        'interaction': interaction_text,
        'severity': severity,
        'evidence': evidence,
        'table_references': table_references,
        'bnf_page': page
    }


def extract_interactions(lines):
    interactions = []

    started = False
    current = ''
    current_page = None

    for item in lines:
        line = item['line']

        if not started:
            if (
                'list of drug interactions'
                in line.lower()
            ):
                started = True

            continue

        sections = line.split('▶')

        if (
            sections[0].strip()
            and current
        ):
            current += (' ' + sections[0].strip())

        for section in sections[1:]:
            if current:
                interactions.append(create_interaction_record(current, current_page))

            current = section.strip()
            current_page = item['page']

    if current:
        interactions.append(
            create_interaction_record(current, current_page))

    for number, interaction in enumerate(interactions, start = 0):
        interaction['interaction_id'] = (f'BNF_{number}')

    return interactions

# evidence extraction
lines = extract_pages()

tables = extract_tables(lines)
interactions = extract_interactions(lines)

# extraction output
bnf_evidence = {
    'tables': tables,
    'interactions': interactions
}

save_json(bnf_evidence, BNF_OUTPUT_PATH)
