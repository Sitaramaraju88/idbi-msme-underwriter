# services/aa_service.py
import json
import os

class AAService:
    def __init__(self, mock_dir="data/mock_personas"):
        self.mock_dir = mock_dir

    def request_consent(self, msme_id: str) -> str:
        """Simulates AA consent handshaking. Returns a mock consent handle."""
        return f"aa-consent-handle-{msme_id}-xyz"

    def fetch_consented_banking_data(self, consent_handle: str) -> dict:
        """Pulls multi-bank normalized data once consent is authorized."""
        # Extract msme_id out of our mock handle string
        try:
            msme_id = consent_handle.split("-")[3]
            filename = f"msme_{msme_id}.json"
            filepath = os.path.join(self.mock_dir, filename)
            
            with open(filepath, "r") as f:
                data = json.load(f)
            return data["aa_payload"]
        except Exception:
            raise PermissionError("Invalid or expired Account Aggregator consent handle.")