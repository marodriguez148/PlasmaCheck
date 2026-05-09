# Assumptions, Scalability, and what you would implement in the future

## Assumptions Made

- **No database access** — All tests were written against the staging environment directly. Dynamic IDs (encounter IDs, location IDs, package IDs) were either generated client-side (UUIDs) or assumed from observed network traffic. With DB access, fixtures could seed and tear down test data deterministically.
- **Single user scope** — Tests run against a shared QA user account. This creates potential state conflicts if tests run in parallel (e.g., `is_appointments_empty()` depends on prior booking history).
- **Stable staging environment** — The staging environment is assumed to be available and in a consistent state. No mocking or contract testing is in place for API responses.
- **Bearer token via Playwright interception** — Auth token capture relies on reloading the page and intercepting an authenticated request, which assumes the app always re-fires such a request on reload.

---

## Scalability Improvements

- **Parallel execution** — `plasma_check.py` supports `pytest-xdist` via `--workers`, but the shared `page` fixture is session-scoped, which would break under parallelism. Each worker would need its own browser context and isolated test user.
- **Database models with SQLAlchemy** — With DB access, test data setup/teardown could be handled programmatically — creating appointments, encounters, and users as needed rather than relying on pre-existing state.
- **Allure reporting** — Replace the current log files with Allure reports to capture screenshots, network calls, and step-by-step test results in a visual dashboard.
- **Component library expansion** — The accordion and dropdown components are a good foundation. Breadcrumb navigation, encounter cards, and location cards would be natural next additions to enable deeper page-level assertions.

---

## CI/CD Integration

- Add a **GitHub Actions workflow** (or Jenkinsfile) that installs dependencies, runs `playwright install`, and executes `python plasma_check.py --headless` on pull requests.
- Store credentials as **environment secrets** rather than hardcoding them in `constants.py`.
- Publish the HTML or Allure report as a CI artifact after each run.

---

## What I Would Test Next

- Full **sign-up flow** linked into the booking flow for new users.
- **Provider portal** login at minimum, and appointment management if data allows.
- More **API coverage** — booking stage transitions, appointment cancellation, and medical questionnaire — with proper fixture-managed encounter IDs from the DB.