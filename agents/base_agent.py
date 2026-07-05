# agents/base_agent.py
from pydantic import BaseModel, Field
from typing import Optional, List

class AgentSignals(BaseModel):
    # GST signals
    gst_vintage_months: int = 0
    average_monthly_turnover_inr: float = 0.0
    turnover_growth_trend: str = "unknown"  # "growing", "stable", "declining"
    gst_filing_punctuality_pct: float = 100.0
    concentration_risk_pct: float = 0.0

    # UPI signals
    upi_volume_90_days_inr: float = 0.0
    upi_tx_count: int = 0
    upi_velocity_trend: str = "stable"
    weekend_intensity_ratio: float = 1.0

    # EPFO signals
    has_epfo: bool = False
    current_employee_count: int = 0
    payroll_stability: str = "stable"  # "stable", "growing", "shrinking"

    # AA Banking signals
    average_daily_balance_inr: float = 0.0
    cheque_bounces_6m: int = 0
    mandate_failures_6m: int = 0
    inward_outward_ratio: float = 1.0
    critical_risk_flag: bool = False