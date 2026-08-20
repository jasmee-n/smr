import json
from pathlib import Path
from itertools import combinations

from libraries import *

# paths
PROJECT_ROOT = Path('/data/home/bt25094/dissertation/smr pipeline')

EVALUATION_PATH = PROJECT_ROOT / 'data' / 'datasets' / 'evaluation'
CLINICAL_DATABASE_PATH = PROJECT_ROOT / 'data' / 'clinical_database'

PATIENTS_PATH = EVALUATION_PATH / 'evaluation_patients.json'
GROUND_TRUTH_PATH = EVALUATION_PATH / 'evaluation_reference.json'

BNF_PATH = CLINICAL_DATABASE_PATH/ 'bnf_evidence'/ 'bnf_evidence.json'
STOPP_START_PATH = CLINICAL_DATABASE_PATH/'stopp_start_evidence'/ 'stopp_start_evidence.json'

OUTPUT_PATH = EVALUATION_PATH / 'evaluation_reference.json'

with PATIENTS_PATH.open('r', encoding='utf-8') as file:
    patients = json.load(file)

with GROUND_TRUTH_PATH.open('r', encoding='utf-8') as file:
    scenarios = json.load(file)

with BNF_PATH.open('r', encoding='utf-8') as file:
    bnf = json.load(file)

with STOPP_START_PATH.open('r', encoding='utf-8') as file:
    stopp_start = json.load(file)

scenario_map = {
    item['patient_id']: item
    for item in scenarios
}

def normalise(text):
    return str(text).strip().lower()

def medication_name(medication):
    parts = medication.split()
    name = []

    for part in parts:
        if any(character.isdigit() for character in part):
            break
        name.append(part)

    return ' '.join(name)

def patient_medication_names(patient):
    return [
        medication_name(medication)
        for medication in patient.get('raw_medications', [])
    ]

INDICATION_LOOKUP = {}

for condition, medications in CONDITION_MEDICATIONS.items():
    for medication in medications:
        name = normalise(medication_name(medication))
        INDICATION_LOOKUP.setdefault(name, []).append(condition)

TABLE_EFFECTS = {
    1: 'hepatotoxicity',
    2: 'nephrotoxicity',
    3: 'anticoagulant_effects',
    4: 'antiplatelet_effects',
    6: 'bradycardia',
    8: 'hypotension',
    9: 'qt_prolongation',
    10: 'anticholinergic_burden',
    11: 'cns_depression',
    13: 'serotonin_syndrome',
    14: 'hypoglycaemia',
    16: 'hyperkalaemia',
    17: 'hypokalaemia',
    18: 'hyponatraemia'
}

def get_indications(patient):
    conditions = set(patient.get('conditions', []))
    results = []

    for medication in patient_medication_names(patient):
        possible = [
            condition
            for condition in INDICATION_LOOKUP.get(
                normalise(medication),
                []
            )
            if condition in conditions
        ]

        results.append({
            'medication': medication,
            'expected_indication': possible[0] if possible else 'unclear',
            'acceptable_indications': possible
        })

    return results

def get_interactions(patient):
    medication_names = patient_medication_names(patient)
    medication_names_lower = {
        normalise(name): name
        for name in medication_names
    }

    results = []

    for interaction in bnf['interactions']:
        drug_a = normalise(
            interaction.get('drug_or_class_a') or ''
        )
        drug_b = normalise(
            interaction.get('drug_or_class_b') or ''
        )
        interaction_text = normalise(
            interaction.get('interaction') or ''
        )

        matched = [
            original
            for name, original in medication_names_lower.items()
            if (
                name in drug_a
                or name in drug_b
                or name in interaction_text
            )
        ]

        if len(set(matched)) >= 2:
            pair = sorted(set(matched), key=str.lower)[:2]

            results.append({
                'drug_a': pair[0],
                'drug_b': pair[1],
                'severity': interaction.get('severity'),
                'source': 'BNF interaction',
                'interaction_id': interaction.get('interaction_id')
            })

    for table in bnf['tables']:
        table_number = table.get('table_number')

        if table_number not in TABLE_EFFECTS:
            continue

        table_drugs = {
            normalise(drug)
            for drug in table.get('drugs', [])
        }

        matched = [
            medication
            for medication in medication_names
            if normalise(medication) in table_drugs
        ]

        if len(matched) >= 2:
            for drug_a, drug_b in combinations(sorted(set(matched)), 2):
                results.append({
                    'drug_a': drug_a,
                    'drug_b': drug_b,
                    'severity': 'moderate',
                    'source': f'BNF table {table_number}',
                    'effect': TABLE_EFFECTS[table_number]
                })

    unique = {}

    for item in results:
        key = tuple(sorted([
            normalise(item['drug_a']),
            normalise(item['drug_b'])
        ])) + (item.get('effect', item.get('interaction_id')),)

        unique[key] = item

    return list(unique.values())

