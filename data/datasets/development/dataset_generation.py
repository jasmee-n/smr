import copy
import json
from pathlib import Path

# paths
BASE_PATH = Path('/data/home/bt25094/dissertation/smr pipeline/data/datasets/development')

PATIENTS_PATH = BASE_PATH / 'development_patients.json'
GROUND_TRUTH_PATH = BASE_PATH / 'development_ground_truth.json'

# baseline polypharmacy patient
BASE_PATIENT = {
    'patient_id': None,
    'age': 72,
    'sex': 'Female',
    'ethnicity': None,
    'weight': 70,
    'bmi': 25.5,
    'systolic_bp': 130,
    'diastolic_bp': 76,
    'hba1c': 44,
    'egfr': 72,
    'creatinine': 82,
    'total_cholesterol': 4.2,
    'ldl_cholesterol': 2.1,
    'potassium': 4.3,
    'haemoglobin': 130,
    'smoking_status': 'Never smoked',
    'alcohol_status': 'Occasional alcohol use',
    'conditions': [
        'Hypertension',
        'Hypercholesterolaemia',
        'Osteoarthritis',
        'Gastro-oesophageal reflux disease'
    ],
    'current_medications': [
        'Ramipril 5 mg OD',
        'Amlodipine 5 mg OD',
        'Atorvastatin 20 mg OD',
        'Omeprazole 20 mg OD',
        'Paracetamol 1 g PRN'
    ],
    'allergies_and_adverse_reactions': [],
    'electronic_frailty_index': 0.10,
    'falls_history': 'No falls reported',
    'clinical_notes': 'Routine structured medication review.',
    'patient_concerns': []
}

