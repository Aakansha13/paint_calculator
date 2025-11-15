# Test Plan and Issues Encountered

## Test Plan

### Overview
This document outlines the testing strategy for the Paint Calculator application. The testing approach includes unit tests for API functions and end-to-end (E2E) tests using Playwright to verify the complete user workflow.

### Test Levels

#### 1. Unit Tests (`tests/test_api.py`)
**Purpose**: Test individual functions in isolation to ensure correctness of calculations and data transformations.

**Test Coverage**:
- `calculate_feet()` function
  - Basic room calculations
  - Square rooms
  - Large dimensions
  - Small dimensions
  - Verification of formula: `((Length * 2) + (Width * 2)) * Height`

- `calculate_gallons_required()` function
  - Exact coverage matches
  - Rounding up behavior
  - Less than one gallon cases
  - Multiple gallon requirements
  - Edge cases (zero feet)

- `sanitize_input()` function
  - Positive integers
  - Negative number conversion to absolute value
  - Zero handling
  - String to integer conversion
  - Float string handling

#### 2. Integration Tests (`tests/test_routes.py`)
**Purpose**: Test Flask routes and API endpoints to ensure proper request/response handling.

**Test Coverage**:
- Index route (`/`)
  - Page loads correctly
  - Content is displayed

- Dimensions route (`/dimensions`)
  - Valid room numbers
  - Negative number sanitization
  - Zero rooms handling
  - Missing parameter handling

- Results route (`/results`)
  - Valid form submission
  - Multiple rooms handling

- API Calculate endpoint (`/api/v1/calculate`)
  - Single room calculation
  - Multiple rooms calculation
  - Rounding up verification
  - Invalid JSON handling
  - Missing fields handling

#### 3. End-to-End Tests (`tests/test_e2e.py`)
**Purpose**: Test the complete user workflow from start to finish using browser automation.

**Test Coverage**:
- Home page loading and display
- Navigation flow (Home → Dimensions → Results)
- Form input and submission
- Multiple rooms handling
- Results modal display and calculations
- Negative input sanitization
- Form validation
- Navigation back to home
- Footer information display

### Test Execution Strategy

**Unit Tests**: Fast execution, run frequently during development
**Integration Tests**: Medium execution time, run before commits
**E2E Tests**: Slower execution, run before releases or in CI/CD

**Recommended Test Execution Levels**:
- **Development**: Unit tests + Integration tests
- **Pre-commit**: All tests (unit + integration)
- **CI/CD Pipeline**: All tests including E2E
- **Pre-release**: Full test suite with extended scenarios

## Issues Encountered and Solutions

### Bug #1: Incorrect Surface Area Calculation
**Problem**: The `calculate_feet()` function was using `length * width * height` instead of the correct formula `((Length * 2) + (Width * 2)) * Height`.

**Impact**: This would calculate volume instead of surface area, leading to incorrect paint requirements.

**Solution**: Updated the function to use the correct formula for calculating wall surface area.

**Location**: `paint_calculator/api.py`, line 31

### Bug #2: Incorrect Rounding Direction
**Problem**: The `calculate_gallons_required()` function used `math.floor()` which rounds down, but the documentation stated it should round up.

**Impact**: Customers would be short on paint if their requirements fell between whole gallons.

**Solution**: Changed `math.floor()` to `math.ceil()` to properly round up gallons.

**Location**: `paint_calculator/api.py`, line 40

### Bug #3: Coverage Constant Mismatch
**Problem**: The code used 350 square feet per gallon, but the footer specified 400 square feet per gallon.

**Impact**: Inconsistent messaging between UI and backend calculations.

**Solution**: Updated the constant to 400 to match the footer specification.

**Location**: `paint_calculator/api.py`, line 44

### Bug #4: Config Import Path Issue
**Problem**: The `__init__.py` file tried to import 'config' directly, which would fail if the package is installed.

**Impact**: Potential import errors when running as an installed package.

**Solution**: Updated to use 'paint_calculator.config' for proper package-relative import.

**Location**: `paint_calculator/__init__.py`, line 7

