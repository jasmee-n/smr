# imports
from config import *
from clinical_logic import *
from imports import *
from schemas import *
from utils import *
from validation import *

import traceback

# clinical knowledge
clinical_knowledge = ClinicalKnowledge()

# langsmith
os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['LANGSMITH_API_KEY'] = LANGSMITH_API_KEY
os.environ['LANGSMITH_PROJECT'] = 'smr_development'
os.environ['LANGSMITH_ENDPOINT'] = LANGSMITH_ENDPOINT

repo_id = 'Qwen/Qwen2.5-7B-Instruct'

llm = HuggingFaceEndpoint(
    repo_id = repo_id,
    max_new_tokens = 4000,
    temperature = 0,
    huggingfacehub_api_token = HUGGINGFACEHUB_API_TOKEN,
    provider = 'auto'
)

model = ChatHuggingFace(llm = llm)

# agents
input_agent = InputAgent(model = model)

indication_agent = IndicationAgent(model = model, clinical_knowledge = clinical_knowledge)

ddi_interaction_agent = DDIInteractionAgent(model = model, clinical_knowledge = clinical_knowledge)

risk_agent = RiskAgent(model = model, clinical_knowledge = clinical_knowledge)

deprescribing_agent = DeprescribingAgent(model = model, clinical_knowledge = clinical_knowledge)

monitoring_agent = MonitoringAgent(model = model, clinical_knowledge = clinical_knowledge)

recommendation_agent = RecommendationAgent(model = model, clinical_knowledge = clinical_knowledge)

summary_agent = SummaryAgent(model = model)

safety_validator_agent = SafetyValidatorAgent(model = model)

@traceable(name = 'SMR Pipeline', run_type = 'chain')
def run_smr(patient_input):
    state = input_agent.run(patient_input)
    state = validate_medications(safety_validator_agent, state, patient_input)

    state = indication_agent.run(state)
    state = validate_indications(safety_validator_agent, state)

    state = ddi_interaction_agent.run(state)
    state = validate_interactions(safety_validator_agent, state)

    state = risk_agent.run(state)
    state = validate_risks(safety_validator_agent, state)

    state = deprescribing_agent.run(state)
    state = validate_deprescribing(safety_validator_agent, state)

    state = monitoring_agent.run(state)
    state = validate_monitoring(safety_validator_agent, state)

    state = recommendation_agent.run(state)
    state = validate_recommendations(safety_validator_agent, state)

    state.ranked_findings = rank_findings(state)

    state = summary_agent.run(state)
    state = validate_summary(safety_validator_agent, state, state)

    report = generate_clinician_report(state, state.overview, state.conclusion)

    return state, report

# paths
PROJECT_ROOT = YOUR_PATH

REPORT_OUTPUT_DIRECTORY = PROJECT_ROOT / 'reports' / 'development_reports'
REPORT_OUTPUT_DIRECTORY.mkdir(parents = True, exist_ok = True)

DEVELOPMENT_PATH = PROJECT_ROOT / 'data' / 'datasets' / 'development'

PATIENTS_PATH = DEVELOPMENT_PATH / 'development_patients.json'
RESULTS_PATH = DEVELOPMENT_PATH / 'development_results.json'

with PATIENTS_PATH.open('r', encoding = 'utf-8') as file:
    patients = json.load(file)

results = []

for patient in patients:
    patient_id = patient['patient_id']

    print(f'STARTING: {patient_id}', flush=True)

    try:
        state, report = run_smr(patient)

        results.append({
            'patient_id': patient_id,
            'status': 'completed',
            'state': state.model_dump()
        })

        report_path = REPORT_OUTPUT_DIRECTORY / f'{patient_id}.pdf'
        save_report_as_pdf(report, report_path)

        print(f'COMPLETED: {patient_id}', flush=True)

    except Exception as error:
        print(
            f'FAILED: {patient_id} - {type(error).__name__}: {error}',
            flush=True
        )

        traceback.print_exc()

        results.append({
            'patient_id': patient_id,
            'status': 'failed',
            'error': str(error)
        })

    with RESULTS_PATH.open('w', encoding = 'utf-8') as file:
        json.dump(
            results,
            file,
            indent = 2,
            ensure_ascii = False,
            default = str
        )

completed = sum(item['status'] == 'completed' for item in results)
failed = sum(item['status'] == 'failed'for item in results)

print(f'DEVELOPMENT COMPLETE: {len(results)} patients')
print(f'COMPLETED: {completed}')
print(f'FAILED: {failed}')