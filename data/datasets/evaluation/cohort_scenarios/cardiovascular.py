CARDIOVASCULAR_SCENARIOS = [
    
    {
        "scenario_id": "CVD_EVAL001",
        "case_type": "positive",
        "target": "anticoagulant_antiplatelet_bleeding_risk",
        "conditions": [
            "Atrial fibrillation",
            "Hypertension"
        ],
        "description": (
            "Patient receiving an anticoagulant and antiplatelet without a clear concurrent indication, creating increased bleeding risk."
        )
    },

    {
        "scenario_id": "CVD_EVAL002",
        "case_type": "positive",
        "target": "nsaid_in_heart_failure",
        "conditions": [
            "Heart failure",
            "Osteoarthritis"
        ],
        "description": (
            "Patient with heart failure receiving an NSAID that may worsen fluid retention and heart failure control."
        )
    },

    {
        "scenario_id": "CVD_EVAL003",
        "case_type": "positive",
        "target": "duplicate_antithrombotic_therapy",
        "conditions": [
            "Atrial fibrillation"
        ],
        "description": (
            "Patient receiving unnecessary overlapping antithrombotic therapy."
        )
    },

    {
        "scenario_id": "CVD_EVAL004",
        "case_type": "positive",
        "target": "bradycardia_risk",
        "conditions": [
            "Atrial fibrillation",
            "Hypertension"
        ],
        "description": (
            "Combination of rate-limiting cardiovascular medicines creating a clinically relevant bradycardia risk."
        )
    },

    {
        "scenario_id": "CVD_EVAL005",
        "case_type": "positive",
        "target": "symptomatic_hypotension_risk",
        "conditions": [
            "Hypertension",
            "Heart failure"
        ],
        "description": (
            "Multiple blood-pressure-lowering medicines in a patient with low blood pressure and symptoms compatible with hypotension."
        )
    },

    {
        "scenario_id": "CVD_EVAL006",
        "case_type": "positive",
        "target": "missing_renal_electrolyte_monitoring",
        "conditions": [
            "Heart failure",
            "Hypertension"
        ],
        "description": (
            "Cardiovascular regimen requiring renal function and electrolyte monitoring where relevant monitoring information is absent or overdue."
        )
    },

    {
        "scenario_id": "CVD_EVAL007",
        "case_type": "positive",
        "target": "inappropriate_long_term_antiplatelet",
        "conditions": [
            "Ischaemic heart disease",
            "Atrial fibrillation"
        ],
        "description": (
            "Long-term antiplatelet therapy remains on the medication list despite no clear continuing indication alongside anticoagulation."
        )
    },
    
    {
        "scenario_id": "CVD_EVAL008",
        "case_type": "negative",
        "target": "appropriate_af_anticoagulation",
        "conditions": [
            "Atrial fibrillation",
            "Hypertension"
        ],
        "description": (
            "Stable atrial fibrillation patient receiving an appropriate anticoagulation and rate-control regimen without a predefined medication-related problem."
        )
    },

    {
        "scenario_id": "CVD_EVAL009",
        "case_type": "negative",
        "target": "appropriate_hypertension_management",
        "conditions": [
            "Hypertension"
        ],
        "description": (
            "Hypertension controlled on an appropriate regimen with no deliberately embedded medication-related problem."
        )
    },

    {
        "scenario_id": "CVD_EVAL010",
        "case_type": "negative",
        "target": "appropriate_heart_failure_regimen",
        "conditions": [
            "Heart failure"
        ],
        "description": (
            "Stable heart failure patient receiving an appropriate treatment regimen with suitable monitoring and no predefined medication safety problem."
        )
    },

    {
        "scenario_id": "CVD_EVAL011",
        "case_type": "negative",
        "target": "appropriate_secondary_prevention",
        "conditions": [
            "Ischaemic heart disease",
            "Hypertension"
        ],
        "description": (
            "Patient receiving appropriate cardiovascular secondary prevention without a predefined medication-related problem."
        )
    },
    
    {
        "scenario_id": "CVD_EVAL012",
        "case_type": "boundary",
        "target": "anticoagulant_antiplatelet_valid_indication",
        "conditions": [
            "Atrial fibrillation",
            "Recent acute coronary syndrome"
        ],
        "description": (
            "Patient receiving anticoagulant and antiplatelet therapy where the combination increases bleeding risk but has a documented clinical indication, requiring contextual interpretation rather than automatic discontinuation."
        )
    },

    {
        "scenario_id": "CVD_EVAL013",
        "case_type": "boundary",
        "target": "borderline_low_blood_pressure",
        "conditions": [
            "Hypertension",
            "Heart failure"
        ],
        "description": (
            "Patient receiving several cardiovascular medicines with blood pressure near the lower end of the acceptable range but without clear symptoms of hypotension."
        )
    },

    {
        "scenario_id": "CVD_EVAL014",
        "case_type": "boundary",
        "target": "borderline_bradycardia",
        "conditions": [
            "Atrial fibrillation"
        ],
        "description": (
            "Patient receiving rate-control therapy with a heart rate close to a clinically concerning threshold but without clear symptoms, requiring cautious interpretation."
        )
    },

    {
        "scenario_id": "CVD_EVAL015",
        "case_type": "complex",
        "target": "multiple_cardiovascular_medication_problems",
        "conditions": [
            "Atrial fibrillation",
            "Heart failure",
            "Hypertension",
            "Ischaemic heart disease"
        ],
        "description": (
            "Complex cardiovascular polypharmacy case containing multiple simultaneous medication-related issues across interaction, risk, monitoring and deprescribing domains."
        )
    }
]