# ground truth generation
def ground_truth_generation(scenario, patient, evaluation_case):

    return {
        'patient_id': patient['patient_id'],
        'case_type': scenario['case_type'],
        'target': scenario['target'],
        'evaluation_type': scenario.get('evaluation_type'),
        'evaluation_case': evaluation_case
    }