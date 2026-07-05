# agents/upi_agent.py
from agents.base_agent import AgentSignals

class UPIAgent:
    def process(self, raw_upi_data: dict, signals: AgentSignals) -> AgentSignals:
        if not raw_upi_data:
            return signals

        summary = raw_upi_data.get("summary_past_90_days", {})
        signals.upi_volume_90_days_inr = summary.get("total_volume_inr", 0.0)
        signals.upi_tx_count = summary.get("total_transaction_count", 0)
        signals.upi_velocity_trend = summary.get("monthly_velocity_trend", "stable")
        signals.weekend_intensity_ratio = summary.get("weekend_vs_weekday_ratio", 1.0)
        
        return signals