### Bug #5: Home Button Not Functional
**Problem**: The home button on the results page had `action="#"` which prevented navigation back to home.

**Impact**: Users couldn't navigate back to the home page from results.

**Solution**: Updated form action to `"/"` and changed method to `get` to properly navigate to home.

**Location**: `paint_calculator/templates/results.html`, line 42

### E2E Testing Challenges

#### Challenge #1: AJAX Timing
**Problem**: The results page uses a 5-second setTimeout before making the AJAX call to populate results.

**Solution**: Added `page.wait_for_timeout(6000)` in E2E tests to wait for the AJAX call to complete. This is acceptable for E2E tests but suggests the application could be improved to use event-driven loading instead of fixed timeouts.

**Recommendation**: Consider using Promise-based loading indicators or event listeners that can be more reliably tested.

#### Challenge #2: Dynamic Content Loading
**Problem**: The results modal content is populated via JavaScript after page load.

**Solution**: Tests wait for both the timeout and API response before asserting on content. This ensures tests are reliable but slower.

**Recommendation**: Consider adding loading states or data attributes that can be waited for more deterministically.

### Test Data Considerations

**Positive Test Cases**: Valid inputs, normal usage scenarios
**Negative Test Cases**: Invalid inputs, edge cases (zero, negative numbers)
**Boundary Test Cases**: Exact coverage matches, rounding boundaries

### Future Improvements

1. **API Response Time**: Consider reducing or making configurable the setTimeout delay
2. **Error Handling**: Add more comprehensive error handling tests
3. **Performance Tests**: Add tests for large numbers of rooms
4. **Accessibility Tests**: Add Playwright accessibility testing
5. **Mobile Responsiveness**: Add viewport tests for different screen sizes

## Test Execution Instructions

Followed README.md file instructions for running the tests.

## Execution Outcome and Troubleshooting Summary

All 37 tests are now running smoothly (unit, integration, and E2E). Below is a concise log of issues encountered during automation and how they were resolved, while keeping README instructions intact.

### Summary of Issues Encountered

1) Calculation correctness bugs (fixed in app code)
- Incorrect surface area formula in `calculate_feet()` (volume used instead of wall area) → corrected to `((L*2)+(W*2))*H`.
- Rounding direction in `calculate_gallons_required()` used `floor` → changed to `ceil` per spec.
- Paint coverage constant mismatch (350 vs footer 400) → standardized to 400.

2) Config import path
- `paint_calculator/__init__.py` imported `config` as a top-level module → changed to `paint_calculator.config` to work when installed.

3) Results page home navigation
- Form used `action="#"` and POST, which didn’t navigate home → switched to `action="/"` with GET.

4) Input sanitization and API validation
- `sanitize_input` failed on floats/None → updated to safely handle `None`, float strings, and negatives via `float → floor → abs`.
- API now returns 400 for invalid JSON/missing fields to avoid 500s.

5) Playwright environment and runner behavior
- Missing Playwright browsers caused hard errors → E2E fixture skips with a clear message until `python -m playwright install chromium` is run.
- Default test run should exclude E2E per assessment flow → tests marked `@pytest.mark.e2e` and `pytest.ini` uses `-m "not e2e"` by default.
- Running only E2E: `pytest -m e2e -v` (with server running on 9200).
- Running all tests together (overriding default): `pytest -v -m "e2e or not e2e"`.

6) E2E locator stability and URL quirks
- Strict-mode violations (ambiguous `text=` locators collided with footer/code) → switched to scoped CSS selectors and role-based selectors within specific tables/modals.
- Home URL sometimes included trailing `?` after form submit → relaxed assertion to accept optional `?`.

7) Server availability during E2E
- `net::ERR_CONNECTION_REFUSED` occurred when server wasn’t running on 9200 → ensured app started via `python paint_calculator/run.py` before E2E.

### Final Run States

- Unit + Integration (default): `pytest -v` (E2E excluded by default).
- E2E only: start app (9200) then `pytest -m e2e -v`.
- All tests together: start app (9200) then `pytest -v -m "e2e or not e2e"`.

Result: 37 tests total executing successfully under the appropriate conditions.
