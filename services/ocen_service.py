# services/ocen_service.py
class OCENService:
    def generate_loan_offer(self, msme_id: str, score_results: dict, avg_turnover: float) -> dict:
        """
        Translates multi-dimensional alternate risk vectors into standard 
        OCEN-compliant loan product offers.
        """
        total_score = score_results["total_score"]
        grade = score_results["grade"]
        
        # Default fallback values for non-eligible entities
        eligible = False
        loan_amount = 0
        interest_rate_apr = 0.0
        tenure_months = 0
        repayment_frequency = "MONTHLY"

        # Underwriting Matrix Rule Parameters
        if total_score >= 750:
            eligible = True
            # High quality cash flows allow lending up to 1.5x average monthly sales volume
            loan_amount = int(avg_turnover * 1.5)
            interest_rate_apr = 11.5  # Premium rate for low-risk NTC profiles
            tenure_months = 24

        elif total_score >= 550:
            eligible = True
            # Medium risk caps credit limits at 0.8x monthly turnover
            loan_amount = int(avg_turnover * 0.8)
            interest_rate_apr = 15.0  # Risk premium added
            tenure_months = 12

        # Final structural encapsulation matching real public rail transaction schemas
        return {
            "ocen_tx_metadata": {
                "version": "4.0.0-rc2",
                "msme_id": msme_id,
                "underwriting_status": "APPROVED" if eligible else "REJECTED"
            },
            "offer_details": {
                "is_eligible": eligible,
                "risk_grade": grade,
                "max_credit_limit_inr": loan_amount,
                "pricing": {
                    "interest_rate_type": "FIXED",
                    "apr_percentage": interest_rate_apr,
                },
                "terms": {
                    "tenure_months": tenure_months,
                    "repayment_frequency": repayment_frequency,
                    "processing_fee_pct": 1.0 if eligible else 0.0
                }
            }
        }