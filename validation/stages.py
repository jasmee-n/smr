def validate_medications(validator, state, patient_input):
    return validator.run(
        state = state,
        stage = 'medications',
        stage_output = {
            'patient': state.patient,
            'medications': state.medications
        },
        evidence = patient_input
    )

def validate_indications(validator, state):
    return validator.run(
        state = state,
        stage = 'indications',
        stage_output = state.indications,
        evidence = {
            'patient': state.patient,
            'medications': state.medications,
            'bnf_tables': state.clinical_evidence.bnf_tables
        }
    )

def validate_interactions(validator, state):
    return validator.run(
        state = state,
        stage = 'interactions',
        stage_output = state.interactions,
        evidence = {
            'medications': state.medications,
            'bnf_interactions': state.clinical_evidence.bnf_interactions
        }
    )

def validate_risks(validator, state):
    return validator.run(
        state = state,
        stage = 'risks',
        stage_output = state.risks,
        evidence = {
            'patient': state.patient,
            'medications': state.medications,
            'interactions': state.interactions,
            'stopp_evidence': state.clinical_evidence.stopp,
            'bnf_tables': state.clinical_evidence.bnf_tables
        }
    )

def validate_deprescribing(validator, state):
    return validator.run(
        state = state,
        stage = 'deprescribing',
        stage_output = state.deprescribing,
        evidence = {
            'patient': state.patient,
            'indications': state.indications,
            'medications': state.medications,
            'interactions': state.interactions,
            'risks': state.risks,
            'stopp_evidence': state.clinical_evidence.stopp,
            'bnf_tables': state.clinical_evidence.bnf_tables
        }
    )

def validate_monitoring(validator, state):
    return validator.run(
        state = state,
        stage = 'monitoring',
        stage_output = state.monitoring,
        evidence = {
            'patient': state.patient,
            'medications': state.medications,
            'interactions': state.interactions,
            'risks': state.risks,
            'bnf_tables': state.clinical_evidence.bnf_tables,
            'bnf_interactions': state.clinical_evidence.bnf_interactions
        }
    )

def validate_recommendations(validator, state):
    return validator.run(
        state = state,
        stage = 'recommendations',
        stage_output = state.recommendations,
        evidence = {
            'patient': state.patient,
            'indications': state.indications,
            'medications': state.medications,
            'interactions': state.interactions,
            'risks': state.risks,
            'deprescribing': state.deprescribing,
            'monitoring': state.monitoring,
            'start': state.clinical_evidence.start,
            'stopp': state.clinical_evidence.stopp,
            'bnf_tables': state.clinical_evidence.bnf_tables,
            'bnf_interactions': state.clinical_evidence.bnf_interactions
        }
    )

def validate_summary(validator, state, summary):
    return validator.run(
        state = state,
        stage = 'summary',
        stage_output = {
            'overview': summary.overview,
            'conclusion': summary.conclusion
        },
        evidence = {
            'indications': state.indications,
            'interactions': state.interactions,
            'risks': state.risks,
            'deprescribing': state.deprescribing,
            'monitoring': state.monitoring,
            'recommendations': state.recommendations
        }
    )