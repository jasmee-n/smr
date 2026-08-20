# imports
import json
import re
import math
from pathlib import Path
from difflib import SequenceMatcher

# paths
PROJECT_ROOT = Path('/data/home/bt25094/dissertation/smr pipeline')

RESULTS_PATH = PROJECT_ROOT/ 'results'/ 'attempt_2'/ 'evaluation_results_attempt_2.json'
OUTPUT_PATH = PROJECT_ROOT/ 'results'/ 'summary_evaluation.json'

# load results
with RESULTS_PATH.open('r', encoding = 'utf-8') as file:
    results = json.load(file)

def normalise(text):
    if text is None:
        return ''

    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def similar(text_a, text_b, threshold = 0.70):
    a = normalise(text_a)
    b = normalise(text_b)

    if not a or not b:
        return False

    if a in b or b in a:
        return True

    return SequenceMatcher(None, a, b).ratio() >= threshold

def finding_present(finding, summary_text):
    description = finding.get('description', '')

    if similar(description, summary_text, threshold = 0.70):
        return True

    words = [
        word
        for word in normalise(description).split()
        if len(word) > 4
    ]

    matches = sum(
        word in normalise(summary_text)
        for word in words
    )

    return matches >= 2

def wilson_interval(successes, total, z = 1.96):
    if total == 0:
        return 0, 0

    p = successes / total
    denominator = 1 + z ** 2 / total
    centre = (p + z ** 2 / (2 * total)) / denominator

    margin = z * math.sqrt(
        p * (1 - p) / total
        + z ** 2 / (4 * total ** 2)
    ) / denominator

    return round(centre - margin, 3), round(centre + margin, 3)

patient_results = []

total_high_priority = 0
total_high_priority_present = 0
validator_passed = 0
completed = 0

for result in results:
    if result.get('status') != 'completed':
        continue

    completed += 1

    patient_id = result['patient_id']
    state = result['state']

    overview = state.get('overview', '')
    conclusion = state.get('conclusion', '')

    summary_text = f'{overview} {conclusion}'

    ranked_findings = state.get('ranked_findings', [])

    high_priority = [
        item
        for item in ranked_findings
        if item.get('priority_level') == 'HIGH'
    ]

    represented = [
        item
        for item in high_priority
        if finding_present(item, summary_text)
    ]

    completeness = (
        len(represented) / len(high_priority)
        if high_priority
        else 1
    )

    final_validation = state.get('final_validation', {})

    if final_validation.get('status') == 'passed':
        validator_passed += 1

    total_high_priority += len(high_priority)
    total_high_priority_present += len(represented)

    patient_results.append({
        'patient_id': patient_id,
        'high_priority_findings': len(high_priority),
        'high_priority_represented': len(represented),
        'completeness': round(completeness, 3),
        'validator_status': final_validation.get('status'),
        'represented_findings': [
            item.get('description')
            for item in represented
        ],
        'missed_findings': [
            item.get('description')
            for item in high_priority
            if item not in represented
        ]
    })

overall_completeness = (
    total_high_priority_present / total_high_priority
    if total_high_priority > 0
    else 0
)

completeness_95_ci = wilson_interval(
    total_high_priority_present,
    total_high_priority
)

validator_pass_rate = (
    validator_passed / completed
    if completed > 0
    else 0
)

summary_metrics = {
    'completed_patients': completed,
    'high_priority_findings': total_high_priority,
    'high_priority_findings_represented': total_high_priority_present,
    'overall_completeness': round(overall_completeness, 3),
    'completeness_95_ci': list(completeness_95_ci),
    'validator_pass_rate': round(validator_pass_rate, 3),
    'patients': patient_results
}

with OUTPUT_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(summary_metrics, file, indent = 2, ensure_ascii = False)

print('\nFINAL REPORT QUALITY')
print('-' * 50)

print(
    f'HIGH-PRIORITY FINDINGS REPRESENTED: '
    f'{total_high_priority_present}/{total_high_priority}'
)

print(f'COMPLETENESS: {overall_completeness:.3f}')
print(f'95% CI: {completeness_95_ci}')
print(f'VALIDATOR PASS RATE: {validator_pass_rate:.3f}')

print(f'\nSAVED TO: {OUTPUT_PATH}')