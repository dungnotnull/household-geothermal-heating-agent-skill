# Hooks System Documentation

## Overview

The hooks system provides a flexible mechanism for extending skill behavior at key execution points. Hooks allow for lifecycle management, state synchronization, event emission, and custom processing without modifying core skill logic.

## Hook Types

### 1. Before Execution Hook

**Purpose**: Initialize context, validate inputs, set up logging

**Trigger**: Before main harness execution begins

**Parameters**:
- `user_query` (str): The original user query
- `context` (dict): Initial execution context

**Return**: Updated context object

**Example Implementation**:
```python
def before_execution(user_query: str, context: dict) -> dict:
    """Initialize execution context and validate inputs."""
    # Detect language
    context['language'] = detect_language(user_query)
    
    # Initialize logging
    setup_logging(context.get('log_level', 'INFO'))
    
    # Validate inputs
    if not validate_query(user_query):
        raise ValueError("Invalid query format")
    
    # Set up metrics
    context['start_time'] = time.time()
    context['tokens_used'] = 0
    
    log_event("skill.invoked", {"query_length": len(user_query)})
    
    return context
```

### 2. After Step Hook

**Purpose**: Validate step output, update state, check quality gates

**Trigger**: After each sub-skill completes

**Parameters**:
- `step_number` (int): Current step (1-6)
- `step_output` (dict): Output from the sub-skill
- `requirements` (dict): Quality gate requirements

**Return**: Validation result and updated state

**Example Implementation**:
```python
def after_step(step_number: int, step_output: dict, requirements: dict) -> dict:
    """Validate step output and update execution state."""
    # Check if step produced required outputs
    gate = requirements.get(f'G{step_number}')
    if not gate:
        return {"status": "passed", "state": {}}
    
    # Validate against gate requirements
    validation = validate_gate(step_output, gate)
    
    if not validation['passed']:
        # Attempt auto-fix
        if validation.get('auto_fix_available'):
            fixed_output = auto_fix_gate(step_output, gate)
            validation = validate_gate(fixed_output, gate)
    
    # Update state
    state_update = {
        f'step_{step_number}_output': step_output,
        f'step_{step_number}_gate_status': validation['status'],
        'limitation_flags': validation.get('limitations', [])
    }
    
    log_event(
        "gate.passed" if validation['passed'] else "gate.failed",
        {
            "step": step_number,
            "gate": gate,
            "status": validation['status'],
            "auto_fix_applied": validation.get('auto_fix_applied', False)
        }
    )
    
    return {
        "status": validation['status'],
        "state": state_update,
        "limitations": validation.get('limitations', [])
    }
```

### 3. On Error Hook

**Purpose**: Handle errors, log failures, trigger recovery

**Trigger**: When an error occurs during execution

**Parameters**:
- `error` (Exception): The error that occurred
- `context` (dict): Current execution context
- `retry_count` (int): Current retry attempt number

**Return**: Recovery action or raise exception

**Example Implementation**:
```python
def on_error(error: Exception, context: dict, retry_count: int) -> dict:
    """Handle errors with appropriate recovery strategy."""
    error_type = type(error).__name__
    error_config = get_error_config(error_type)
    
    log_event("error.occurred", {
        "error_type": error_type,
        "error_message": str(error),
        "retry_count": retry_count,
        "context": context
    })
    
    # Check if max retries exceeded
    if retry_count >= error_config.get('max_retries', 3):
        # Apply fallback or escalate
        fallback = error_config.get('fallback', 'raise')
        if fallback == 'raise':
            raise error
        return {
            "action": "fallback",
            "fallback_type": fallback,
            "limitation_flag": True
        }
    
    # Determine recovery strategy
    recovery_strategy = error_config.get('recovery', 'retry')
    
    if recovery_strategy == 'retry':
        backoff_time = calculate_backoff(retry_count, strategy='exponential')
        time.sleep(backoff_time)
        return {"action": "retry", "backoff_seconds": backoff_time}
    
    return {"action": recovery_strategy}
```

### 4. Before Output Hook

**Purpose**: Final validation, format output, apply templates

**Trigger**: Before final report is delivered to user

**Parameters**:
- `analysis_result` (dict): The complete analysis result
- `language` (str): Target output language

**Return**: Formatted and validated output

**Example Implementation**:
```python
def before_output(analysis_result: dict, language: str) -> dict:
    """Final validation and formatting of output."""
    # Validate all required sections present
    required_sections = [
        'report_metadata', 'executive_summary', 'inputs_scope',
        'evidence_collected', 'analysis_scorecard', 'action_plan',
        'academic_evidence', 'disclosure', 'verdict', 'gate_checklist'
    ]
    
    missing_sections = [
        section for section in required_sections
        if section not in analysis_result
    ]
    
    if missing_sections:
        log_event("output.missing_sections", {
            "missing": missing_sections
        })
        # Add empty sections for missing items
        for section in missing_sections:
            analysis_result[section] = None
    
    # Apply language-specific formatting
    if language == 'vi':
        analysis_result = translate_to_vietnamese(analysis_result)
    
    # Apply output template
    formatted_output = apply_output_template(analysis_result, language)
    
    # Final gate check
    gate_checklist = validate_all_gates(analysis_result)
    analysis_result['gate_checklist'] = gate_checklist
    
    log_event("output.generated", {
        "language": language,
        "sections": len(analysis_result),
        "gates_passed": gate_checklist.get('passed', 0),
        "gates_failed": gate_checklist.get('failed', 0)
    })
    
    return formatted_output
```

