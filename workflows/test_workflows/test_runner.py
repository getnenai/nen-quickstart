"""
Test Runner for NenAI Workflow Validation

This script runs all test workflows through nen_validate and reports results.
Run this from Cursor AI to execute the full test suite.
"""

# Valid test cases - should all PASS validation
VALID_TESTS = [
    "valid/minimal-valid",
    "valid/full-featured-valid",
    "valid/optional-fields-valid",
    "valid/nested-models-valid",
    "valid/list-types-valid",
    "valid/union-types-valid",
    "valid/field-validators-valid",
]

# Invalid test cases - should all FAIL validation
INVALID_TESTS = [
    "invalid/missing-input-model",
    "invalid/missing-output-model",
    "invalid/missing-run-function",
    "invalid/wrong-function-signature",
    "invalid/no-success-field",
    "invalid/syntax-error",
    "invalid/missing-imports",
    "invalid/invalid-pydantic-model",
    "invalid/wrong-return-type",
    "invalid/no-docstring",
    "invalid/escaped-docstring",
    "invalid/input-not-basemodel",
    "invalid/output-not-basemodel",
    "invalid/run-wrong-args",
]


def main():
    """
    Run all validation tests and report results.
    
    NOTE: This is meant to be executed by Cursor AI, not run directly.
    The AI will iterate through each test case and call nen_validate.
    """
    print("NenAI Workflow Validation Test Suite")
    print("=" * 60)
    print()
    print("Instructions for Cursor AI:")
    print("1. For each test in VALID_TESTS:")
    print("   - Read the workflow file")
    print("   - Call nen_validate()")
    print("   - Verify it PASSES")
    print()
    print("2. For each test in INVALID_TESTS:")
    print("   - Read the workflow file")
    print("   - Call nen_validate()")
    print("   - Verify it FAILS with appropriate error")
    print()
    print("3. Report summary:")
    print("   - Total tests run")
    print("   - Passed/Failed counts")
    print("   - Any unexpected results")
    print()
    print(f"Total Valid Tests: {len(VALID_TESTS)}")
    print(f"Total Invalid Tests: {len(INVALID_TESTS)}")
    print(f"Total Tests: {len(VALID_TESTS) + len(INVALID_TESTS)}")


if __name__ == "__main__":
    main()