# controlled development changes
CASES = {
    'DEV001': {
        'scenario': 'baseline',
        'changes': {},
        'ground_truth': {}
    },
    'DEV002': {
        'scenario': 'single_ddi',
        'changes': {
            'conditions': [
                'Atrial fibrillation',
                'Hypertension',
                'Hypercholesterolaemia'
            ],
            'current_medications': [
                'Apixaban 5 mg BD',
                'Aspirin 75 mg OD',
                'Ramipril 5 mg OD',
                'Amlodipine 5 mg OD',
                'Atorvastatin 20 mg OD'
            ]
        },
        'ground_truth': {
            'interaction': [
                'Apixaban + Aspirin'
            ]
        }
    },
    'DEV003': {
        'scenario': 'multiple_ddi',
        'changes': {
            'conditions': [
                'Depression',
                'Chronic pain',
                'Hypertension'
            ],
            'raw_medications': [
                'Sertraline 100 mg OD',
                'Tramadol 50 mg TDS PRN',
                'Pregabalin 75 mg BD',
                'Ramipril 5 mg OD',
                'Amlodipine 5 mg OD',
                'Omeprazole 20 mg OD'
            ]
        },
        'ground_truth': {
            'interaction': [
                'Sertraline + Tramadol'
            ]
        }
    },
    'DEV004': {
        'scenario': 'stopp',
        'changes': {
            'age': 84,
            'electronic_frailty_index': 0.31,
            'falls_history': 'Two falls in the previous 6 months',
            'raw_medications': [
                'Diazepam 5 mg ON',
                'Ramipril 5 mg OD',
                'Amlodipine 5 mg OD',
                'Atorvastatin 20 mg OD',
                'Omeprazole 20 mg OD'
            ]
        },
        'ground_truth': {
            'risk': [
                'Falls risk'
            ],
            'deprescribing': [
                'Diazepam review'
            ]
        }
    },
    'DEV005': {
        'scenario': 'start',
        'changes': {
            'conditions': [
                'Coronary artery disease',
                'Hypertension',
                'Gastro-oesophageal reflux disease'
            ],
            'raw_medications': [
                'Ramipril 5 mg OD',
                'Bisoprolol 5 mg OD',
                'Aspirin 75 mg OD',
                'Amlodipine 5 mg OD',
                'Omeprazole 20 mg OD'
            ]
        },
        'ground_truth': {
            'start': [
                'Potential prescribing omission'
            ]
        }
    },
    'DEV006': {
        'scenario': 'unclear_indication',
        'changes': {
            'raw_medications': [
                'Ramipril 5 mg OD',
                'Amlodipine 5 mg OD',
                'Atorvastatin 20 mg OD',
                'Omeprazole 20 mg OD',
                'Amitriptyline 25 mg ON'
            ],
            'clinical_notes': 'No documented indication for amitriptyline.'
        },
        'ground_truth': {
            'unclear_indication': [
                'Amitriptyline'
            ]
        }
    },
    'DEV007': {
        'scenario': 'renal_impairment',
        'changes': {
            'age': 79,
            'egfr': 27,
            'creatinine': 196,
            'conditions': [
                'Chronic kidney disease',
                'Hypertension',
                'Osteoarthritis'
            ],
            'raw_medications': [
                'Ramipril 5 mg OD',
                'Ibuprofen 400 mg TDS PRN',
                'Amlodipine 5 mg OD',
                'Atorvastatin 20 mg OD',
                'Omeprazole 20 mg OD'
            ]
        },
        'ground_truth': {
            'risk': [
                'Renal medication safety risk'
            ]
        }
    },
    'DEV008': {
        'scenario': 'frailty_falls',
        'changes': {
            'age': 87,
            'systolic_bp': 108,
            'diastolic_bp': 62,
            'electronic_frailty_index': 0.42,
            'falls_history': 'Three falls in the previous year',
            'raw_medications': [
                'Ramipril 5 mg OD',
                'Amlodipine 10 mg OD',
                'Sertraline 100 mg OD',
                'Pregabalin 150 mg BD',
                'Codeine 30 mg QDS PRN',
                'Omeprazole 20 mg OD'
            ]
        },
        'ground_truth': {
            'risk': [
                'Falls risk',
                'Sedation risk'
            ]
        }
    },
    'DEV009': {
        'scenario': 'deprescribing',
        'changes': {
            'age': 78,
            'falls_history': 'One fall in the previous year',
            'raw_medications': [
                'Diazepam 2 mg ON',
                'Ramipril 5 mg OD',
                'Amlodipine 5 mg OD',
                'Atorvastatin 20 mg OD',
                'Omeprazole 20 mg OD'
            ],
            'clinical_notes': 'Diazepam has been used long term.'
        },
        'ground_truth': {
            'deprescribing': [
                'Diazepam review'
            ]
        }
    },
    'DEV010': {
        'scenario': 'complex',
        'changes': {
            'age': 82,
            'egfr_ml_min_1_73m2': 39,
            'creatinine_umol_l': 137,
            'electronic_frailty_index': 0.36,
            'falls_history': 'Two falls in the previous year',
            'conditions': [
                'Atrial fibrillation',
                'Hypertension',
                'Chronic kidney disease',
                'Depression',
                'Osteoarthritis'
            ],
            'raw_medications': [
                'Apixaban 5 mg BD',
                'Aspirin 75 mg OD',
                'Sertraline 100 mg OD',
                'Tramadol 50 mg TDS PRN',
                'Ramipril 5 mg OD',
                'Amlodipine 5 mg OD',
                'Atorvastatin 20 mg OD',
                'Omeprazole 20 mg OD'
            ]
        },
        'ground_truth': {
            'interaction': [
                'Apixaban + Aspirin',
                'Sertraline + Tramadol'
            ],
            'risk': [
                'Bleeding risk',
                'Falls risk',
                'Renal medication safety risk'
            ]
        }
    }
}


# generate development set
patients = []
ground_truth = []

for patient_id, case in CASES.items():
    patient = copy.deepcopy(
        BASE_PATIENT
    )

    patient['patient_id'] = patient_id

    patient.update(case['changes'])

    patients.append(patient)

    ground_truth.append({
        'patient_id': patient_id,
        'scenario': case['scenario'],
        **case['ground_truth']
    })

# save
with PATIENTS_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(patients, file, indent = 2, ensure_ascii = False)

with GROUND_TRUTH_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(ground_truth, file, indent = 2, ensure_ascii = False)
