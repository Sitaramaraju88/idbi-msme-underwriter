# services/uli_service.py
import json
import os

class ULIService:
    def __init__(self, mock_dir="data/mock_personas"):
        self.mock_dir = mock_dir

    def _load_msme_file(self, msme_id: str) -> dict:
        filename = f"msme_{msme_id}.json"
        filepath = os.path.join(self.mock_dir, filename)
        
        if not os.path.exists(filepath):
            raise ValueError(f"MSME ID {msme_id} not found in ULI Sandbox.")
            
        with open(filepath, "r") as f:
            return json.load(f)

    def get_gst_data(self, msme_id: str) -> dict:
        """Simulates ULI API call to GSTN Network."""
        data = self._load_msme_file(msme_id)
        return data["uli_payload"]["gst_data"]

    def get_upi_data(self, msme_id: str) -> dict:
        """Simulates ULI API call to NPCI/UPI Merchant Logs."""
        data = self._load_msme_file(msme_id)
        return data["uli_payload"]["upi_data"]

    def get_epfo_data(self, msme_id: str) -> dict:
        """Simulates ULI API call to EPFO Portal."""
        data = self._load_msme_file(msme_id)
        return data["uli_payload"]["epfo_data"]