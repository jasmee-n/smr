# imports
import json
import re
from pathlib import Path
from difflib import SequenceMatcher

# paths
PROJECT_ROOT = Path('/data/home/bt25094/dissertation/smr pipeline')

RESULTS_PATH = PROJECT_ROOT/ 'results'/ 'attempt_2'/ 'evaluation_results_attempt_2.json'

REFERENCE_PATH = PROJECT_ROOT/ 'data'/ 'datasets'/ 'evaluation'/ 'evaluation_reference.json'

LOG1_PATH = PROJECT_ROOT/ 'results'/ 'attempt_1'/ 'execution_log_attempt_1.json'
LOG2_PATH = PROJECT_ROOT/ 'results'/ 'attempt_2'/ 'execution_log_attempt_2.json'

OUTPUT_PATH = PROJECT_ROOT/ 'results'/ 'evaluation_metrics.json'
VALIDATION_PATH = PROJECT_ROOT/ 'results'/ 'matching_validation.json'

# load files
with RESULTS_PATH.open('r', encoding = 'utf-8') as file:
    results = json.load(file)

with REFERENCE_PATH.open('r', encoding = 'utf-8') as file:
    evaluation_reference = json.load(file)

with LOG1_PATH.open('r', encoding = 'utf-8') as file:
    log1 = json.load(file)

with LOG2_PATH.open('r', encoding = 'utf-8') as file:
    log2 = json.load(file)

reference_map = {
    patient['patient_id']: patient
    for patient in evaluation_reference
}

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

def medication_name(text):
    text = normalise(text)

    parts = text.split()
    name = []

    for part in parts:
        if any(character.isdigit() for character in part):
            break

        name.append(part)

    return ' '.join(name)

def calculate_metrics(tp, fp, fn):
    precision = (
        tp / (tp + fp) 
        if (tp + fp) > 0 
        else 0
    )
    recall = (
        tp / (tp + fn) 
        if (tp + fn) > 0 
        else 0
    )
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return {
        'tp': tp,
        'fp': fp,
        'fn': fn,
        'precision': round(precision, 3),
        'recall': round(recall, 3),
        'f1': round(f1, 3)
    }

def execution_metrics(log):
    completed = sum(item['status'] == 'completed' for item in log)
    failed = sum(item['status'] == 'failed' for item in log)

    return {
        'total': len(log),
        'completed': completed,
        'failed': failed,
        'success_rate': round(completed / len(log), 3)
    }

def clinical_category(text):
    text = normalise(text)

    if 'hyperkalaemia' in text or 'hyperkalemia' in text:
        return 'hyperkalaemia'

    if 'hypokalaemia' in text or 'hypokalemia' in text:
        return 'hypokalaemia'

    if 'hyponatraemia' in text or 'hyponatremia' in text:
        return 'hyponatraemia'

    if 'hypotension' in text:
        return 'hypotension'

    if 'bradycardia' in text:
        return 'bradycardia'

    if 'anticholinergic' in text or 'antimuscarinic' in text:
        return 'anticholinergic'

    if 'antiplatelet' in text or 'bleeding' in text:
        return 'antiplatelet'

    if 'anticoagulant' in text:
        return 'anticoagulant'

    if 'serotonin' in text:
        return 'serotonin'

    if 'qt' in text:
        return 'qt'

    if 'hypoglycaemia' in text or 'hypoglycemia' in text:
        return 'hypoglycaemia'

    if 'renal' in text or 'kidney' in text or 'nephro' in text:
        return 'renal'

    if 'hepat' in text or 'liver' in text:
        return 'hepatotoxicity'

    if 'cns' in text or 'central nervous' in text or 'sedation' in text:
        return 'cns_depression'

    return text

def monitoring_category(text):
    text = normalise(text)

    if 'potassium' in text and (
        'renal' in text
        or 'kidney' in text
        or 'egfr' in text
    ):
        return 'potassium_renal'

    if 'potassium' in text:
        return 'potassium'

    if 'sodium' in text:
        return 'sodium'

    if 'renal' in text or 'kidney' in text or 'egfr' in text:
        return 'renal'

    if 'ecg' in text or 'qt' in text:
        return 'ecg'

    if 'glucose' in text or 'hba1c' in text:
        return 'glucose'

    return text

