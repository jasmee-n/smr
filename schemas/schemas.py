# schemas
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class PatientRecord(BaseModel):
    patient_id: str
    age: int
    sex: str
    ethnicity: Optional[str] = None

    weight: Optional[float] = None 
    bmi: Optional[float] = None

    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None

    hba1c: Optional[float] = None
    egfr: Optional[float] = None
    creatinine: Optional[float] = None
    total_cholesterol: Optional[float] = None
    ldl_cholesterol: Optional[float] = None
    potassium: Optional[float] = None
    haemoglobin: Optional[float] = None

    smoking_status: Optional[str] = None
    alcohol_status: Optional[str] = None

    raw_medications: List[str] = Field(default_factory = list)
    conditions: List[str] = Field(default_factory = list)
    allergies: List[str] = Field(default_factory = list)

    frailty_score: Optional[float] = None
    falls_history: Optional[str] = None
    clinical_notes: Optional[str] = None
    patient_concerns: List[str] = Field(default_factory = list)


class Medication(BaseModel):
    name: str
    dose: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    start_date: Optional[str] = None


class MedicationsList(BaseModel):
    medications: List[Medication] = Field(default_factory = list)


class ClinicalEvidence(BaseModel):
    bnf_interactions: List[dict] = Field(default_factory = list)
    bnf_tables: List[dict] = Field(default_factory = list)
    stopp: List[dict] = Field(default_factory = list)
    start: List[dict] = Field(default_factory = list)


class Indication(BaseModel):
    medication_name: str
    indication: str
    rationale: str
    source: Optional[str] = None


class IndicationsList(BaseModel):
    indications: List[Indication] = Field(default_factory = list)


class Interaction(BaseModel):
    drug_a: str
    drug_b: str
    severity: str
    rationale: str
    source: Optional[str] = None


class InteractionsList(BaseModel):
    interactions: List[Interaction] = Field(default_factory = list)


class Risk(BaseModel):
    risk_type: str
    severity: str
    rationale: str
    source: Optional[str] = None


class RisksList(BaseModel):
    risks: List[Risk] = Field(default_factory = list)


class Deprescribing(BaseModel):
    medication: str
    issue: str
    rationale: str
    suggested_action: str
    priority: str
    source: Optional[str] = None


class DeprescribingList(BaseModel):
    deprescribing: List[Deprescribing] = Field(default_factory = list)


class Monitoring(BaseModel):
    medication_or_condition: str
    monitoring_required: str
    rationale: str
    timeframe: Optional[str] = None
    priority: Optional[str] = None
    source: Optional[str] = None


class MonitoringList(BaseModel):
    monitoring: List[Monitoring] = Field(default_factory = list) 


class Recommendation(BaseModel):
    recommendation: str
    rationale: str
    priority: str
    source: Optional[str] = None


class RecommendationsList(BaseModel):
    recommendations: List[Recommendation] = Field(default_factory = list)


class PrioritisedFinding(BaseModel):
    finding_type: str
    priority_score: int
    priority_level: str
    description: str
    source: Optional[str] = None


class ReportSummary(BaseModel):
    overview: str
    conclusion: str


class ValidationIssue(BaseModel):
    claim: str
    issue_type: Literal[
        'unsupported_claim',
        'patient_mismatch',
        'missing_information',
        'unsafe_recommendation',
        'severity_mismatch',
        'contradiction',
        'uncertainty_not_acknowledged',
        'other'
        ]
    description: str
    affected_item: Optional[str] = None 
    severity: Literal[
        'low',
        'moderate',
        'high',
        'critical'
        ] 
    suggested_action: Optional[str] = None


class ValidationResult(BaseModel):
    stage: str
    status: Literal[
        'passed',
        'passed_with_warnings',
        'failed'
        ]
    is_grounded: bool = True
    is_patient_consistent: bool = True
    is_clinically_safe: bool = True
    has_sufficient_information: bool = True
    issues: list[ValidationIssue] = Field(default_factory = list)
    summary: str


class SMRState(BaseModel):
    patient: PatientRecord
    
    medications: MedicationsList = Field(default_factory = MedicationsList)
    medications_validation: Optional[ValidationResult] = None
    
    clinical_evidence: ClinicalEvidence = Field(default_factory = ClinicalEvidence)
    
    indications: IndicationsList = Field(default_factory = IndicationsList)
    indications_validation: Optional[ValidationResult] = None
    
    interactions: InteractionsList = Field(default_factory = InteractionsList)
    interactions_validation: Optional[ValidationResult] = None
    
    risks: RisksList = Field(default_factory = RisksList)
    risks_validation: Optional[ValidationResult] = None
    
    deprescribing: DeprescribingList = Field(default_factory = DeprescribingList)
    deprescribing_validation: Optional[ValidationResult] = None
    
    monitoring: MonitoringList = Field(default_factory = MonitoringList)
    monitoring_validation: Optional[ValidationResult] = None
    
    recommendations: RecommendationsList = Field(default_factory = RecommendationsList)
    recommendation_validation: Optional[ValidationResult] = None
    
    ranked_findings: List[PrioritisedFinding] = Field(default_factory = list)
    
    final_validation: Optional[ValidationResult] = None
    overview: Optional[str] = None
    conclusion: Optional[str] = None