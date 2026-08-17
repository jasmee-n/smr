RESPIRATORY_SCENARIOS = [
    
    {
        "scenario_id": "RES_EVAL001",
        "case_type": "positive",
        "target": "duplicate_bronchodilator_therapy",
        "conditions": [
            "Chronic obstructive pulmonary disease"
        ],
        "description": (
            "Patient receiving unintended duplicate bronchodilator therapy requiring medication review."
        )
    },

    {
        "scenario_id": "RES_EVAL002",
        "case_type": "positive",
        "target": "inappropriate_inhaler_regimen",
        "conditions": [
            "Chronic obstructive pulmonary disease"
        ],
        "description": (
            "Patient receiving an inhaler regimen containing a clear medication-appropriateness problem."
        )
    },

    {
        "scenario_id": "RES_EVAL003",
        "case_type": "positive",
        "target": "excessive_reliever_use",
        "conditions": [
            "Asthma"
        ],
        "description": (
            "Patient with asthma showing excessive reliance on reliever medication requiring clinical review."
        )
    },

    {
        "scenario_id": "RES_EVAL004",
        "case_type": "positive",
        "target": "respiratory_medication_disease_interaction",
        "conditions": [
            "Asthma",
            "Hypertension"
        ],
        "description": (
            "Patient receiving treatment for a comorbid condition that may adversely affect the underlying respiratory disease."
        )
    },

    {
        "scenario_id": "RES_EVAL005",
        "case_type": "negative",
        "target": "appropriate_copd_regimen",
        "conditions": [
            "Chronic obstructive pulmonary disease"
        ],
        "description": (
            "Stable patient with chronic obstructive pulmonary disease receiving an appropriate inhaled treatment regimen without a predefined medication-related problem."
        )
    },

    {
        "scenario_id": "RES_EVAL006",
        "case_type": "negative",
        "target": "appropriate_asthma_regimen",
        "conditions": [
            "Asthma"
        ],
        "description": (
            "Patient with asthma receiving an appropriate medication regimen without a deliberately embedded medication-related problem."
        )
    },

    {
        "scenario_id": "RES_EVAL007",
        "case_type": "negative",
        "target": "appropriate_respiratory_polypharmacy",
        "conditions": [
            "Chronic obstructive pulmonary disease",
            "Hypertension"
        ],
        "description": (
            "Patient receiving respiratory and cardiovascular medications without a predefined interaction or medication-appropriateness problem."
        )
    },

    {
        "scenario_id": "RES_EVAL008",
        "case_type": "negative",
        "target": "stable_respiratory_treatment",
        "conditions": [
            "Asthma",
            "Allergic rhinitis"
        ],
        "description": (
            "Patient with stable respiratory disease receiving an appropriate medication regimen without a predefined medication-safety problem."
        )
    },

    {
        "scenario_id": "RES_EVAL009",
        "case_type": "boundary",
        "target": "possible_inhaler_step_down",
        "conditions": [
            "Asthma"
        ],
        "description": (
            "Patient with well-controlled asthma where treatment step-down may be considered but continued treatment remains clinically plausible."
        )
    },

    {
        "scenario_id": "RES_EVAL010",
        "case_type": "complex",
        "target": "complex_respiratory_polypharmacy",
        "conditions": [
            "Chronic obstructive pulmonary disease",
            "Heart failure",
            "Hypertension",
            "Osteoarthritis"
        ],
        "description": (
            "Complex respiratory and cardiovascular multimorbidity case containing multiple medication interaction, appropriateness and monitoring problems."
        )
    }
]