def reason_category(text):
    text = normalise(text)

    if 'duplicate' in text:
        return 'duplicate'

    if 'hyperkalaemia' in text or 'hyperkalemia' in text:
        return 'hyperkalaemia'

    if 'hypokalaemia' in text or 'hypokalemia' in text:
        return 'hypokalaemia'

    if 'hyponatraemia' in text or 'hyponatremia' in text:
        return 'hyponatraemia'

    if 'hypoglycaemia' in text or 'hypoglycemia' in text:
        return 'hypoglycaemia'

    if 'qt' in text:
        return 'qt'

    if 'egfr' in text or 'renal' in text or 'kidney' in text or 'nephro' in text:
        return 'renal'

    if 'bleeding' in text:
        return 'bleeding'

    if 'fall' in text:
        return 'falls'

    return text

def match_indication(predicted, expected):
    predicted_medication = normalise(predicted.get('medication_name'))
    predicted_indication = normalise(predicted.get('indication'))

    expected_medication = normalise(expected.get('medication'))
    expected_indications = expected.get('acceptable_indications', [])

    medication_match = (
        predicted_medication == expected_medication
        or predicted_medication in expected_medication
        or expected_medication in predicted_medication
    )

    indication_match = any(
        similar(predicted_indication, indication)
        for indication in expected_indications
    )

    return medication_match and indication_match

def match_interaction(predicted, expected):
    predicted_pair = {
        medication_name(predicted.get('drug_a')),
        medication_name(predicted.get('drug_b'))
    }

    expected_pair = {
        medication_name(expected.get('drug_a')),
        medication_name(expected.get('drug_b'))
    }

    if predicted_pair != expected_pair:
        return False

    expected_effect = expected.get('effect')

    if not expected_effect:
        return True

    predicted_effect = clinical_category(
        predicted.get('rationale', '')
    )

    expected_effect = clinical_category(
        expected_effect
    )

    return predicted_effect == expected_effect

def match_risk(predicted, expected):
    predicted_risk = clinical_category(
        predicted.get('risk_type', '')
    )

    expected_risk = clinical_category(expected.get('risk_type', expected.get('effect', '')))

    if predicted_risk != expected_risk:
        return False

    expected_medications = [
        normalise(medication)
        for medication in expected.get('medications', [])
    ]

    predicted_text = normalise(
        f'{predicted.get('medications', '')}'
        f'{predicted.get('rationale', '')}'
    )

    if not expected_medications:
        return True

    medication_matches = sum(
        medication in predicted_text
        for medication in expected_medications
    )

    required_matches = min(2, len(expected_medications))

    return medication_matches >= required_matches

def match_deprescribing(predicted, expected):
    predicted_medication = medication_name(predicted.get('medication', ''))
    expected_medication = medication_name(expected.get('medication', ''))

    predicted_reason = (
        predicted.get('issue', '')
        or predicted.get('rationale', '')
    )
    expected_reason = expected.get('reason', '')

    medication_match = predicted_medication == expected_medication
    reason_match = reason_category(predicted_reason)== reason_category(expected_reason)

    return medication_match and reason_match

def match_monitoring(predicted, expected):
    predicted_monitoring = monitoring_category(predicted.get('monitoring_required', ''))
    expected_monitoring = monitoring_category(expected.get('monitoring_required', ''))

    predicted_reason = reason_category(predicted.get('rationale', ''))
    expected_reason = reason_category(expected.get('reason', ''))

    monitoring_match = predicted_monitoring == expected_monitoring

    reason_match = predicted_reason == expected_reason
    
    return monitoring_match and reason_match

def match_recommendation(predicted, expected):
    predicted_recommendation = normalise(predicted.get('recommendation', ''))

    predicted_rationale = predicted.get('rationale', '')

    expected_reason = expected.get('reason', '')

    if expected.get('recommendation_type') == 'medication_review':
        medication = normalise(expected.get('medication', ''))
    
        review_terms = [
            'stop',
            'discontinue',
            'deprescribe',
            'reduce',
            'review',
            'avoid',
            'switch'
        ]

        start_terms = [
            'initiate',
            'start',
            'commence'
        ]

        medication_match = (medication in predicted_recommendation)

        action_match = (
            any(
                term in predicted_recommendation
                for term in review_terms
            )
            and not any(
                term in predicted_recommendation
                for term in start_terms
            )
        )

        reason_match = reason_category(predicted_rationale) == reason_category(expected_reason)

        return (
            medication_match
            and action_match
            and reason_match
        )

    predicted_action = monitoring_category(predicted_recommendation)
    expected_action = monitoring_category(expected.get('action', ''))
    
    predicted_reason = reason_category(predicted_rationale)
    expected_reason = reason_category(expected_reason)

    action_match = predicted_action == expected_action
    reason_match = predicted_reason == expected_reason

    monitoring_action = (
        'monitor' in predicted_recommendation
        or 'check' in predicted_recommendation
    )

    return (
        action_match
        and reason_match
        and monitoring_action
    )

