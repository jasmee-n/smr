# imports
import random
from copy import deepcopy

from config import *
from libraries import *

# demographics generation
def demographic_generation():
    return {
        'age': random.randint(*AGE_RANGE),
        'sex': random.choice(SEX),
        'ethnicity': random.choice(ETHNICITY)
    }

# observations generation
def observations_generation():
    weight = round(random.uniform(*WEIGHT_RANGE), 1)
    height = random.uniform(*HEIGHT_RANGE)

    return {
        'weight': weight,
        'bmi': round(weight / (height ** 2), 1),
        'systolic_bp': random.randint(*SYSTOLIC_BP_RANGE),
        'diastolic_bp': random.randint(*DIASTOLIC_BP_RANGE),
        'heart_rate': random.randint(*HEART_RATE_RANGE),
        'hba1c': round(random.uniform(*HBA1C_RANGE), 1),
        'egfr': random.randint(*EGFR_RANGE),
        'creatinine': random.randint(*CREATININE_RANGE),
        'potassium': round(random.uniform(*POTASSIUM_RANGE), 1),
        'haemoglobin': random.randint(*HAEMOGLOBIN_RANGE)
    }

# scenario observations
def apply_scenario_observations(observations, scenario):
    target = scenario['target']

    if target == 'symptomatic_hypotension_risk':
        observations['systolic_bp'] = random.randint(85, 95)

    elif target == 'borderline_low_blood_pressure':
        observations['systolic_bp'] = random.randint(95, 105)

    elif target == 'bradycardia_risk':
        observations['heart_rate'] = random.randint(40, 50)

    elif target == 'borderline_bradycardia':
        observations['heart_rate'] = random.randint(50, 60)

    elif target == 'missing_current_renal_function':
        observations['egfr'] = None
        observations['creatinine'] = None

    return observations

# clinical notes generation
def clinical_notes_generation(scenario):
    target = scenario['target']
    notes = []

    if target == 'symptomatic_hypotension_risk':
        notes.append('Reports dizziness on standing.')

    elif target == 'recurrent_falls_medication_risk':
        notes.append('Reports recurrent falls over the previous 6 months.')

    elif target == 'missing_current_renal_function':
        notes.append('Recent renal function results are unavailable.')

    return notes

# medication generation
def medications_generation(conditions):
    medications = []

    for condition in conditions:
        options = CONDITION_MEDICATIONS.get(condition, [])

        if options:
            medications.append(random.choice(options))

    return list(dict.fromkeys(medications))

# multimorbidity generation
def conditions_generation(scenario):
    conditions = deepcopy(scenario['conditions'])
    available = [condition for condition in CONDITIONS if condition not in conditions]

    random.shuffle(available)

    target_medications = random.randint(MIN_MEDICATIONS, MAX_MEDICATIONS)

    while (
        len(medications_generation(conditions)) < target_medications
        and len(conditions) < MAX_CONDITIONS
        and available
    ):
        conditions.append(available.pop())

    return conditions

# evaluation type generation
def evaluation_type_generation(target):
    target = target.lower()

    if 'anticholinergic' in target:
        return 'anticholinergic_risk'

    elif 'bleeding' in target or 'anticoagulant' in target or 'antiplatelet' in target or 'antithrombotic' in target:
        return 'bleeding_risk'

    elif 'bradycardia' in target or 'hypotension' in target or 'blood_pressure' in target or 'heart_failure' in target or 'cardiovascular' in target:
        return 'cardiovascular_risk'

    elif 'cns' in target or 'psychotropic' in target or 'seroton' in target or 'qt' in target:
        return 'cns_risk'

    elif 'diabetes' in target or 'glycaemic' in target or 'hypoglycaemia' in target:
        return 'diabetes_risk'

    elif 'falls' in target or 'sedative' in target or 'frailty' in target:
        return 'falls_sedation_risk'

    elif 'indication' in target:
        return 'indication_risk'

    elif 'monitoring' in target:
        return 'monitoring_risk'

    elif 'renal' in target or 'kidney' in target or 'egfr' in target or 'nephro' in target or 'hyperkalaemia' in target:
        return 'renal_risk'

    elif 'respiratory' in target or 'inhaler' in target or 'bronchodilator' in target or 'reliever' in target:
        return 'respiratory_risk'

    return None

# evaluation case generation
def add_evaluation_case(medications, scenario):
    if scenario['case_type'] == 'negative':
        return medications, None

    evaluation_type = evaluation_type_generation(scenario['target'])

    if evaluation_type is None:
        return medications, None

    evaluation_case = random.choice(EVALUATION_LIBRARY[evaluation_type])

    medications.extend(evaluation_case)
    medications = list(dict.fromkeys(medications))

    return medications, evaluation_case

# patient generation
def patient_generation(scenario):
    demographics = demographic_generation()
    observations = observations_generation()
    observations = apply_scenario_observations(observations, scenario)
    clinical_notes = clinical_notes_generation(scenario)

    conditions = conditions_generation(scenario)
    medications = medications_generation(conditions)
    medications, evaluation_case = add_evaluation_case(medications, scenario)

    patient = {
    'patient_id': scenario['scenario_id'],
    'age': demographics['age'],
    'sex': demographics['sex'],
    'ethnicity': demographics['ethnicity'],
    'weight': observations['weight'],
    'bmi': observations['bmi'],
    'systolic_bp': observations['systolic_bp'],
    'diastolic_bp': observations['diastolic_bp'],
    'hba1c': observations['hba1c'],
    'egfr': observations['egfr'],
    'creatinine': observations['creatinine'],
    'total_cholesterol': round(random.uniform(3.0, 7.0), 1),
    'ldl_cholesterol': round(random.uniform(1.0, 5.0), 1),
    'potassium': observations['potassium'],
    'haemoglobin': observations['haemoglobin'],
    'smoking_status': random.choice(SMOKING_STATUS),
    'alcohol_status': random.choice(ALCOHOL_STATUS),
    'raw_medications': medications,
    'conditions': conditions,
    'allergies': random.choice(ALLERGIES),
    'frailty_score': round(random.uniform(0.05, 0.45), 2),
    'falls_history': 'No falls reported',
    'clinical_notes': ' '.join(clinical_notes) if clinical_notes else 'Routine structured medication review.',
    'patient_concerns': []
    }
    
    return patient, evaluation_case