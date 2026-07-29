---
name: household-geothermal-heating
description: Household Geothermal Heating System Design & Operation — Small-Scale Geothermal Heat Pump Engineering evidence-backed analysis harness. Use for geothermal system design, heat pump sizing, ground loop design, COP/economics analysis, and O&M planning. Triggers on: geothermal design, heat pump sizing, ground loop, GSHP, borehole design, heating system economics, geothermal operation & maintenance.
version: 1.0.0
author: 972026 Skill Library
license: MIT
compatibility:
  required_tools:
    - WebSearch
    - WebFetch
    - Read
    - Write
    - Bash
    - Skill
  python_version: ">=3.8"
  claude_code_version: ">=1.0"
---

# SKILL.md — Skill Registry & System Documentation

## Overview

`household-geothermal-heating` is a production-grade harness skill for **Small-Scale Geothermal Heat Pump Engineering**. It transforms Claude into a domain-expert that delivers structured, evidence-backed outputs through an orchestrated 6-step workflow.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT (/skill-name invoke)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              PRE-FLIGHT: Language Detection & Routing            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Language Detection (Vietnamese/English/Other)              │  │
│  │  Skill Router (determine execution path)                   │  │
│  │  Context Window Manager (optimize token usage)            │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MAIN HARNESS (6-Step Workflow)                │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Step 1: sub-gather-requirements                            │  │
│  │ Step 2: sub-evidence-collector                             │  │
│  │ Step 3: sub-core-analysis                                  │  │
│  │ Step 4: sub-knowledge-updater                              │  │
│  │ Step 5: sub-advisor                                        │  │
│  │ Step 6: Quality Gate Review (U1-U6, G1-G6)                 │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 OUTPUT GENERATION & DELIVERY                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Structured Report (all mandatory sections)                │  │
│  │  Evidence Chain (citations with tiers)                     │  │
│  │  Risk/Limitation Disclosure                                │  │
│  │  Post-Execution Gate Checklist                             │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Skill Registration & Resolution

### Registration Schema

```json
{
  "skill_id": "household-geothermal-heating",
  "version": "1.0.0",
  "name": "household-geothermal-heating",
  "type": "harness",
  "domain": "Small-Scale Geothermal Heat Pump Engineering",
  "entry_point": "skills/main.md",
  "sub_skills": [
    "sub-gather-requirements",
    "sub-evidence-collector",
    "sub-core-analysis",
    "sub-knowledge-updater",
    "sub-advisor"
  ],
  "tools": ["WebSearch", "WebFetch", "Read", "Write", "Bash", "Skill"],
  "quality_gates": {
    "universal": ["U1", "U2", "U3", "U4", "U5", "U6"],
    "domain": ["G1", "G2", "G3", "G4", "G5", "G6"]
  },
  "supported_languages": ["en", "vi"],
  "triggers": [
    "geothermal design",
    "heat pump sizing",
    "ground loop",
    "GSHP",
    "borehole design",
    "heating system economics",
    "geothermal O&M"
  ]
}
```

### Resolution Process

1. **Trigger Detection**: Skill is invoked via `/household-geothermal-heating` or trigger phrases
2. **Capability Check**: Verify required tools are available
3. **Language Detection**: Determine output language (English/Vietnamese)
4. **Context Loading**: Load SKILL.md body and sub-skill files
5. **Execution**: Begin Step 1 of harness workflow

### Input/Output JSON Schemas

#### Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Household Geothermal Heating Skill Input",
  "required": ["user_query"],
  "properties": {
    "user_query": {
      "type": "string",
      "description": "Natural language query from user"
    },
    "language": {
      "type": "string",
      "enum": ["en", "vi", "auto"],
      "default": "auto",
      "description": "Output language (auto-detect if not specified)"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["standard", "comparison", "risk_assessment", "minimal"],
      "default": "standard"
    },
    "context": {
      "type": "object",
      "properties": {
        "building_params": {
          "type": "object",
          "properties": {
            "floor_area": {"type": "number"},
            "insulation_level": {"type": "string"},
            "ceiling_height": {"type": "number"},
            "window_area_pct": {"type": "number"}
          }
        },
        "location": {
          "type": "string",
          "description": "City, region, or climate zone"
        },
        "climate_data": {
          "type": "object",
          "properties": {
            "design_temp": {"type": "number"},
            "hdd": {"type": "number"},
            "ground_temp": {"type": "number"}
          }
        },
        "economics": {
          "type": "object",
          "properties": {
            "electricity_cost": {"type": "number"},
            "alternative_fuel": {"type": "string"},
            "alternative_cost": {"type": "number"}
          }
        }
      }
    }
  }
}
```

#### Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Household Geothermal Heating Skill Output",
  "required": [
    "report_metadata",
    "executive_summary",
    "inputs_scope",
    "evidence_collected",
    "analysis_scorecard",
    "action_plan",
    "academic_evidence",
    "disclosure",
    "verdict",
    "gate_checklist"
  ],
  "properties": {
    "report_metadata": {
      "type": "object",
      "properties": {
        "date": {"type": "string", "format": "date"},
        "analyst": {"type": "string"},
        "language": {"type": "string"},
        "domain": {"type": "string"},
        "version": {"type": "string"}
      }
    },
    "executive_summary": {
      "type": "string",
      "description": "2-3 sentence summary of verdict and headline action"
    },
    "inputs_scope": {
      "type": "object",
      "properties": {
        "object_of_analysis": {"type": "string"},
        "constraints": {"type": "array"},
        "timeframe": {"type": "string"},
        "available_inputs": {"type": "object"}
      }
    },
    "evidence_collected": {
      "type": "object",
      "properties": {
        "current_data": {"type": "object"},
        "authoritative_docs": {"type": "array"},
        "recent_developments": {"type": "array"},
        "reference_benchmarks": {"type": "array"}
      }
    },
    "analysis_scorecard": {
      "type": "object",
      "properties": {
        "building_load": {"type": "object"},
        "heat_pump_spec": {"type": "object"},
        "ground_loop_design": {"type": "object"},
        "cop_economics": {"type": "object"},
        "operation_maintenance": {"type": "object"}
      }
    },
    "action_plan": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "action": {"type": "string"},
          "priority": {"type": "string"},
          "magnitude": {"type": "string"},
          "safety_limits": {"type": "array"}
        }
      }
    },
    "academic_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "authors": {"type": "string"},
          "year": {"type": "integer"},
          "title": {"type": "string"},
          "venue": {"type": "string"},
          "doi": {"type": "string"},
          "tier": {"type": "integer", "minimum": 1, "maximum": 4},
          "key_finding": {"type": "string"}
        }
      }
    },
    "disclosure": {
      "type": "string",
      "description": "Mandatory risk/limitation disclosure"
    },
    "verdict": {
      "type": "object",
      "properties": {
        "category": {
          "type": "string",
          "enum": [
            "Optimal & Economical",
            "Conditional (loop space)",
            "Low Efficiency",
            "Inconclusive"
          ]
        },
        "scenarios": {"type": "object"},
        "key_risks": {"type": "array"},
        "evidence_chain": {"type": "array"},
        "remediation": {"type": "string"}
      }
    },
    "gate_checklist": {
      "type": "object",
      "properties": {
        "universal_gates": {"type": "object"},
        "domain_gates": {"type": "object"},
        "limitations": {"type": "array"}
      }
    }
  }
}
```

## Validation & Enforcement

### Quality Gate Validation

Each quality gate implements the following validation logic:

1. **Gate Check**: Verify condition is met
2. **Auto-Fix**: Attempt automatic remediation if condition not met
3. **Retry**: Allow up to 2 retry attempts
4. **Limitation Flag**: Emit explicit limitation if gate cannot pass
5. **Continue**: Proceed to next gate (system continues even if some gates fail with limitations)

### Error Handling Matrix

