# data/synthetic_generator.py
import json
import os
import random

def generate_bulk_msme_data(total_count=105):
    os.makedirs('data/mock_personas', exist_ok=True)
    
    # Target configurations
    archetypes = ["healthy_retailer", "distressed_manufacturer", "micro_no_epfo"]
    retail_names = ["Sharma", "Verma", "Gupta", "Krishna", "Balaji", "Patel", "Reddy", "Nair"]
    manuf_names = ["Apex", "Dynamic", "Om", "Vanguard", "Matrix", "Zenith", "United", "Bharat"]
    suffix = ["Stores", "Kirana", "Enterprises", "Castings", "Logistics", "Industries", "Traders"]

    for i in range(1, total_count + 1):
        # Evenly cycle through the three core archetypes
        arch = archetypes[i % 3]
        uid = f"{1000 + i}"
        
        # Base templates customized procedurally
        if arch == "healthy_retailer":
            name = f"{random.choice(retail_names)} {random.choice(suffix[:3])} #{uid}"
            vintage = random.randint(24, 60)
            base_turnover = random.randint(350000, 600000)
            
            # Generate stable/growing GST numbers
            gst_history = []
            for m in ["06", "05", "04", "03", "02", "01"]:
                variance = random.randint(-20000, 40000)
                turnover = base_turnover + variance
                gst_history.append({
                    "month": f"2026-{m}",
                    "turnover_inr": turnover,
                    "tax_paid_inr": int(turnover * 0.05),
                    "filed_on_time": random.choices([True, False], weights=[95, 5])[0]
                })
                
            upi_vol = random.randint(1000000, 1600000)
            emp_count = random.randint(3, 7)
            
            payload = {
                "metadata": {"business_name": name, "pan": f"BKPPS{uid}K", "gstin": f"27AAAAA{uid}Z1", "constitution": "Proprietorship", "segment": "NTC", "archetype": arch},
                "uli_payload": {
                    "gst_data": {"vintage_months": vintage, "gstr_3b_history": gst_history, "concentration_risk_pct": round(random.uniform(5.0, 15.0), 2)},
                    "upi_data": {"vpa": f"merchant{uid}@okhdfcbank", "summary_past_90_days": {"total_volume_inr": upi_vol, "total_transaction_count": random.randint(3000, 5000), "average_ticket_size_inr": random.randint(200, 400), "monthly_velocity_trend": "stable", "weekend_vs_weekday_ratio": round(random.uniform(1.1, 1.4), 2)}},
                    "epfo_data": {"establishment_id": f"MHBAN00{uid}000", "payroll_history": [{"month": "2026-06", "employee_count": emp_count, "total_contribution_inr": emp_count * 2000}, {"month": "2026-05", "employee_count": emp_count, "total_contribution_inr": emp_count * 2000}]}
                },
                "aa_payload": {
                    "account_summary": {"bank_name": "State Bank of India", "account_type": "CURRENT", "average_daily_balance_3m_inr": random.randint(50000, 90000), "current_balance_inr": random.randint(40000, 70000)},
                    "risk_triggers_past_180_days": {"cheque_bounces": 0, "ecs_mandate_failures": 0, "inward_outward_ratio": round(random.uniform(1.05, 1.20), 2), "days_with_negative_or_zero_balance": 0}
                }
            }

        elif arch == "distressed_manufacturer":
            name = f"{random.choice(manuf_names)} {random.choice(suffix[3:])} #{uid}"
            vintage = random.randint(12, 36)
            
            # Generate distinctly declining sales pattern
            gst_history = []
            turnover_step = random.randint(1200000, 1500000)
            for m in ["01", "02", "03", "04", "05", "06"]: # Sinking order
                turnover_step -= random.randint(80000, 150000)
                gst_history.insert(0, {
                    "month": f"2026-{m}",
                    "turnover_inr": turnover_step,
                    "tax_paid_inr": int(turnover_step * 0.18),
                    "filed_on_time": random.choices([True, False], weights=[60, 40])[0]
                })
                
            upi_vol = random.randint(200000, 500000)
            
            payload = {
                "metadata": {"business_name": name, "pan": f"AAKCA{uid}M", "gstin": f"27BBBBB{uid}Z2", "constitution": "Private Limited", "segment": "NTB", "archetype": arch},
                "uli_payload": {
                    "gst_data": {"vintage_months": vintage, "gstr_3b_history": gst_history, "concentration_risk_pct": round(random.uniform(55.0, 80.0), 2)},
                    "upi_data": {"vpa": f"factory{uid}@okaxis", "summary_past_90_days": {"total_volume_inr": upi_vol, "total_transaction_count": random.randint(80, 200), "average_ticket_size_inr": random.randint(2000, 5000), "monthly_velocity_trend": "declining", "weekend_vs_weekday_ratio": 0.2}},
                    "epfo_data": {"establishment_id": f"MHBAN00{uid}000", "payroll_history": [{"month": "2026-06", "employee_count": 10, "total_contribution_inr": 20000}, {"month": "2026-05", "employee_count": 15, "total_contribution_inr": 30000}, {"month": "2026-04", "employee_count": 20, "total_contribution_inr": 40000}]}
                },
                "aa_payload": {
                    "account_summary": {"bank_name": "HDFC Bank", "account_type": "CURRENT", "average_daily_balance_3m_inr": random.randint(1000, 5000), "current_balance_inr": random.randint(100, 1000)},
                    "risk_triggers_past_180_days": {"cheque_bounces": random.randint(2, 5), "ecs_mandate_failures": random.randint(1, 4), "inward_outward_ratio": round(random.uniform(0.75, 0.92), 2), "days_with_negative_or_zero_balance": random.randint(8, 22)}
                }
            }

        else: # micro_no_epfo
            name = f"Sai Baba {random.choice(suffix[:3])} #{uid}"
            vintage = random.randint(6, 18)
            base_turnover = random.randint(80000, 180000)
            
            gst_history = []
            for m in ["06", "05", "04", "03", "02", "01"]:
                turnover = base_turnover + random.randint(-10000, 10000)
                gst_history.append({
                    "month": f"2026-{m}",
                    "turnover_inr": turnover,
                    "tax_paid_inr": int(turnover * 0.01), # Low composition tax scheme
                    "filed_on_time": True
                })
                
            payload = {
                "metadata": {"business_name": name, "pan": f"CLKPV{uid}P", "gstin": f"27CCCCC{uid}Z3", "constitution": "Proprietorship", "segment": "NTC", "archetype": arch},
                "uli_payload": {
                    "gst_data": {"vintage_months": vintage, "gstr_3b_history": gst_history, "concentration_risk_pct": 0.0},
                    "upi_data": {"vpa": f"sai{uid}@okremit", "summary_past_90_days": {"total_volume_inr": random.randint(300000, 600000), "total_transaction_count": random.randint(1500, 2500), "average_ticket_size_inr": random.randint(100, 250), "monthly_velocity_trend": "stable", "weekend_vs_weekday_ratio": 1.0}},
                    "epfo_data": None  # System verification target for missing/informal profiles
                },
                "aa_payload": {
                    "account_summary": {"bank_name": "ICICI Bank", "account_type": "CURRENT", "average_daily_balance_3m_inr": random.randint(12000, 25000), "current_balance_inr": random.randint(5000, 18000)},
                    "risk_triggers_past_180_days": {"cheque_bounces": 0, "ecs_mandate_failures": 0, "inward_outward_ratio": 1.01, "days_with_negative_or_zero_balance": 2}
                }
            }
            
        # Save output sequentially
        with open(f"data/mock_personas/msme_{uid}.json", "w") as f:
            json.dump(payload, f, indent=4)

    print(f"🔥 Successfully baked 105 structural MSME JSON profiles inside data/mock_personas/")

if __name__ == "__main__":
    generate_bulk_msme_data()