# imports
import json
import random
from pathlib import Path

from cohort_scenarios import *
from config import RANDOM_SEED

from patient_generation import patient_generation, evaluation_type_generation
from ground_truth_generation import ground_truth_generation

# variables
random.seed(RANDOM_SEED)

OUTPUT_DIRECTORY = Path(__file__).parent

PATIENT_PATH = OUTPUT_DIRECTORY / 'evaluation_patients.json'
GROUND_TRUTH_PATH = OUTPUT_DIRECTORY / 'evaluation_reference.json'

# scenarios
ALL_SCENARIOS = (
    CARDIOVASCULAR_SCENARIOS
    + DIABETES_AND_CKD_SCENARIOS
    + HIGH_RISK_DRUG_INTERACTION_SCENARIOS
    + FRAILTY_SCENARIOS
    + MENTAL_HEALTH_SCENARIOS
    + MULTI_MORBIDITY_SCENARIOS
    + RESPIRATORY_SCENARIOS
)

# validation
assert len(ALL_SCENARIOS) == 100, f'Expected 100 scenarios, found {len(ALL_SCENARIOS)}.'

scenario_ids = [scenario['scenario_id'] for scenario in ALL_SCENARIOS]
assert len(scenario_ids) == len(set(scenario_ids)), 'Duplicate scenario IDs found.'

# generation
patients = []
ground_truth = []

for scenario in ALL_SCENARIOS:
    patient, evaluation_case = patient_generation(scenario)

    patients.append(patient)
    ground_truth.append(ground_truth_generation(scenario, patient, evaluation_case))

# output
with PATIENT_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(patients, file, indent = 2, ensure_ascii = False)

with GROUND_TRUTH_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(ground_truth, file, indent = 2, ensure_ascii = False)