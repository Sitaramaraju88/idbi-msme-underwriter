# agents/scoring_agent.py
import os
from agents.base_agent import AgentSignals
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class ScoringAgent:
    def __init__(self):
        # Fall back to a mock LLM string if the user hasn't set an environment API key yet
        self.api_key_configured = os.getenv("OPENAI_API_KEY") is not None
        if self.api_key_configured:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    def calculate_scores(self, s: AgentSignals) -> dict:
        """Computes objective, multi-dimensional credit matrix scores out of 1000."""
        
        # Pillar 1: Revenue & Scale Stability (Max: 300)
        p1 = 150  # base score for having standard vintage
        if s.gst_vintage_months > 24: p1 += 50
        if s.turnover_growth_trend == "growing": p1 += 70
        elif s.turnover_growth_trend == "stable": p1 += 50
        else: p1 -= 50  # penalty for declining turnover
        if s.concentration_risk_pct < 25.0: p1 += 30
        p1 = max(0, min(300, p1))

        # Pillar 2: Liquidity & Cash Flow (Max: 350)
        p2 = 100
        if s.upi_volume_90_days_inr > 800000: p2 += 100
        elif s.upi_volume_90_days_inr > 300000: p2 += 50
        if s.upi_velocity_trend == "stable": p2 += 50
        if s.average_daily_balance_inr > 40000: p2 += 100
        elif s.average_daily_balance_inr > 10000: p2 += 50
        p2 = max(0, min(350, p2))

        # Pillar 3: Operational Formality (Max: 150)
        p3 = 50
        if s.has_epfo:
            p3 += 50
            if s.payroll_stability == "growing": p3 += 50
            elif s.payroll_stability == "stable": p3 += 30
        else:
            p3 += 20  # micro-enterprises are safely capped without crashing
        p3 = max(0, min(150, p3))

        # Pillar 4: Transactional Maturity & Clean Records (Max: 200)
        p4 = 150
        if s.gst_filing_punctuality_pct > 90.0: p4 += 50
        if s.critical_risk_flag:
            p4 -= 150  # heavy penalty for cheque bounces/mandate failures
        p4 = max(0, min(200, p4))

        total_score = p1 + p2 + p3 + p4
        
        # Risk Category classification
        if total_score >= 750: grade = "LOW RISK (Green)"
        elif total_score >= 550: grade = "MEDIUM RISK (Amber)"
        else: grade = "HIGH RISK (Red)"

        return {
            "total_score": total_score,
            "grade": grade,
            "breakdown": {
                "revenue_stability": p1,
                "cash_flow_consistency": p2,
                "operational_formality": p3,
                "transaction_maturity": p4
            }
        }

    def generate_credit_memo(self, s: AgentSignals, score_results: dict) -> str:
        """Generates human-readable narrative context via LLM or fallback interpreter."""
        
        context_summary = f"""
        Business Analytics Metrics Summary:
        - Total Alternate Credit Score: {score_results['total_score']}/1000 (Grade: {score_results['grade']})
        - Revenue Pillar: {score_results['breakdown']['revenue_stability']}/300, Trend: {s.turnover_growth_trend}
        - Cash Flow Pillar: {score_results['breakdown']['cash_flow_consistency']}/350, 90-Day UPI Vol: ₹{s.upi_volume_90_days_inr}
        - EPFO Infrastructure: {'Active' if s.has_epfo else 'None/Informal'}, Headcount: {s.current_employee_count}
        - Banking Flags: Cheque Bounces: {s.cheque_bounces_6m}, Mandate Failures: {s.mandate_failures_6m}
        """

        if not self.api_key_configured:
            # Fallback human-readable output logic if running without API keys
            return f"### 📊 Automated Assessment Notes\n\n* **Risk Grade**: {score_results['grade']}\n* **Revenue Vector**: Business registers a `{s.turnover_growth_trend}` trajectory with a customer concentration factor of {s.concentration_risk_pct}%.\n* **Banking Integrity Checks**: Found {s.cheque_bounces_6m} active cheque bounces. Critical vulnerability status flagged as: `{s.critical_risk_flag}`."

        # Execute fully contextual agent reasoning
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert IDBI Bank credit underwriter. Write a concise, bulleted Credit Memo based on the alternate data signals provided. Do not use generic prose. Call out specific strengths, risks, and a clear underwriting recommendation."),
            ("human", "Analyze these metrics and compile the memo:\n\n{metrics}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"metrics": context_summary})
        return response.content