def compare_findings(predicted, expected, matcher):
    matched_expected = set()
    tp = 0
    fp = 0

    for predicted_item in predicted:
        match_found = False

        for expected_index, expected_item in enumerate(expected):
            if expected_index in matched_expected:
                continue

            if matcher(predicted_item, expected_item):
                tp += 1
                matched_expected.add(expected_index)
                match_found = True
                break

        if not match_found:
            fp += 1

    fn = len(expected) - len(matched_expected)

    return tp, fp, fn

def validation_examples(predicted, expected, matcher, limit = 5):
    matched = []
    missed = []
    matched_expected = set()

    for predicted_item in predicted:
        for expected_index, expected_item in enumerate(expected):
            if expected_index in matched_expected:
                continue

            if matcher(predicted_item, expected_item):
                matched.append({
                    'predicted': predicted_item,
                    'expected': expected_item
                })

                matched_expected.add(expected_index)
                break

    for expected_index, expected_item in enumerate(expected):
        if expected_index not in matched_expected:
            missed.append(expected_item)

    return {
        'matched': matched[:limit],
        'missed': missed[:limit]
    }

agents = {
    'indications': {'tp': 0, 'fp': 0, 'fn': 0},
    'interactions': {'tp': 0, 'fp': 0, 'fn': 0},
    'risks': {'tp': 0, 'fp': 0, 'fn': 0},
    'deprescribing': {'tp': 0, 'fp': 0, 'fn': 0},
    'monitoring': {'tp': 0, 'fp': 0, 'fn': 0},
    'recommendations': {'tp': 0, 'fp': 0, 'fn': 0}
}

validation = {
    'indications': {'matched': [], 'missed': []},
    'interactions': {'matched': [], 'missed': []},
    'risks': {'matched': [], 'missed': []},
    'deprescribing': {'matched': [], 'missed': []},
    'monitoring': {'matched': [], 'missed': []},
    'recommendations': {'matched': [], 'missed': []}
}

matchers = {
    'indications': match_indication,
    'interactions': match_interaction,
    'risks': match_risk,
    'deprescribing': match_deprescribing,
    'monitoring': match_monitoring,
    'recommendations': match_recommendation
}

completed_patients = 0
failed_patients = 0

for result in results:
    patient_id = result['patient_id']

    if result.get('status') != 'completed':
        failed_patients += 1
        continue

    if patient_id not in reference_map:
        print(f'WARNING: NO REFERENCE STANDARD FOR {patient_id}')
        continue

    completed_patients += 1

    state = result['state']
    reference = reference_map[patient_id]

    predicted_data = {
        'indications': state.get('indications', {}).get('indications', []),
        'interactions': state.get('interactions', {}).get('interactions', []),
        'risks': state.get('risks', {}).get('risks', []),
        'deprescribing': state.get('deprescribing', {}).get('deprescribing', []),
        'monitoring': state.get('monitoring', {}).get('monitoring', []),
        'recommendations': state.get('recommendations', {}).get('recommendations', [])
    }

    expected_data = {
        'indications': [
            item
            for item in reference.get('expected_indications', [])
            if item.get('acceptable_indications')
        ],
        'interactions': reference.get('expected_interactions', []),
        'risks': reference.get('expected_risks', []),
        'deprescribing': reference.get('expected_deprescribing', []),
        'monitoring': reference.get('expected_monitoring', []),
        'recommendations': reference.get('expected_recommendations', [])
    }

    for agent in agents:
        predicted = predicted_data[agent]
        expected = expected_data[agent]
        matcher = matchers[agent]

        tp, fp, fn = compare_findings(predicted, expected, matcher)

        agents[agent]['tp'] += tp
        agents[agent]['fp'] += fp
        agents[agent]['fn'] += fn

        examples = validation_examples(predicted, expected, matcher)

        for item in examples['matched']:
            if len(validation[agent]['matched']) < 5:
                validation[agent]['matched'].append({
                    'patient_id': patient_id,
                    'predicted': item['predicted'],
                    'expected': item['expected']
                })

        for item in examples['missed']:
            if len(validation[agent]['missed']) < 5:
                validation[agent]['missed'].append({
                    'patient_id': patient_id,
                    'expected': item
                })

