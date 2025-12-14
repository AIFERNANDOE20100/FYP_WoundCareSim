# app/utils/validators.py
from typing import Dict, Any, List
from pydantic import BaseModel, validator, Field
from typing import Dict, List

REQUIRED_FIELDS = [
    "scenario_id",
    "scenario_title",
    "patient_history",
    "wound_details",
    "assessment_questions",
    "evaluation_criteria",
    "vector_store_namespace"
]


def validate_scenario_payload(data: Dict):
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    if not isinstance(data.get("assessment_questions", []), list):
        raise ValueError("assessment_questions must be a list")

    for q in data.get("assessment_questions", []):
        if "question" not in q or "answer" not in q:
            raise ValueError("Each MCQ must have question and answer")

    if not isinstance(data.get("evaluation_criteria", {}), dict):
        raise ValueError("evaluation_criteria must be a dictionary")

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

# ==================== SCENARIO VALIDATION ====================

def validate_scenario_body(scenario_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate complete scenario data structure.
    
    Args:
        scenario_data: Dictionary containing scenario fields
        
    Returns:
        Validated scenario data
        
    Raises:
        ValidationError: If validation fails
    """
    required_fields = [
        "scenario_title",
        "patient_history",
        "wound_details",
        "required_conversation_points",
        "assessment_questions",
        "evaluation_criteria",
        "created_by"
    ]
    
    # Check required fields exist
    missing_fields = [field for field in required_fields if field not in scenario_data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate each field is not empty
    errors = []
    
    if not scenario_data.get("scenario_title", "").strip():
        errors.append("scenario_title cannot be empty")
    
    if not scenario_data.get("patient_history", "").strip():
        errors.append("patient_history cannot be empty")
    
    if not scenario_data.get("wound_details", "").strip():
        errors.append("wound_details cannot be empty")
    
    if not scenario_data.get("created_by", "").strip():
        errors.append("created_by cannot be empty")
    
    # Validate list fields
    if not isinstance(scenario_data.get("required_conversation_points"), list):
        errors.append("required_conversation_points must be a list")
    elif len(scenario_data["required_conversation_points"]) == 0:
        errors.append("required_conversation_points cannot be empty")
    
    if not isinstance(scenario_data.get("assessment_questions"), list):
        errors.append("assessment_questions must be a list")
    elif len(scenario_data["assessment_questions"]) == 0:
        errors.append("assessment_questions cannot be empty")
    
    # Validate evaluation criteria
    if not isinstance(scenario_data.get("evaluation_criteria"), dict):
        errors.append("evaluation_criteria must be a dictionary")
    elif len(scenario_data["evaluation_criteria"]) == 0:
        errors.append("evaluation_criteria cannot be empty")
    
    if errors:
        raise ValidationError(f"Validation failed: {'; '.join(errors)}")
    
    # Validate MCQ structure
    try:
        validate_mcq_list(scenario_data["assessment_questions"])
    except ValidationError as e:
        errors.append(str(e))
    
    if errors:
        raise ValidationError(f"Validation failed: {'; '.join(errors)}")
    
    return scenario_data


def validate_mcq_structure(mcq: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a single MCQ question structure.
    
    Expected structure:
    {
        "question": "What is the wound type?",
        "options": ["A. Pressure ulcer", "B. Diabetic ulcer", "C. Venous ulcer"],
        "correct_answer": "A",
        "points": 10
    }
    
    Args:
        mcq: Dictionary containing MCQ data
        
    Returns:
        Validated MCQ data
        
    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["question", "options", "correct_answer"]
    
    # Check required fields
    missing_fields = [field for field in required_fields if field not in mcq]
    if missing_fields:
        raise ValidationError(f"MCQ missing required fields: {', '.join(missing_fields)}")
    
    errors = []
    
    # Validate question is not empty
    if not mcq.get("question", "").strip():
        errors.append("MCQ question cannot be empty")
    
    # Validate options
    if not isinstance(mcq.get("options"), list):
        errors.append("MCQ options must be a list")
    elif len(mcq["options"]) < 2:
        errors.append("MCQ must have at least 2 options")
    else:
        # Check all options are non-empty strings
        empty_options = [i for i, opt in enumerate(mcq["options"]) if not str(opt).strip()]
        if empty_options:
            errors.append(f"MCQ options at indices {empty_options} are empty")
    
    # Validate correct_answer
    if not mcq.get("correct_answer", "").strip():
        errors.append("MCQ correct_answer cannot be empty")
    
    # Validate points (optional but should be positive if present)
    if "points" in mcq:
        if not isinstance(mcq["points"], (int, float)):
            errors.append("MCQ points must be a number")
        elif mcq["points"] < 0:
            errors.append("MCQ points cannot be negative")
    
    if errors:
        raise ValidationError(f"MCQ validation failed: {'; '.join(errors)}")
    
    return mcq


def validate_mcq_list(mcq_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validate a list of MCQ questions.
    
    Args:
        mcq_list: List of MCQ dictionaries
        
    Returns:
        Validated MCQ list
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(mcq_list, list):
        raise ValidationError("MCQ list must be a list")
    
    if len(mcq_list) == 0:
        raise ValidationError("MCQ list cannot be empty")
    
    errors = []
    for i, mcq in enumerate(mcq_list):
        try:
            validate_mcq_structure(mcq)
        except ValidationError as e:
            errors.append(f"MCQ {i+1}: {str(e)}")
    
    if errors:
        raise ValidationError(f"MCQ list validation failed: {'; '.join(errors)}")
    
    return mcq_list


def validate_empty_fields(data: Dict[str, Any], fields: List[str]) -> None:
    """
    Check if specified fields are empty.
    
    Args:
        data: Dictionary to validate
        fields: List of field names to check
        
    Raises:
        ValidationError: If any field is empty
    """
    empty_fields = []
    
    for field in fields:
        value = data.get(field)
        
        # Check for None or empty string
        if value is None or (isinstance(value, str) and not value.strip()):
            empty_fields.append(field)
        
        # Check for empty list
        elif isinstance(value, list) and len(value) == 0:
            empty_fields.append(field)
        
        # Check for empty dict
        elif isinstance(value, dict) and len(value) == 0:
            empty_fields.append(field)
    
    if empty_fields:
        raise ValidationError(f"Empty fields detected: {', '.join(empty_fields)}")


# ==================== EVALUATION CRITERIA VALIDATION ====================

def validate_evaluation_criteria(criteria: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate evaluation criteria structure.
    
    Expected structure:
    {
        "history": {
            "required_points": ["pain location", "duration"],
            "weight": 0.2
        },
        "assessment": {
            "required_points": ["wound size", "wound depth"],
            "weight": 0.3
        },
        ...
    }
    
    Args:
        criteria: Dictionary containing evaluation criteria
        
    Returns:
        Validated criteria
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(criteria, dict):
        raise ValidationError("Evaluation criteria must be a dictionary")
    
    if len(criteria) == 0:
        raise ValidationError("Evaluation criteria cannot be empty")
    
    errors = []
    total_weight = 0.0
    
    for step, step_criteria in criteria.items():
        if not isinstance(step_criteria, dict):
            errors.append(f"Criteria for '{step}' must be a dictionary")
            continue
        
        # Check for required_points
        if "required_points" not in step_criteria:
            errors.append(f"Criteria for '{step}' missing 'required_points'")
        elif not isinstance(step_criteria["required_points"], list):
            errors.append(f"Criteria for '{step}': 'required_points' must be a list")
        
        # Check for weight (optional but should sum to 1.0 if all present)
        if "weight" in step_criteria:
            if not isinstance(step_criteria["weight"], (int, float)):
                errors.append(f"Criteria for '{step}': weight must be a number")
            elif step_criteria["weight"] < 0 or step_criteria["weight"] > 1:
                errors.append(f"Criteria for '{step}': weight must be between 0 and 1")
            else:
                total_weight += step_criteria["weight"]
    
    # Check if weights sum to approximately 1.0 (allow small floating point errors)
    if total_weight > 0 and abs(total_weight - 1.0) > 0.01:
        errors.append(f"Weights should sum to 1.0, got {total_weight}")
    
    if errors:
        raise ValidationError(f"Evaluation criteria validation failed: {'; '.join(errors)}")
    
    return criteria


# ==================== SESSION VALIDATION ====================

def validate_session_id(session_id: str) -> str:
    """
    Validate session ID format.
    
    Args:
        session_id: Session ID to validate
        
    Returns:
        Validated session ID
        
    Raises:
        ValidationError: If invalid
    """
    if not session_id or not isinstance(session_id, str):
        raise ValidationError("Session ID must be a non-empty string")
    
    if not session_id.startswith("sess_"):
        raise ValidationError("Session ID must start with 'sess_'")
    
    return session_id


def validate_scenario_id(scenario_id: str) -> str:
    """
    Validate scenario ID format.
    
    Args:
        scenario_id: Scenario ID to validate
        
    Returns:
        Validated scenario ID
        
    Raises:
        ValidationError: If invalid
    """
    if not scenario_id or not isinstance(scenario_id, str):
        raise ValidationError("Scenario ID must be a non-empty string")
    
    return scenario_id


# ==================== UTILITY FUNCTIONS ====================

def sanitize_string(text: str, max_length: int = None) -> str:
    """
    Sanitize string input by stripping whitespace and optionally truncating.
    
    Args:
        text: Input string
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    sanitized = text.strip()
    
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_field_types(data: Dict[str, Any], field_types: Dict[str, type]) -> None:
    """
    Validate that fields have correct types.
    
    Args:
        data: Dictionary to validate
        field_types: Dictionary mapping field names to expected types
        
    Raises:
        ValidationError: If type validation fails
    """
    errors = []
    
    for field, expected_type in field_types.items():
        if field in data and not isinstance(data[field], expected_type):
            actual_type = type(data[field]).__name__
            expected_type_name = expected_type.__name__
            errors.append(
                f"Field '{field}' has type {actual_type}, expected {expected_type_name}"
            )
    
    if errors:
        raise ValidationError(f"Type validation failed: {'; '.join(errors)}")