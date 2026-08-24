import json
import re
from pathlib import Path

from pypdf import PdfReader


# paths
BASE_PATH = Path('/data/home/bt25094/dissertation/smr pipeline/data/clinical_database/stopp_start_evidence')

PDF_PATH = BASE_PATH / 'stopp_start.pdf'
OUTPUT_PATH = BASE_PATH / 'stopp_start_criteria.json'

# text clean
def clean_text(text):
    return ' '.join(text.split()).strip()

# framework extraction
def get_framework(line):
    line = line.lower()

    if 'stopp' in line and 'screening tool' in line:
        return 'STOPP'

    if 'start' in line and 'screening tool' in line:
        return 'START'

    return None

# section extraction
def get_section(line):
    match = re.match(
        r'^Section\s+([A-Z])\s*[:.]\s*(.+)',
        line,
        flags = re.IGNORECASE
    )

    if not match:
        return None

    return {
        'code': match.group(1).upper(),
        'title': match.group(2).strip()
    }

# criterion extraction
def get_criterion(line):
    match = re.match(
        r'^(\d+)\.\s*(.+)',
        line
    )

    if not match:
        return None

    return {
        'number': int(
            match.group(1)
        ),
        'text': match.group(2).strip()
    }

# PDF extraction
reader = PdfReader(
    str(PDF_PATH)
)

criteria = []

framework = None
section = None
current = None

for page_number, page in enumerate(
    reader.pages,
    start = 1
):
    text = page.extract_text() or ''

    for raw_line in text.splitlines():

        line = clean_text(
            raw_line
        )

        if not line:
            continue

        new_framework = get_framework(
            line
        )

        if new_framework:
            framework = new_framework
            continue

        new_section = get_section(
            line
        )

        if new_section:
            section = new_section
            continue

        new_criterion = get_criterion(
            line
        )

        if new_criterion and framework and section:

            if current:
                criteria.append(
                    current
                )

            current = {
                'framework': framework,
                'section': section['code'],
                'section_title': section['title'],
                'criterion_number': new_criterion['number'],
                'criterion': new_criterion['text'],
                'page': page_number
            }

            continue

        if current:
            current['criterion'] += ' ' + line

if current:
    criteria.append(current)

# extraction output
with OUTPUT_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(criteria, file, indent = 2, ensure_ascii = False)

print(f'CRITERIA EXTRACTED: {len(criteria)}')
print(f'SAVED TO: {OUTPUT_PATH}')