| Error Type | Severity | Detection | Recovery | Max Retries |
|------------|----------|-----------|----------|-------------|
| Source timeout | Warning | No response 30s | Alternate source | 3 |
| Invalid input | Error | Schema mismatch | User confirmation | 2 |
| Missing input | Warning | Field absent | Default + flag | N/A |
| Stale reading | Warning | Timestamp old | Refresh request | 1 |
| Knowledge base miss | Warning | No matches | WebSearch gap-fill | 2 |
| Conflicting actions | Error | Mutually exclusive | Precedence rules | N/A |
| Envelope unavailable | Warning | No setpoint | Genus fallback | 1 |
| Object/class ambiguous | Warning | Unclear classification | User confirm | 2 |

### Graceful Degradation Levels

| Level | Condition | Behavior | Output |
|-------|-----------|----------|--------|
| 0 | All sources reachable | Full analysis | Complete report |
| 1 | Some sources fail | Secondary sources + flags | Report with substituted sources |
| 2 | Most sources fail | Knowledge base only | Historical context notice |
| 3 | Required input missing | Available variables only | DATA UNAVAILABLE flags |
| 4 | All sources fail | No output | DATA UNAVAILABLE notice |

## Sub-Skill Registry

### Sub-Skill Manifest

```json
{
  "sub_skills": [
    {
      "name": "sub-gather-requirements",
      "step": 1,
      "file": "skills/sub-gather-requirements.md",
      "purpose": "Clarify object, scope, constraints, timeframe, inputs, audience, language",
      "inputs": ["user_query", "language"],
      "outputs": ["requirements_object"],
      "gate": "G1",
      "tools": ["conversation only"]
    },
    {
      "name": "sub-evidence-collector",
      "step": 2,
      "file": "skills/sub-evidence-collector.md",
      "purpose": "Fetch real-time and reference data from authoritative sources",
      "inputs": ["requirements_object"],
      "outputs": ["evidence_bundle"],
      "gate": "G2",
      "tools": ["WebSearch", "WebFetch", "Read"]
    },
    {
      "name": "sub-core-analysis",
      "step": 3,
      "file": "skills/sub-core-analysis.md",
      "purpose": "Design system: load calculation, heat pump sizing, loop design, COP/economics",
      "inputs": ["evidence_bundle", "requirements_object"],
      "outputs": ["analysis_scorecard"],
      "gates": ["G3", "G4"],
      "tools": ["Read", "WebFetch", "Arithmetic"]
    },
    {
      "name": "sub-knowledge-updater",
      "step": 4,
      "file": "skills/sub-knowledge-updater.md",
      "purpose": "Query knowledge base for academic evidence with tier labels",
      "inputs": ["topic_keywords"],
      "outputs": ["citations_with_tiers", "gaps"],
      "gate": "G5",
      "tools": ["Read", "WebSearch"]
    },
    {
      "name": "sub-advisor",
      "step": 5,
      "file": "skills/sub-advisor.md",
      "purpose": "Synthesize analysis into risk-disclosed conclusion with evidence chain",
      "inputs": ["analysis_scorecard", "evidence_bundle", "citations"],
      "outputs": ["verdict", "scenarios", "risks", "actions", "disclosure"],
      "gate": "G6",
      "tools": ["Reasoning", "Skill"]
    }
  ]
}
```

## Context Window Management

### Token Optimization Strategy

1. **Progressive Disclosure**: Load only metadata initially (~100 tokens)
2. **Just-In-Time Loading**: Load skill body when triggered (<500 lines)
3. **Resource Management**: Load reference files only when needed
4. **Compression**: Use concise language and structured formats
5. **Caching**: Cache frequently accessed resources

### Estimated Token Usage

| Component | Tokens | When Loaded |
|-----------|--------|-------------|
| SKILL.md metadata | ~100 | Always |
| SKILL.md body | ~1,500 | On trigger |
| Sub-skill file | ~800-1,200 | When invoked |
| Reference file | ~500-2,000 | As needed |
| SECOND-KNOWLEDGE-BRAIN.md | ~3,000 | When queried |
| **Total (typical run)** | ~6,000-8,000 | Full execution |

## Hooks System

### Lifecycle Hooks

