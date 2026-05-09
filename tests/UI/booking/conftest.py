import pytest
import random


@pytest.fixture(scope="function")
def test_card_info():
    card_list = [
        {
            "card_number": "4242424242424242",
            "expiration_date": "12/28",
            "cvv": "123",
            "zip_code": "12345",
            "country": "US",
        },
        {
            "card_number": "5555555555554444",
            "expiration_date": "11/28",
            "cvv": "456",
            "zip_code": "54321",
            "country": "US",
        },
        {
            "card_number": "378282246310005",
            "expiration_date": "10/28",
            "cvv": "789",
            "zip_code": "67890",
            "country": "US",
        },
    ]

    return random.choice(card_list)
