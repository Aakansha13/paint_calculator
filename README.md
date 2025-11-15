## Synopsis

The **Paint Calculator** is a hypothetical project that calculates how many gallons of paint would be required to paint a number of rooms.

## Requirements

* Python 3
* Pip

## What we're looking for

* Install Python / Pip
* Run application
* Write unit tests against the application.
* Write playwright E2E tests against the application
* You are allowed to change any of the source code as you see fit to make things easier for yourself. You are encouraged to fix any bugs you discover.
* Explain any problems you had while writing the tests, and what you did to make it easier. Pointing to localhost for the application is OK.

## Instructions

Because each applicant's code should be secret from one another, we should not submit it to the same repo.

1. Clone the repo (do not fork)
2. Create a new public repo on Github
3. Add the new repo as a new remote
* `git remote add acme <url>`
4. Initialize the new repo with what is cloned
* `git push acme master`
5. Create a new branch off of master to put your changes on
6. Run the application locally
* `pip3 install -e .`
* `python3 paint_calculator/run.py`
7. Perform testing and debugging activities

## Submitting 

To make it easier on everybody, it's best if we use a PR to diff what work was completed.

1. Make any and all commits to your new branch and push the changes
* `git push acme <branch>`
2. Create a PR to your new repo
3. Make sure you include your test plan and any automated tests, as well as update this README to instruct someone on how to run the tests
4. Include any other text in a file - which tests would be suited for a different level of execution, or any problems encountered...etc
5. Send the link to the PR

## Running Tests

This project includes unit tests, integration tests, and end-to-end (E2E) tests using Playwright.

### Prerequisites for Testing

1. Install the application and test dependencies:
   ```bash
   pip3 install -e .
   pip3 install -e ".[test]"
   ```

2. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

### Running Unit Tests

Unit tests verify the core calculation functions:

```bash
pytest tests/test_api.py -v
```

### Running Integration Tests

Integration tests verify Flask routes and API endpoints:

```bash
pytest tests/test_routes.py -v
```

### Running All Tests Together

Run all unit and integration tests:

```bash
pytest tests/test_api.py tests/test_routes.py -v
```

### Running End-to-End Tests

E2E tests require the application to be running. Open a terminal and start the application:

```bash
python3 paint_calculator/run.py
```

In another terminal, run the E2E tests:

```bash
pytest tests/test_e2e.py -v
```

The E2E tests will connect to `http://localhost:9200` by default.

### Running Tests with Coverage

To see test coverage:

```bash
pytest --cov=paint_calculator --cov-report=html tests/
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

### Test Files Overview

- `tests/test_api.py` - Unit tests for API calculation functions
- `tests/test_routes.py` - Integration tests for Flask routes
- `tests/test_e2e.py` - End-to-end tests using Playwright
- `tests/conftest.py` - Pytest fixtures for Playwright

### Test Plan and Issues

See `TEST_PLAN.md` for detailed information about:
- Test strategy and coverage
- Issues encountered during testing
- Solutions implemented
- Recommendations for future improvements

## Bugs Fixed

Several bugs were discovered and fixed during testing:

1. **Surface Area Calculation Bug**: Fixed incorrect formula in `calculate_feet()` function
2. **Rounding Bug**: Changed `math.floor()` to `math.ceil()` for proper rounding up
3. **Coverage Constant Mismatch**: Updated to use 400 square feet per gallon (matching footer)
4. **Config Import Path**: Fixed import path for proper package installation
5. **Home Button Navigation**: Fixed home button to properly navigate back to home page

See `TEST_PLAN.md` for detailed information about these bugs and their fixes.
