# agents/aa_agent.py
from agents.base_agent import AgentSignals

class AAAgent:
    def process(self, raw_aa_data: dict, signals: AgentSignals) -> AgentSignals:
        if not raw_aa_data:
            return signals

        summary = raw_aa_data.get("account_summary", {})
        triggers = raw_aa_data.get("risk_triggers_past_180_days", {})

        signals.average_daily_balance_inr = summary.get("average_daily_balance_3m_inr", 0.0)
        signals.cheque_bounces_6m = triggers.get("cheque_bounces", 0)
        signals.mandate_failures_6m = triggers.get("ecs_mandate_failures", 0)
        signals.inward_outward_ratio = triggers.get("inward_outward_ratio", 1.0)

        # Trigger a hard risk flag if clear structural failure signals emerge
        if signals.cheque_bounces_6m > 2 or signals.mandate_failures_6m > 2 or signals.inward_outward_ratio < 0.90:
            signals.critical_risk_flag = True

        return signals