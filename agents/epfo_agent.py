# agents/epfo_agent.py
from agents.base_agent import AgentSignals

class EPFOAgent:
    def process(self, raw_epfo_data: dict, signals: AgentSignals) -> AgentSignals:
        if not raw_epfo_data or "payroll_history" not in raw_epfo_data:
            signals.has_epfo = False
            signals.payroll_stability = "informal"
            return signals

        history = raw_epfo_data.get("payroll_history", [])
        if not history:
            signals.has_epfo = False
            return signals

        signals.has_epfo = True
        signals.current_employee_count = history[0].get("employee_count", 0)

        # Track workforce headcount drops
        headcounts = [m["employee_count"] for m in history]
        if len(headcounts) >= 2:
            if headcounts[0] < headcounts[-1]:
                signals.payroll_stability = "shrinking"
            elif headcounts[0] > headcounts[-1]:
                signals.payroll_stability = "growing"
            else:
                signals.payroll_stability = "stable"
                
        return signals