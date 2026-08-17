# imports
from config import *
from clinical_logic import *
from imports import *
from schemas import *
from utils import *
from validation import *

# clinical knowledge base
clinical_knowledge = ClinicalKnowledge()

# langsmith
os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['LANGSMITH_API_KEY'] = LANGSMITH_API_KEY
os.environ['LANGSMITH_PROJECT'] = 'smr_evaluation'
os.environ['LANGSMITH_ENDPOINT'] = LANGSMITH_ENDPOINT

# model initialisation
repo_id = 'Qwen/Qwen2.5-7B-Instruct'

llm = HuggingFaceEndpoint(
    repo_id = repo_id,
    max_new_tokens = 4000,
    temperature = 0,
    huggingfacehub_api_token = HUGGINGFACEHUB_API_TOKEN,
    provider = 'auto'
)

model = ChatHuggingFace(llm = llm)

# agent initialisation
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

    # input agent
    state = input_agent.run(patient_input)
    state = validate_medications(safety_validator_agent, state, patient_input)

    # indication agent
    state = indication_agent.run(state)
    state = validate_indications(safety_validator_agent, state)

    # drug-drug interaction agent
    state = ddi_interaction_agent.run(state)
    state = validate_interactions(safety_validator_agent, state)

    # risk agent
    state = risk_agent.run(state)
    state = validate_risks(safety_validator_agent, state)

    # deprescribing agent
    state = deprescribing_agent.run(state)
    state = validate_deprescribing(safety_validator_agent, state)

    # monitoring agent
    state = monitoring_agent.run(state)
    state = validate_monitoring(safety_validator_agent, state)

    # recommendation agent
    state = recommendation_agent.run(state)
    state = validate_recommendations(safety_validator_agent, state)

    # summary agent
    summary = summary_agent.run(state)
    state = validate_summary(safety_validator_agent, state, summary)

    # clinician report
    clinician_report = generate_clinician_report(
        state,
        summary.overview,
        summary.conclusion
    )

    return state, clinician_report

# output directory
PROJECT_ROOT = Path('/data/home/bt25094/dissertation/smr pipeline')

REPORT_OUTPUT_DIRECTORY = PROJECT_ROOT / 'reports' / 'eval_reports'
REPORT_OUTPUT_DIRECTORY.mkdir(parents = True, exist_ok = True)

# evaluation dataset
EVALUATION_PATH = PROJECT_ROOT / 'data' / 'datasets' / 'evaluation'

PATIENTS_PATH = EVALUATION_PATH / 'evaluation_patients.json'
RESULTS_PATH = EVALUATION_PATH / 'evaluation_results.json'
EXECUTION_LOG_PATH = EVALUATION_PATH / 'execution_log.json'

# load patients
with PATIENTS_PATH.open('r', encoding = 'utf-8') as file:
    patients = json.load(file)

# results
results = []
execution_log = []

# evaluation run
for patient in patients:
    patient_id = patient['patient_id']

    print(f'STARTING: {patient_id}', flush = True)

    try:
        state, report = run_smr(patient)

        results.append({
            'patient_id': patient_id,
            'status': 'completed',
            'state': state.model_dump()
        })

        execution_log.append({
            'patient_id': patient_id,
            'attempt': 1,
            'status': 'completed',
            'error_type': None,
            'error': None
        })

        REPORT_PATH = REPORT_OUTPUT_DIRECTORY / f'{patient_id}.pdf'
        save_report_as_pdf(report, REPORT_PATH)

        print(f'COMPLETED: {patient_id}', flush = True)

    except Exception as error:
        results.append({
            'patient_id': patient_id,
            'status': 'failed',
            'error': str(error)
        })

        execution_log.append({
            'patient_id': patient_id,
            'attempt': 1,
            'status': 'failed',
            'error_type': type(error).__name__,
            'error': str(error)
        })

        print(
            f'FAILED: {patient_id} - {type(error).__name__}: {error}',
            flush = True
        )
    
    with RESULTS_PATH.open('w', encoding = 'utf-8') as file:
        json.dump(
            results,
            file,
            indent = 2,
            ensure_ascii = False,
            default = str
        )
    
    with EXECUTION_LOG_PATH.open('w', encoding = 'utf-8') as file:
        json.dump(
            execution_log,
            file,
            indent = 2,
            ensure_ascii = False,
            default = str
        )

completed = sum(
    1 for item in execution_log
    if item['status'] == 'completed'
)

failed = sum(
    1 for item in execution_log
    if item['status'] == 'failed'
)

print(f'EVALUATION COMPLETE: {len(results)} patients')
print(f'FIRST-PASS COMPLETED: {completed}')
print(f'FIRST-PASS FAILED: {failed}')
print(f'FIRST-PASS COMPLETION RATE: {completed / len(patients):.1%}')