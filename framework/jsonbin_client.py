import os
import requests

from dotenv import load_dotenv

load_dotenv()


class JSONBinClient:

    def __init__(self):

        self.base_url = os.getenv(
            "JSONBIN_BASE_URL",
            "https://api.jsonbin.io/v3"
        )

        self.api_key = os.getenv("JSONBIN_MASTER_KEY")

        if not self.api_key:
            raise ValueError(
                "JSONBIN_MASTER_KEY is not configured"
            )

        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key
        }

        self.timeout = 20

    def create_bin(self, payload):

        return requests.post(
            f"{self.base_url}/b",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )

    def read_bin(self, bin_id):

        return requests.get(
            f"{self.base_url}/b/{bin_id}",
            headers=self.headers,
            timeout=self.timeout
        )

    def delete_bin(self, bin_id):

        return requests.delete(
            f"{self.base_url}/b/{bin_id}",
            headers=self.headers,
            timeout=self.timeout
        )