# NenAI Workflow Validation Test Suite

This directory contains test workflows to validate the `nen_validate` tool.

## Structure

```
test_workflows/
├── valid/          # Workflows that SHOULD pass validation
└── invalid/        # Workflows that SHOULD fail validation
```

## Valid Test Cases

| Test Case | Description |
|-----------|-------------|
| `minimal-valid` | Minimal valid workflow with required components |
| `full-featured-valid` | Complex workflow with all features |
| `optional-fields-valid` | Workflow with optional fields in models |
| `nested-models-valid` | Workflow with nested Pydantic models |
| `list-types-valid` | Workflow with list type fields |
| `dict-types-valid` | Workflow with dictionary type fields |
| `union-types-valid` | Workflow with Union types |
| `field-validators-valid` | Workflow with Field validators |

## Invalid Test Cases

| Test Case | Description | Expected Error |
|-----------|-------------|----------------|
| `missing-input-model` | No Input class defined | Missing Input model |
| `missing-output-model` | No Output class defined | Missing Output model |
| `missing-run-function` | No run() function | Missing run function |
| `wrong-function-signature` | run() has wrong signature | Invalid function signature |
| `no-success-field` | Output model missing success field | Missing success field |
| `syntax-error` | Python syntax error | Syntax error |
| `missing-imports` | Missing nen.workflow imports | Import error |
| `invalid-pydantic-model` | Malformed Pydantic model | Invalid model definition |
| `wrong-return-type` | run() doesn't return Output | Wrong return type |
| `no-docstring` | Missing module docstring | Missing docstring |
| `escaped-docstring` | Malformed docstring with escapes | Syntax error |
| `input-not-basemodel` | Input class not inheriting BaseModel | Invalid model |
| `output-not-basemodel` | Output class not inheriting BaseModel | Invalid model |
| `run-wrong-args` | run() function with wrong arguments | Invalid signature |
| `multiple-run-functions` | Multiple run() functions defined | Ambiguous entry point |

## Running Tests

To test validation manually:

```python
# Read a test workflow
workflow_content = Read("workflows/test_workflows/valid/minimal-valid/workflow.py")

# Validate it
nen_validate(content=workflow_content, filename="workflow.py")
```

## Expected Behavior

- **Valid workflows**: `nen_validate()` should return success
- **Invalid workflows**: `nen_validate()` should return error with specific reason
