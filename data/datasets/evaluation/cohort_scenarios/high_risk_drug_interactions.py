HIGH_RISK_DRUG_INTERACTION_SCENARIOS = [
    
    {
        "scenario_id": "DDI_EVAL001",
        "case_type": "positive",
        "target": "anticoagulant_antiplatelet_interaction",
        "conditions": [
            "Atrial fibrillation"
        ],
        "description": (
            "Patient receiving anticoagulant and antiplatelet therapy creating a clinically relevant drug interaction and increased bleeding risk."
        )
    },

    {
        "scenario_id": "DDI_EVAL002",
        "case_type": "positive",
        "target": "anticoagulant_nsaid_interaction",
        "conditions": [
            "Atrial fibrillation",
            "Osteoarthritis"
        ],
        "description": (
            "Patient receiving an anticoagulant and NSAID combination creating a clinically relevant interaction and increased bleeding risk."
        )
    },

    {
        "scenario_id": "DDI_EVAL003",
        "case_type": "positive",
        "target": "serotonergic_interaction",
        "conditions": [
            "Depression",
            "Chronic pain"
        ],
        "description": (
            "Patient receiving multiple serotonergic medications creating a clinically relevant interaction."
        )
    },

    {
        "scenario_id": "DDI_EVAL004",
        "case_type": "positive",
        "target": "qt_prolongation_interaction",
        "conditions": [
            "Depression",
            "Cardiac arrhythmia"
        ],
        "description": (
            "Patient receiving medications with additive effects on QT prolongation creating a clinically relevant interaction."
        )
    },

    {
        "scenario_id": "DDI_EVAL005",
        "case_type": "positive",
        "target": "bradycardia_interaction",
        "conditions": [
            "Atrial fibrillation"
        ],
        "description": (
            "Patient receiving multiple rate-limiting medications creating a clinically relevant risk of bradycardia."
        )
    },

    {
        "scenario_id": "DDI_EVAL006",
        "case_type": "positive",
        "target": "hyperkalaemia_interaction",
        "conditions": [
            "Heart failure",
            "Hypertension"
        ],
        "description": (
            "Patient receiving a medication combination creating a clinically relevant increased risk of hyperkalaemia."
        )
    },

    {
        "scenario_id": "DDI_EVAL007",
        "case_type": "positive",
        "target": "cns_depression_interaction",
        "conditions": [
            "Chronic pain",
            "Anxiety"
        ],
        "description": (
            "Patient receiving multiple CNS-depressant medications creating clinically relevant additive sedation."
        )
    },

    {
        "scenario_id": "DDI_EVAL008",
        "case_type": "positive",
        "target": "pharmacokinetic_interaction",
        "conditions": [
            "Atrial fibrillation",
            "Hypertension"
        ],
        "description": (
            "Patient receiving medications with a clinically relevant pharmacokinetic interaction affecting drug exposure or treatment safety."
        )
    },

    {
        "scenario_id": "DDI_EVAL009",
        "case_type": "negative",
        "target": "cardiovascular_no_interaction",
        "conditions": [
            "Hypertension"
        ],
        "description": (
            "Patient receiving multiple cardiovascular medications without a predefined clinically relevant drug-drug interaction."
        )
    },

    {
        "scenario_id": "DDI_EVAL010",
        "case_type": "negative",
        "target": "diabetes_no_interaction",
        "conditions": [
            "Type 2 diabetes",
            "Hypertension"
        ],
        "description": (
            "Patient receiving a multidrug diabetes and hypertension regimen without a predefined clinically relevant drug-drug interaction."
        )
    },

    {
        "scenario_id": "DDI_EVAL011",
        "case_type": "negative",
        "target": "analgesia_no_interaction",
        "conditions": [
            "Osteoarthritis",
            "Hypertension"
        ],
        "description": (
            "Patient receiving analgesic and cardiovascular medications without a predefined clinically relevant drug-drug interaction."
        )
    },

    {
        "scenario_id": "DDI_EVAL012",
        "case_type": "negative",
        "target": "polypharmacy_no_interaction",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Osteoarthritis"
        ],
        "description": (
            "Patient with a higher medication count without a predefined clinically relevant drug-drug interaction."
        )
    },

    {
        "scenario_id": "DDI_EVAL013",
        "case_type": "boundary",
        "target": "interaction_with_valid_clinical_indication",
        "conditions": [
            "Atrial fibrillation",
            "Recent acute coronary syndrome"
        ],
        "description": (
            "Patient receiving interacting medications for a documented clinical indication where the risk should be recognised without assuming treatment is inappropriate."
        )
    },

    {
        "scenario_id": "DDI_EVAL014",
        "case_type": "boundary",
        "target": "interaction_severity_context_dependent",
        "conditions": [
            "Hypertension",
            "Chronic pain"
        ],
        "description": (
            "Patient with a potential interaction where clinical significance depends on factors such as dose, monitoring or individual patient characteristics."
        )
    },

    {
        "scenario_id": "DDI_EVAL015",
        "case_type": "boundary",
        "target": "interaction_requires_missing_information",
        "conditions": [
            "Atrial fibrillation",
            "Hypertension"
        ],
        "description": (
            "Patient with a potential drug interaction that cannot be fully interpreted because clinically important information is unavailable."
        )
    }
]