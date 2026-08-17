DIABETES_AND_CKD_SCENARIOS = [
    
    {
        "scenario_id": "DCKD_EVAL001",
        "case_type": "positive",
        "target": "medication_inappropriate_for_renal_function",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient receiving a medication whose use is inappropriate given significantly reduced renal function."
        )
    },

    {
        "scenario_id": "DCKD_EVAL002",
        "case_type": "positive",
        "target": "renal_dose_adjustment_required",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient receiving a medication requiring dose adjustment because of reduced renal function."
        )
    },

    {
        "scenario_id": "DCKD_EVAL003",
        "case_type": "positive",
        "target": "missing_renal_function_monitoring",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient receiving treatment requiring renal-function monitoring where relevant monitoring information is absent or overdue."
        )
    },

    {
        "scenario_id": "DCKD_EVAL004",
        "case_type": "positive",
        "target": "hypoglycaemia_risk_in_ckd",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient receiving diabetes treatment where renal impairment contributes to an increased risk of hypoglycaemia."
        )
    },

    {
        "scenario_id": "DCKD_EVAL005",
        "case_type": "positive",
        "target": "nephrotoxic_medication_risk",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease",
            "Osteoarthritis"
        ],
        "description": (
            "Patient with chronic kidney disease receiving a medication that may further compromise renal function."
        )
    },

    {
        "scenario_id": "DCKD_EVAL006",
        "case_type": "positive",
        "target": "acute_kidney_injury_risk_combination",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease",
            "Hypertension"
        ],
        "description": (
            "Patient receiving a combination of medications associated with an increased risk of acute kidney injury."
        )
    },

    {
        "scenario_id": "DCKD_EVAL007",
        "case_type": "positive",
        "target": "diabetes_treatment_requires_review",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient receiving diabetes treatment that requires review because of reduced renal function and current clinical context."
        )
    },

    {
        "scenario_id": "DCKD_EVAL008",
        "case_type": "negative",
        "target": "appropriate_diabetes_ckd_regimen",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient receiving diabetes treatment that is appropriate for the current level of renal function."
        )
    },

    {
        "scenario_id": "DCKD_EVAL009",
        "case_type": "negative",
        "target": "appropriate_renal_adjustment",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient receiving a renally affected medication that has already been appropriately adjusted for kidney function."
        )
    },

    {
        "scenario_id": "DCKD_EVAL010",
        "case_type": "negative",
        "target": "stable_ckd_with_monitoring",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease",
            "Hypertension"
        ],
        "description": (
            "Patient with stable chronic kidney disease receiving appropriate treatment with relevant renal and metabolic monitoring."
        )
    },

    {
        "scenario_id": "DCKD_EVAL011",
        "case_type": "boundary",
        "target": "egfr_near_dosing_threshold",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient with renal function close to a medication-specific dosing threshold requiring careful interpretation."
        )
    },

    {
        "scenario_id": "DCKD_EVAL012",
        "case_type": "boundary",
        "target": "renal_function_near_contraindication_threshold",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient with renal function close to a threshold at which medication appropriateness would change."
        )
    },

    {
        "scenario_id": "DCKD_EVAL013",
        "case_type": "boundary",
        "target": "missing_current_renal_function",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient where current renal function is required to determine medication safety but sufficiently recent information is unavailable."
        )
    },

    {
        "scenario_id": "DCKD_EVAL014",
        "case_type": "boundary",
        "target": "borderline_glycaemic_overtreatment",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease"
        ],
        "description": (
            "Patient where diabetes treatment intensity may represent overtreatment but the clinical context does not make treatment reduction clearly necessary."
        )
    },

    {
        "scenario_id": "DCKD_EVAL015",
        "case_type": "complex",
        "target": "multiple_renal_medication_problems",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease",
            "Hypertension",
            "Heart failure"
        ],
        "description": (
            "Complex patient containing multiple renal-function-dependent medication, interaction and monitoring problems."
        )
    }
]