### 5. After Execution Hook

**Purpose**: Log completion, update metrics, cleanup

**Trigger**: After all execution completes (success or failure)

**Parameters**:
- `result` (dict): Final execution result
- `duration` (float): Total execution time in seconds
- `tokens_used` (int): Total tokens consumed

**Return**: None (cleanup only)

**Example Implementation**:
```python
def after_execution(result: dict, duration: float, tokens_used: int):
    """Log completion and update performance metrics."""
    # Calculate performance metrics
    success = result.get('success', True)
    gate_pass_rate = calculate_gate_pass_rate(result.get('gate_checklist', {}))
    
    # Log completion
    log_event("execution.completed", {
        "success": success,
        "duration_seconds": duration,
        "tokens_used": tokens_used,
        "gate_pass_rate": gate_pass_rate,
        "limitations": result.get('limitations', [])
    })
    
    # Update performance metrics
    update_metrics({
        'execution_time': duration,
        'tokens_used': tokens_used,
        'gate_pass_rate': gate_pass_rate,
        'success': success
    })
    
    # Cleanup
    cleanup_temp_files()
    clear_cache(if_expired=True)
    
    # Check performance against targets
    if duration > config.performance.target_execution_time_seconds:
        log_warning(f"Execution exceeded target time: {duration}s")
    
    if tokens_used > config.performance.target_tokens_per_run:
        log_warning(f"Token usage exceeded target: {tokens_used}")
```

## Event System

### Event Types

| Event | Description | Data |
|-------|-------------|------|
| `skill.invoked` | Skill triggered by user | query_length, language |
| `step.started` | Sub-skill execution started | step_number, skill_name |
| `step.completed` | Sub-skill execution completed | step_number, success, duration |
| `gate.passed` | Quality gate passed | gate_name, step |
| `gate.failed` | Quality gate failed | gate_name, step, auto_fix |
| `data.fetch` | Data fetch from external source | source, success, duration |
| `error.occurred` | Error during execution | error_type, message, retry |
| `limitation.flagged` | Limitation detected and flagged | limitation_type, level |
| `output.generated` | Final report generated | language, sections, gates |

### Event Emission

Events are emitted using the `emit_event()` function:

```python
def emit_event(event_type: str, data: dict):
    """Emit an event with structured data."""
    event = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'data': data,
        'context': {
            'skill': config.system.skill_name,
            'version': config.system.skill_version,
            'execution_id': get_execution_id()
        }
    }
    
    # Log event
    if config.logging.events.log_all_events or \
       event_type in config.logging.events.monitored_events:
        log_event(event)
    
    # Trigger event handlers
    for handler in get_event_handlers(event_type):
        handler(event)
```

### Event Handlers

Custom event handlers can be registered:

```python
def register_event_handler(event_type: str, handler: callable):
    """Register a custom event handler."""
    _event_handlers[event_type].append(handler)

# Example: Monitor for limitations
def handle_limitation_flagged(event):
    """Send notification when limitation is flagged."""
    if event['data']['level'] >= 3:
        send_notification(
            f"High severity limitation flagged: {event['data']['limitation_type']}"
        )

register_event_handler('limitation.flagged', handle_limitation_flagged)
```

## State Management

### State Schema

```python
{
    'execution_id': str,
    'start_time': float,
    'language': str,
    'user_query': str,
    'current_step': int,
    'degradation_level': int,
    'steps_completed': List[int],
    'gate_results': Dict[str, bool],
    'limitation_flags': List[dict],
    'tokens_used': int,
    'sources_accessed': List[dict],
    'errors_encountered': List[dict]
}
```

### State Updates

State is updated atomically using the `update_state()` function:

```python
def update_state(updates: dict):
    """Update execution state atomically."""
    current_state = get_state()
    current_state.update(updates)
    set_state(current_state)
    emit_state_change(updates)
```

## Error Recovery

### Recovery Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `retry` | Retry operation with backoff | Transient failures |
| `fallback` | Use alternative source/method | Primary unavailable |
| `default` | Use default value | Non-critical data |
| `skip` | Continue without data | Optional data |
| `escalate` | Raise to user attention | Critical failure |

### Backoff Calculation

```python
def calculate_backoff(retry_count: int, strategy: str = 'exponential') -> float:
    """Calculate backoff time before retry."""
    if strategy == 'exponential':
        return min(2 ** retry_count, 60)  # Max 60 seconds
    elif strategy == 'linear':
        return min(retry_count * 5, 30)  # Max 30 seconds
    elif strategy == 'fixed':
        return 5  # Fixed 5 second delay
    else:
        return 1  # Default 1 second
```

## Configuration

Hooks behavior can be configured in `config/config.json`:

```json
{
  "hooks": {
    "enabled": true,
    "before_execution": {"enabled": true},
    "after_step": {"enabled": true, "validate_gates": true},
    "on_error": {"enabled": true, "max_retries": 3},
    "before_output": {"enabled": true, "validate_sections": true},
    "after_execution": {"enabled": true, "cleanup": true},
    "event_handlers": {
      "custom_handlers": [],
      "monitor_all_events": false,
      "monitored_events": ["error.occurred", "limitation.flagged"]
    }
  }
}
```

## Implementation

See `scripts/hooks.py` for the complete hooks implementation.

---

**Version**: 1.0.0
**Last Updated**: 2026-07-27
