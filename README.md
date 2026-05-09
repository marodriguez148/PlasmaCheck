# PlasmaCheck
Automation test suite for the Ezra member-facing portal. Built with Playwright + pytest, covering UI end-to-end flows and API contract tests.

---

## Requirements

- Python 3.11+
- Google Chrome (or Chromium)

---

## Setup

**1. Clone the repository**
```bash
git clone <repo-url>
cd PlasmaCheck
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Install Playwright browsers**
```bash
playwright install
```

---

## Running Tests

Tests are run via `plasma_check.py`, a CLI wrapper around pytest.

**Run all tests**
```bash
python plasma_check.py
```

**Run a specific file**
```bash
python plasma_check.py tests/UI/booking/test_booking_scan.py
```

**Run a specific test**
```bash
python plasma_check.py tests/UI/booking/test_booking_scan.py::TestBookingScan::test_booking_scan
```

**Filter by name**
```bash
python plasma_check.py -k "login"
```

**Run in headless mode**
```bash
python plasma_check.py --headless
```

**Run with a different browser**
```bash
python plasma_check.py --browser firefox
```

**List collected tests without running**
```bash
python plasma_check.py --list
```

---

## Project Structure

```
PlasmaCheck/
├── components/         # Reusable UI components (accordion, dropdowns, etc.)
├── constants/          # URLs, credentials, shared constants
├── pages/              # Page object models
│   ├── booking_pages/  # Select plan, schedule scan, reserve appointment, confirmation
│   ├── base_page.py
│   └── login_page.py
├── tests/
│   ├── UI/             # End-to-end browser tests
│   │   ├── booking/    # Booking scan flow
│   │   └── login/      # Login / authentication
│   ├── API/            # API contract tests
│   ├── base_test.py    # Shared UI test base class
│   └── base_api_test.py# Shared API test base class
├── utils/              # Logger and shared utilities
├── plasma_check.py     # Test runner CLI
└── requirements.txt
```

---

## Test Suites

### UI Tests

| Test | Description |
|------|-------------|
| `test_member_page_login` | Logs in with valid credentials and verifies dashboard |
| `test_invalid_member_page_login` | Verifies error state for invalid credentials |
| `test_booking_scan` | Full booking flow: plan selection → scheduling → payment → confirmation |

### API Tests

| Test | Description |
|------|-------------|
| `test_get_licensed_states` | Verifies the licensed states endpoint returns the expected list |
| `test_booking_stages` | Posts each booking stage and verifies 200 responses |

---

## Configuration

Environment targets and test credentials are defined in `constants/constants.py`.

- **Member portal (staging):** `https://myezra-staging.ezra.com/`
- **Provider portal (staging):** `https://staging-hub.ezra.com/`