def get_risks(patient):
    medication_names = patient_medication_names(patient)
    results = []

    for table in bnf['tables']:
        table_number = table.get('table_number')

        if table_number not in TABLE_EFFECTS:
            continue

        table_drugs = {
            normalise(drug)
            for drug in table.get('drugs', [])
        }

        matched = [
            medication
            for medication in medication_names
            if normalise(medication) in table_drugs
        ]

        if len(matched) >= 2:
            results.append({
                'risk_type': TABLE_EFFECTS[table_number],
                'severity': 'moderate',
                'medications': sorted(set(matched)),
                'source': f'BNF table {table_number}'
            })
        
    egfr = patient.get('egfr')

    if egfr is not None:
        medications_lower = {
            normalise(medication)
            for medication in medication_names
        }

        if egfr < 50 and 'naproxen' in medications_lower:
            results.append({
                'risk_type': 'renal_impairment',
                'severity': 'high',
                'medications': ['Naproxen'],
                'source': 'STOPP E4'
            })

        if egfr < 30 and 'metformin' in medications_lower:
            results.append({
                'risk_type': 'metformin_in_severe_renal_impairment',
                'severity': 'high',
                'medications': ['Metformin'],
                'source': 'STOPP E6'
            })

        if egfr < 30 and 'spironolactone' in medications_lower:
            results.append({
                'risk_type': 'hyperkalaemia',
                'severity': 'high',
                'medications': ['Spironolactone'],
                'source': 'STOPP E7'
            })

    return results

def get_deprescribing(patient):
    medication_names = patient_medication_names(patient)
    medications_lower = [
        normalise(medication)
        for medication in medication_names
    ]

    findings = []
    
    duplicates = {
        medication
        for medication in medications_lower
        if medications_lower.count(medication) > 1
    }

    for medication in sorted(duplicates):
        findings.append({
            'medication': medication,
            'reason': 'duplicate regular medication',
            'source': 'STOPP A3'
        })

    egfr = patient.get('egfr')

    if egfr is not None and egfr < 50 and 'naproxen' in medications_lower:
        findings.append({
            'medication': 'Naproxen',
            'reason': 'NSAID with eGFR below 50',
            'source': 'STOPP E4'
        })

    if egfr is not None and egfr < 30 and 'metformin' in medications_lower:
        findings.append({
            'medication': 'Metformin',
            'reason': 'Metformin with eGFR below 30',
            'source': 'STOPP E6'
        })

    if egfr is not None and egfr < 30 and 'spironolactone' in medications_lower:
        findings.append({
            'medication': 'Spironolactone',
            'reason': 'MRA with eGFR below 30',
            'source': 'STOPP E7'
        })

    return findings

def get_monitoring(patient, risks):
    monitoring = []
    risk_types = {
        item['risk_type']
        for item in risks
    }

    if 'hyperkalaemia' in risk_types:
        monitoring.append({
            'monitoring_required': 'serum potassium and renal function',
            'reason': 'hyperkalaemia risk'
        })

    if 'hyponatraemia' in risk_types:
        monitoring.append({
            'monitoring_required': 'serum sodium',
            'reason': 'hyponatraemia risk'
        })

    if 'qt_prolongation' in risk_types:
        monitoring.append({
            'monitoring_required': 'ECG / QT interval review',
            'reason': 'QT prolongation risk'
        })

    if 'hypoglycaemia' in risk_types:
        monitoring.append({
            'monitoring_required': 'blood glucose / HbA1c review',
            'reason': 'hypoglycaemia risk'
        })

    if 'renal_impairment' in risk_types:
        monitoring.append({
            'monitoring_required': 'renal function',
            'reason': 'renal impairment risk'
        })

    return monitoring

def get_recommendations(deprescribing, monitoring):
    recommendations = []

    for item in deprescribing:
        recommendations.append({
            'recommendation_type': 'medication_review',
            'medication': item['medication'],
            'reason': item['reason']
        })

    for item in monitoring:
        recommendations.append({
            'recommendation_type': 'monitoring',
            'action': item['monitoring_required'],
            'reason': item['reason']
        })

    return recommendations

ground_truth = []

for patient in patients:
    scenario = scenario_map.get(
        patient['patient_id'],
        {}
    )

    risks = get_risks(patient)
    deprescribing = get_deprescribing(patient)
    monitoring = get_monitoring(patient, risks)

    ground_truth.append({
        'patient_id': patient['patient_id'],
        'case_type': scenario.get('case_type'),
        'target': scenario.get('target'),
        'evaluation_case': scenario.get('evaluation_case'),

        'expected_indications': get_indications(patient),
        'expected_interactions': get_interactions(patient),
        'expected_risks': risks,
        'expected_deprescribing': deprescribing,
        'expected_monitoring': monitoring,
        'expected_recommendations': get_recommendations(
            deprescribing,
            monitoring
        )
    })

with OUTPUT_PATH.open('w', encoding='utf-8') as file:
    json.dump(
        ground_truth,
        file,
        indent=2,
        ensure_ascii=False
    )