```python
{
  "before_execution": {
    "purpose": "Initialize context, validate inputs, set up logging",
    "handler": "hooks/before_execution.py",
    "parameters": ["user_query", "context"]
  },
  "after_step": {
    "purpose": "Validate step output, update state, check gates",
    "handler": "hooks/after_step.py",
    "parameters": ["step_number", "step_output", "requirements"]
  },
  "on_error": {
    "purpose": "Handle errors, log failures, trigger recovery",
    "handler": "hooks/on_error.py",
    "parameters": ["error", "context", "retry_count"]
  },
  "before_output": {
    "purpose": "Final validation, format output, apply templates",
    "handler": "hooks/before_output.py",
    "parameters": ["analysis_result", "language"]
  },
  "after_execution": {
    "purpose": "Log completion, update metrics, cleanup",
    "handler": "hooks/after_execution.py",
    "parameters": ["result", "duration", "tokens_used"]
  }
}
```

### Event Emission

The system emits events for state synchronization and monitoring:

```python
EVENT_TYPES = {
    "skill.invoked": "Skill triggered by user",
    "step.started": "Sub-skill execution started",
    "step.completed": "Sub-skill execution completed",
    "gate.passed": "Quality gate passed",
    "gate.failed": "Quality gate failed (auto-fix triggered)",
    "data.fetch": "Data fetch from external source",
    "error.occurred": "Error during execution",
    "limitation.flagged": "Limitation detected and flagged",
    "output.generated": "Final report generated"
}
```

## Tools System

### Tool Definitions

Each tool implements the following schema:

```json
{
  "tool_name": {
    "purpose": "Brief description of tool purpose",
    "input_schema": {
      "type": "object",
      "properties": {},
      "required": []
    },
    "output_schema": {
      "type": "object",
      "properties": {}
    },
    "error_handling": {
      "timeout": 30,
      "retry_strategy": "exponential_backoff",
      "fallback": "alternative_tool_or_default"
    },
    "rate_limits": {
      "max_calls_per_minute": 10,
      "max_concurrent": 3
    }
  }
}
```

### Tool Execution Handlers

Tools are executed through a centralized handler that:
1. Validates input against schema
2. Checks rate limits
3. Executes with timeout
4. Handles errors with retry logic
5. Returns validated output

## Configuration Management

### Configuration Schema

See `config/config.json` for complete configuration structure.

Key configuration sections:
- **system**: Core system settings
- **tools**: Tool configurations and rate limits
- **quality_gates**: Gate parameters and thresholds
- **logging**: Log levels and formatters
- **features**: Feature flags for experimental functionality

## Logging & Monitoring

### Log Levels

- **CRITICAL**: System failure, cannot proceed
- **ERROR**: Error with recovery, limitation flagged
- **WARNING**: Degraded mode, fallback activated
- **INFO**: Normal execution milestones
- **DEBUG**: Detailed execution trace

### Structured Logging

All logs include:
- Timestamp (ISO 8601)
- Level
- Component (skill/sub-skill)
- Event type
- Context (relevant variables)
- Error details (if applicable)

## Performance Metrics

### Key Performance Indicators

- **Execution Time**: Target < 60 seconds for standard analysis
- **Token Efficiency**: Target < 10,000 tokens per run
- **Gate Pass Rate**: Target > 95% gates passing
- **Source Success Rate**: Target > 80% primary sources reachable
- **User Satisfaction**: Measured via feedback

## Deployment

### Installation

1. Copy skill directory to Claude Code skills folder
2. Verify required tools are available
3. Test with sample query
4. Configure environment variables (optional)

### Dependencies

See `requirements.txt` for Python dependencies.

### Version Compatibility

- Claude Code: >= 1.0
- Python: >= 3.8
- Claude Model: Opus 4.7 (recommended), Sonnet 4.6 (compatible)

---

## Appendix A: Language Translation Table

See `skills/main.md` for complete English/Vietnamese translation table.

## Appendix B: Quality Gate Reference

See `skills/main.md` for complete gate definitions and auto-fix logic.

## Appendix C: Error Recovery Procedures

See `skills/main.md` for graceful degradation and error handling tables.

## Appendix D: Knowledge Base Schema

See `SECOND-KNOWLEDGE-BRAIN.md` for knowledge base structure and update protocol.

---

**Document Version**: 1.0.0
**Last Updated**: 2026-07-27
**Maintainer**: 972026 Skill Library
