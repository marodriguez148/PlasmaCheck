import uuid

from datetime import datetime
from base_api_test import BaseAPITest
from utils.logger import get_logger

logger = get_logger(__name__)

class TestBookingAPI(BaseAPITest):
    def test_get_licensed_states(self, user_token):

        endpoint = "/individuals/api/users/getLicensedStates"
        headers = {
            "sentry-trace": "39cfc957c8e444dea1ebd5edb4fbb3a0-80b9f649aea43fd6-1",
            "baggage": "sentry-environment=stage,sentry-release=4b4f624ddf03d48b08cd15f88ec6d8ca7a8373e2,sentry-public_key=dfd2428f9e0d58df5404bed162a34002,sentry-trace_id=39cfc957c8e444dea1ebd5edb4fbb3a0,sentry-transaction=sign-up%2FSelectPlan,sentry-sampled=true,sentry-sample_rand=0.18059224144427588,sentry-sample_rate=1",
            "Origin": "https://myezra-staging.ezra.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=0"
        }
        response = self.request("GET", endpoint, token=user_token, headers=headers)
        
        expected_states = ["AK","AL","AS","AZ","CA","CO","CT","DE","FL","KS","KY","LA","MN","NJ","NY","TN","TX","UT"]
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        licensed_states = response.json()
        assert isinstance(licensed_states, list), f"Expected licensed states to be a list, got {type(licensed_states)}"
        assert licensed_states == expected_states, "Expected licensed states list to equal expected list of states"

    def test_booking_stages(self, user_token):
        endpoint = "/individuals/api/members/bookingstage"
        encounter_id = str(uuid.uuid4())  # Generate a random UUID for testing
        headers = {
            "sentry-trace": "53300aaf2a8d4851aa050888df0c4a8d-84b6d71bbebcb667-1",
            "baggage": "sentry-environment=stage,sentry-release=4b4f624ddf03d48b08cd15f88ec6d8ca7a8373e2,sentry-public_key=dfd2428f9e0d58df5404bed162a34002,sentry-trace_id=53300aaf2a8d4851aa050888df0c4a8d,sentry-transaction=sign-up%2FSelectPlan,sentry-sampled=true,sentry-sample_rand=0.17223341171846684,sentry-sample_rate=1",
            "Origin": "https://myezra-staging.ezra.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
        }
        stage_list = ["SCAN_SELECTION_PAGE", "LOCATION_PAGE", "PAYMENT_PAGE"]
        for stage in stage_list:
            json_data = {
                "encounterId": encounter_id,
                "memberId": "1bff6562-96d3-4585-ad22-767a9081ac62", #Default qa user member_id
                "stage": stage,
                "visitedOn": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now().microsecond // 1000:03d}Z"
            }
            response = self.request("POST", endpoint, token=user_token, headers=headers, json=json_data)
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"