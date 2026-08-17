# imports
import os
import json
import pandas as pd

from langchain.chat_models import init_chat_model
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langsmith import traceable

from pathlib import Path
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional
from dataclasses import dataclass, field

from clinical_logic import ClinicalKnowledge

from agents import (
    InputAgent,
    IndicationAgent,
    DDIInteractionAgent,
    RiskAgent,
    DeprescribingAgent,
    MonitoringAgent,
    RecommendationAgent,
    SafetyValidatorAgent,
    SummaryAgent,
    generate_clinician_report
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer