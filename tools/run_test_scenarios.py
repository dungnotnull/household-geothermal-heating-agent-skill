"""
run_test_scenarios.py — Skill 248: household-geothermal-heating
Production-grade structural & content validator.

Verifies the 8-File Contract, sub-skill content, knowledge base,
test scenarios, and quality-gate coverage.

Exit code 0 = all checks pass, non-zero = failures.

Usage:
    python tools/run_test_scenarios.py --all
    python tools/run_test_scenarios.py --section files
    python tools/run_test_scenarios.py --section content --verbose
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Set, Tuple


# =============================================================================
# Configuration
# =============================================================================

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

# Quality gates definition
GATES = {
    "universal": {
        "U1": {"check": ">=3 sources cited, >=1 academic/authoritative", "fix": "Fetch from knowledge base"},
        "U2": {"check": "Disclosure/limitations before recommendation", "fix": "Prepend disclosure"},
        "U3": {"check": "Evidence hierarchy stated (Tier 1-4)", "fix": "Annotate tiers"},
        "U4": {"check": "Language matches user preference", "fix": "Translate output"},
        "U5": {"check": "Output uses template (all sections)", "fix": "Reformat to template"},
        "U6": {"check": "Every claim traceable or flagged", "fix": "Mark unsupported claims"}
    },
    "domain": {
        "G1": {"check": "Requirements complete", "fix": "Ask clarifying questions"},
        "G2": {"check": "Evidence collected", "fix": "Fetch authoritative sources"},
        "G3": {"check": "Heating/cooling load computed", "fix": "Compute load"},
        "G4": {"check": "Ground loop sized to load", "fix": "Size ground loop"},
        "G5": {"check": "COP/SPF & economics quantified", "fix": "Quantify efficiency"},
        "G6": {"check": "Operation/maintenance planned", "fix": "Plan O&M"}
    }
}

# Verdict categories for geothermal domain
VERDICTS = [
    "Optimal & Economical",
    "Conditional (loop space)",
    "Low Efficiency",
    "Inconclusive"
]

# Required sub-skills
REQUIRED_SUBSKILLS = {
    "sub-gather-requirements",
    "sub-evidence-collector",
    "sub-core-analysis",
    "sub-knowledge-updater",
    "sub-advisor"
}

# Required files (8-File Contract)
REQUIRED_FILES = [
    "CLAUDE.md",
    "PROJECT-detail.md",
    "PROJECT-DEVELOPMENT-PHASE-TRACKING.md",
    "README.md",
    "SECOND-KNOWLEDGE-BRAIN.md",
    "skills/main.md",
    "tools/knowledge_updater.py",
    "tools/test_knowledge_updater.py",
    "tools/run_test_scenarios.py",
    "tests/test-scenarios.md",
    "tests/TEST_RESULTS.md"
]


# =============================================================================
# Test Infrastructure
# =============================================================================

class TestRunner:
    """Test runner with check tracking."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.checks_passed = 0
        self.checks_failed = 0
        self.failures: List[str] = []

    def ok(self, label: str, detail: str = ""):
        """Record a passed check."""
        self.checks_passed += 1
        if self.verbose or detail:
            msg = f"[PASS] {label}"
            if detail:
                msg += f": {detail}"
            print(f"  {msg}")

    def fail(self, label: str, detail: str = ""):
        """Record a failed check."""
        self.checks_failed += 1
        self.failures.append(f"{label}: {detail}")
        msg = f"[FAIL] {label}"
        if detail:
            msg += f": {detail}"
        print(f"  {msg}")

    def require(self, condition: bool, label: str, detail: str = ""):
        """Require a condition; record as pass or fail."""
        if condition:
            self.ok(label, detail)
        else:
            self.fail(label, detail)

    def summary(self) -> int:
        """Print summary and return exit code."""
        total = self.checks_passed + self.checks_failed
        print(f"\n{'=' * 60}")
        print(f"Results: {self.checks_passed}/{total} checks passed")
        print(f"{'=' * 60}")

        if self.failures:
            print("\nFailures:")
            for f in self.failures:
                print(f"  - {f}")

        return 0 if self.checks_failed == 0 else 1