# metrics
clinical_metrics = {
    agent: calculate_metrics(**counts)
    for agent, counts in agents.items()
    if agent in ['indications', 'interactions']
}

target_detection = {
    agent: {
        'detected': counts['tp'],
        'expected': counts['tp'] + counts['fn'],
        'recall': round(
            counts['tp'] / (counts['tp'] + counts['fn']),
            3
        ) if (counts['tp'] + counts['fn']) > 0 else 0
    }
    for agent, counts in agents.items()
    if agent in ['risks', 'deprescribing', 'monitoring', 'recommendations']
}

micro_tp = sum(
    agents[agent]['tp']
    for agent in ['indications', 'interactions']
)

micro_fp = sum(
    agents[agent]['fp']
    for agent in ['indications', 'interactions']
)

micro_fn = sum(
    agents[agent]['fn']
    for agent in ['indications', 'interactions']
)

micro_metrics = calculate_metrics(micro_tp, micro_fp, micro_fn)

macro_metrics = {
    'precision': round(
        sum(
            item['precision']
            for item in clinical_metrics.values()
        ) / len(clinical_metrics), 3
    ),

    'recall': round(
        sum(
            item['recall']
            for item in clinical_metrics.values()
        ) / len(clinical_metrics), 3
    ),

    'f1': round(
        sum(
            item['f1']
            for item in clinical_metrics.values()
        ) / len(clinical_metrics), 3
    )
}

attempt_1 = execution_metrics(log1)
attempt_2 = execution_metrics(log2)

metrics = {
    'execution_reliability': {
        'attempt_1': attempt_1,
        'attempt_2': attempt_2
    },

    'clinical_evaluation_attempt_2': {
        'completed_patients': completed_patients,
        'failed_patients': failed_patients,
        'metrics': clinical_metrics,
        'target_detection': target_detection,
        'micro_metrics': micro_metrics,
        'macro_metrics': macro_metrics
    }
}

OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)

with OUTPUT_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(metrics, file, indent = 2, ensure_ascii = False)

with VALIDATION_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(validation, file, indent = 2, ensure_ascii = False)
    
print('\nEXECUTION RELIABILITY:')
print('-' * 50)

print(
    f'ATTEMPT 1: '
    f'{attempt_1['completed']}/{attempt_1['total']}'
    f'({attempt_1['success_rate']:.1%})'
)

print(
    f'ATTEMPT 2: '
    f'{attempt_2['completed']}/{attempt_2['total']}'
    f'({attempt_2['success_rate']:.1%})'
)

print('\nCLINICAL PERFORMANCE:')
print('-' * 50)

for agent, metric in clinical_metrics.items():
    print(
        f'{agent.upper():20}'
        f'P={metric['precision']:.3f} '
        f'R={metric['recall']:.3f} '
        f'F1={metric['f1']:.3f} '
        f'TP={metric['tp']} '
        f'FP={metric['fp']} '
        f'FN={metric['fn']}'
    )

print('\nTARGET FINDING DETECTION:')
print('-' * 50)

for agent, metric in target_detection.items():
    print(
        f'{agent.upper():20} '
        f'R={metric['recall']:.3f}  '
        f'DETECTED={metric['detected']}/{metric['expected']}'
    )

print('\nMICRO PERFORMANCE:')
print('-' * 50)

print(f'PRECISION: {micro_metrics['precision']:.3f}')
print(f'RECALL: {micro_metrics['recall']:.3f}')
print(f'F1: {micro_metrics['f1']:.3f}')

print('\nMACRO PERFORMANCE:')
print('-' * 50)

print(f'PRECISION: {macro_metrics['precision']:.3f}')
print(f'RECALL: {macro_metrics['recall']:.3f}')
print(f'F1: {macro_metrics['f1']:.3f}')

print(f'\nMETRICS SAVED TO: {OUTPUT_PATH}')
print(f'VALIDATION SAVED TO: {VALIDATION_PATH}')