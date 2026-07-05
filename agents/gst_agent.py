# agents/gst_agent.py
from agents.base_agent import AgentSignals

class GSTAgent:
    def process(self, raw_gst_data: dict, signals: AgentSignals) -> AgentSignals:
        if not raw_gst_data:
            signals.turnover_growth_trend = "no_data"
            return signals

        history = raw_gst_data.get("gstr_3b_history", [])
        signals.gst_vintage_months = raw_gst_data.get("vintage_months", 0)
        signals.concentration_risk_pct = raw_gst_data.get("concentration_risk_pct", 0.0)

        if not history:
            return signals

        # Calculate average turnover
        turnovers = [m["turnover_inr"] for m in history]
        signals.average_monthly_turnover_inr = sum(turnovers) / len(turnovers)

        # Calculate filing punctuality
        on_time_count = sum(1 for m in history if m["filed_on_time"])
        signals.gst_filing_punctuality_pct = (on_time_count / len(history)) * 100

        # Calculate MoM trend vector (comparing first half vs second half of history)
        if len(turnovers) >= 4:
            half = len(turnovers) // 2
            recent_avg = sum(turnovers[:half]) / half
            older_avg = sum(turnovers[half:]) / half
            
            if recent_avg < older_avg * 0.90:
                signals.turnover_growth_trend = "declining"
            elif recent_avg > older_avg * 1.10:
                signals.turnover_growth_trend = "growing"
            else:
                signals.turnover_growth_trend = "stable"

        return signals