def read_file(path: Path) -> str:
    """Read file content safely."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return ""


# =============================================================================
# File Structure Tests
# =============================================================================

def test_file_structure(runner: TestRunner):
    """Test 8-File Contract and directory structure."""
    print("\n[1] File Structure Tests")
    print("-" * 60)

    # Check required files
    for f in REQUIRED_FILES:
        path = ROOT / f
        runner.require(
            path.exists(),
            f"file present: {f}",
            f"missing at {path}"
        )

    # Check sub-skills directory
    runner.require(
        SKILLS.exists(),
        "skills directory exists"
    )

    # Check for required sub-skills
    sub_files = list(SKILLS.glob("sub-*.md"))
    sub_names = {f.stem for f in sub_files}

    runner.require(
        len(sub_files) >= 5,
        f"at least 5 sub-skills",
        f"found {len(sub_files)}"
    )

    runner.require(
        REQUIRED_SUBSKILLS.issubset(sub_names),
        "all required sub-skills present",
        f"missing {REQUIRED_SUBSKILLS - sub_names}"
    )

    # Check tools directory
    tools_dir = ROOT / "tools"
    runner.require(tools_dir.exists(), "tools directory exists")

    # Check tests directory
    tests_dir = ROOT / "tests"
    runner.require(tests_dir.exists(), "tests directory exists")


# =============================================================================
# Frontmatter and Content Tests
# =============================================================================

def test_skill_frontmatter(runner: TestRunner):
    """Test skill files have proper frontmatter and sections."""
    print("\n[2] Skill Frontmatter & Content Tests")
    print("-" * 60)

    fm_pattern = re.compile(r"^---\s*\n(.*?\n)---", re.S)
    required_sections = {
        "sub-*.md": ["Role & Persona", "Workflow", "Output Format", "Quality Gates"],
        "main.md": ["Role & Persona", "Quality Gates", "Graceful Degradation"]
    }

    # Test sub-skills
    sub_skills = list(SKILLS.glob("sub-*.md"))
    for skill_file in sub_skills:
        content = read_file(skill_file)

        # Check frontmatter
        runner.require(
            bool(fm_pattern.search(content)),
            f"{skill_file.name}: frontmatter present"
        )

        # Check frontmatter content
        fm_match = fm_pattern.search(content)
        if fm_match:
            fm_content = fm_match.group(1)
            runner.require(
                "name:" in fm_content and "description:" in fm_content,
                f"{skill_file.name}: name+description in frontmatter"
            )

        # Check required sections
        for section in required_sections["sub-*.md"]:
            runner.require(
                section in content,
                f"{skill_file.name}: has '{section}' section"
            )

    # Test main.md
    main_file = SKILLS / "main.md"
    if main_file.exists():
        content = read_file(main_file)

        for section in required_sections["main.md"]:
            runner.require(
                section in content,
                f"main.md: has '{section}' section"
            )

        runner.require(
            "Harness Execution Protocol" in content or "Workflow" in content,
            "main.md: has harness workflow"
        )

        runner.require(
            "Pre-Flight" in content,
            "main.md: has pre-flight language detection"
        )

        runner.require(
            "limitation" in content.lower(),
            "main.md: mentions limitation banner"
        )


# =============================================================================
# Quality Gate Coverage Tests
# =============================================================================

def test_quality_gates(runner: TestRunner):
    """Test quality gates are documented and consistent."""
    print("\n[3] Quality Gate Tests")
    print("-" * 60)

    main_content = read_file(SKILLS / "main.md")
    advisor_content = read_file(SKILLS / "sub-advisor.md")

    # Check universal gates
    for gate_id in GATES["universal"].keys():
        runner.require(
            gate_id in main_content,
            f"main.md: mentions universal gate {gate_id}"
        )

    # Check domain gates
    for gate_id in GATES["domain"].keys():
        runner.require(
            gate_id in main_content,
            f"main.md: mentions domain gate {gate_id}"
        )

    # Check verdict categories
    for verdict in VERDICTS:
        runner.require(
            verdict in advisor_content or verdict in main_content,
            f"verdict '{verdict}' documented"
        )


# =============================================================================
# Knowledge Base Tests
# =============================================================================

def test_knowledge_base(runner: TestRunner):
    """Test SECOND-KNOWLEDGE-BRAIN.md structure and content."""
    print("\n[4] Knowledge Base Tests")
    print("-" * 60)

    brain_path = ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
    brain_content = read_file(brain_path)

    # Check evidence hierarchy
    runner.require(
        "Tier 1" in brain_content and "Tier 4" in brain_content,
        "brain: evidence hierarchy tiers defined"
    )

    # Check for DOIs
    doi_pattern = re.compile(r"10\.\d{4,9}/[^\s|]+")
    dois = doi_pattern.findall(brain_content)
    runner.require(
        len(dois) >= 2,
        f"brain: has >=2 DOI references",
        f"found {len(dois)}"
    )

    # Check for research table
    table_rows = len(re.findall(r"\|\s*\d{4}\s*\|", brain_content))
    runner.require(
        table_rows >= 3 or "### 2." in brain_content,
        "brain: key papers table present"
    )

    # Check for core methods section
    runner.require(
        "## 1. Core" in brain_content or "### 1.1" in brain_content,
        "brain: core methods section present"
    )

    # Check for data sources section
    runner.require(
        "## 4. Authoritative Data Sources" in brain_content,
        "brain: data sources section present"
    )

    # Check for self-update protocol
    runner.require(
        "## 6. Self-Update Protocol" in brain_content,
        "brain: self-update protocol present"
    )

    # Check for update log section
    runner.require(
        "## 7. Knowledge Update Log" in brain_content,
        "brain: update log section present"
    )


# =============================================================================
# Test Scenarios Tests
# =============================================================================

def test_test_scenarios(runner: TestRunner):
    """Test test-scenarios.md coverage."""
    print("\n[5] Test Scenarios Tests")
    print("-" * 60)

    scenarios_path = ROOT / "tests" / "test-scenarios.md"
    scenarios_content = read_file(scenarios_path)

    # Count scenarios
    scenario_count = scenarios_content.count("## Scenario")
    runner.require(
        scenario_count >= 5,
        f"scenarios: >=5 defined",
        f"found {scenario_count}"
    )

    # Check for degraded mode scenario
    runner.require(
        "degraded" in scenarios_content.lower() or "missing" in scenarios_content.lower(),
        "scenarios: degraded/missing case covered"
    )

    # Check for comparison/conflict scenario
    runner.require(
        "conflict" in scenarios_content.lower() or "compare" in scenarios_content.lower(),
        "scenarios: comparison/conflict case covered"
    )

    # Check gate coverage
    for gate_id in ["G1", "G2", "G3"]:
        runner.require(
            gate_id in scenarios_content,
            f"scenarios: gate {gate_id} referenced"
        )


# =============================================================================
# Knowledge Updater Tests
# =============================================================================

def test_knowledge_updater(runner: TestRunner):
    """Test knowledge_updater.py structure."""
    print("\n[6] Knowledge Updater Tests")
    print("-" * 60)

    ku_path = ROOT / "tools" / "knowledge_updater.py"
    ku_content = read_file(ku_path)

    # Check for KNOWLEDGE_CONFIG
    runner.require(
        "KNOWLEDGE_CONFIG" in ku_content,
        "knowledge_updater: KNOWLEDGE_CONFIG present"
    )

    # Check for deduplication
    runner.require(
        "sha256" in ku_content.lower() or "compute_hash" in ku_content,
        "knowledge_updater: hash deduplication implemented"
    )

    # Check for scoring
    runner.require(
        "score_entry" in ku_content,
        "knowledge_updater: scoring function present"
    )

    # Check for dry-run
    runner.require(
        "--dry-run" in ku_content,
        "knowledge_updater: dry-run flag present"
    )

    # Check for main execution
    runner.require(
        "def main" in ku_content,
        "knowledge_updater: main function defined"
    )


# =============================================================================
# PDPT and Documentation Tests
# =============================================================================

def test_documentation(runner: TestRunner):
    """Test PROJECT-DEVELOPMENT-PHASE-TRACKING.md and README.md."""
    print("\n[7] Documentation Tests")
    print("-" * 60)

    # PDPT
    pdpt_path = ROOT / "PROJECT-DEVELOPMENT-PHASE-TRACKING.md"
    pdpt_content = read_file(pdpt_path)

    runner.require(
        "100%" in pdpt_content,
        "PDPT: 100% completion markers present"
    )

    runner.require(
        "Phase 5" in pdpt_content,
        "PDPT: Phase 5 mentioned"
    )

    # README
    readme_path = ROOT / "README.md"
    readme_content = read_file(readme_path)

    runner.require(
        "Usage" in readme_content or "##" in readme_content,
        "README: usage section present"
    )

    # PROJECT-detail
    pd_path = ROOT / "PROJECT-detail.md"
    pd_content = read_file(pd_path)

    runner.require(
        "Idea (Vietnamese)" in pd_content,
        "PROJECT-detail: original idea preserved"
    )

    runner.require(
        "Harness Architecture" in pd_content,
        "PROJECT-detail: harness architecture diagram present"
    )


# =============================================================================
# Content Quality Tests
# =============================================================================

def test_content_quality(runner: TestRunner):
    """Test content quality and production-readiness."""
    print("\n[8] Content Quality Tests")
    print("-" * 60)

    # Check for placeholder content
    brain_path = ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
    brain_content = read_file(brain_path)

    # Flag suspicious placeholder content
    suspicious_patterns = [
        "gamification",  # Wrong for this domain
        "INSERT HERE",
        "TODO",
        "PLACEHOLDER",
        "FIXME"
    ]

    for pattern in suspicious_patterns:
        if pattern.lower() in brain_content.lower():
            runner.fail(
                f"content quality",
                f"suspicious placeholder '{pattern}' found in knowledge base"
            )

    # Check for real geothermal content
    geothermal_keywords = [
        "heat pump",
        "ground loop",
        "borehole",
        "COP",
        "thermal conductivity",
        "IGSHPA",
        "ASHRAE"
    ]

    keyword_count = sum(1 for kw in geothermal_keywords if kw.lower() in brain_content.lower())
    runner.require(
        keyword_count >= 4,
        "content quality: domain-relevant content present",
        f"found {keyword_count}/{len(geothermal_keywords)} keywords"
    )


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate household-geothermal-heating project structure and content"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all test sections"
    )
    parser.add_argument(
        "--section", "-s",
        choices=["files", "content", "gates", "knowledge", "scenarios", "updater", "docs", "quality"],
        help="Run specific test section"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output (show all checks)"
    )

    args = parser.parse_args()

    # Create test runner
    runner = TestRunner(verbose=args.verbose)

    print("=" * 60)
    print("Household Geothermal Heating - Project Validator")
    print("=" * 60)

    # Run tests
    if args.all or args.section == "files":
        test_file_structure(runner)

    if args.all or args.section == "content":
        test_skill_frontmatter(runner)

    if args.all or args.section == "gates":
        test_quality_gates(runner)

    if args.all or args.section == "knowledge":
        test_knowledge_base(runner)

    if args.all or args.section == "scenarios":
        test_test_scenarios(runner)

    if args.all or args.section == "updater":
        test_knowledge_updater(runner)

    if args.all or args.section == "docs":
        test_documentation(runner)

    if args.all or args.section == "quality":
        test_content_quality(runner)

    # If no section specified, run all
    if not args.section and not args.all:
        print("No section specified. Running all tests...")
        test_file_structure(runner)
        test_skill_frontmatter(runner)
        test_quality_gates(runner)
        test_knowledge_base(runner)
        test_test_scenarios(runner)
        test_knowledge_updater(runner)
        test_documentation(runner)
        test_content_quality(runner)

    # Return exit code
    return runner.summary()


if __name__ == "__main__":
    sys.exit(main())
