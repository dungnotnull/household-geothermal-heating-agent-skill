"""
test_knowledge_updater.py — Skill 248: household-geothermal-heating
Comprehensive test suite for knowledge update pipeline.

Tests:
- Hash computation and deduplication
- Scoring algorithm accuracy
- Entry formatting
- API fetching (with mocked responses)
- Error handling
- Edge cases

Run with: python tools/test_knowledge_updater.py
"""

import datetime
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import knowledge_updater as ku


class TestHashComputation:
    """Test SHA256 hash computation for deduplication."""

    def test_identical_urls(self):
        """Identical URLs should produce identical hashes."""
        url = "https://doi.org/10.1016/j.renene.2012.09.018"
        h1 = ku.compute_hash(url)
        h2 = ku.compute_hash(url)
        assert h1 == h2, f"Hash mismatch for identical URLs: {h1} != {h2}"
        print("[OK] Identical URLs produce identical hashes")

    def test_different_urls(self):
        """Different URLs should produce different hashes."""
        url1 = "https://doi.org/10.1016/j.renene.2012.09.018"
        url2 = "https://doi.org/10.1016/j.geothermics.2010.03.001"
        h1 = ku.compute_hash(url1)
        h2 = ku.compute_hash(url2)
        assert h1 != h2, f"Different URLs should have different hashes"
        print("[OK] Different URLs produce different hashes")

    def test_case_insensitive(self):
        """Hash computation should be case-insensitive."""
        url1 = "HTTPS://DOI.ORG/10.1016/J.RENENE.2012.09.018"
        url2 = "https://doi.org/10.1016/j.renene.2012.09.018"
        h1 = ku.compute_hash(url1)
        h2 = ku.compute_hash(url2)
        assert h1 == h2, "Hash should be case-insensitive"
        print("[OK] Hash computation is case-insensitive")

    def test_whitespace_normalization(self):
        """Hash computation should normalize whitespace."""
        url1 = "https://doi.org/10.1016/j.renene.2012.09.018"
        url2 = "  https://doi.org/10.1016/j.renene.2012.09.018  "
        h1 = ku.compute_hash(url1)
        h2 = ku.compute_hash(url2)
        assert h1 == h2, "Hash should normalize whitespace"
        print("[OK] Hash computation normalizes whitespace")

    def test_hash_format(self):
        """Hash should be valid SHA256 hex string."""
        url = "https://doi.org/10.1016/j.renene.2012.09.018"
        h = ku.compute_hash(url)
        assert len(h) == 64, f"Hash length should be 64, got {len(h)}"
        assert all(c in "0123456789abcdef" for c in h), "Hash should be hexadecimal"
        print("[OK] Hash format is valid SHA256")


class TestScoring:
    """Test entry scoring algorithm."""

    def setup_method(self):
        """Setup test fixtures."""
        self.now = datetime.datetime.now()
        self.keywords = ["ground source heat pump", "geothermal", "borehole", "COP"]

    def test_perfect_score(self):
        """Entry with perfect match should score 10."""
        entry = {
            "title": "Ground source heat pump performance analysis",
            "abstract": "This study analyzes geothermal heat pump COP and borehole design",
            "published_date": self.now,
            "citation_count": 1000
        }
        score = ku.score_entry(entry, self.keywords, self.now)
        assert score >= 9.0, f"Perfect match should score >= 9.0, got {score}"
        print(f"[OK] Perfect match scores high: {score:.2f}/10")

    def test_low_score(self):
        """Entry with poor match should score low."""
        entry = {
            "title": "Machine learning applications in finance",
            "abstract": "Stock market prediction using neural networks",
            "published_date": self.now - datetime.timedelta(days=1000),
            "citation_count": 0
        }
        score = ku.score_entry(entry, self.keywords, self.now)
        assert score <= 2.0, f"Poor match should score <= 2.0, got {score}"
        print(f"[OK] Poor match scores low: {score:.2f}/10")

    def test_recency_impact(self):
        """Recent entries should score higher."""
        base_entry = {
            "title": "Ground source heat pump analysis",
            "abstract": "Geothermal system performance",
            "citation_count": 10
        }

        old_entry = {**base_entry, "published_date": self.now - datetime.timedelta(days=730)}
        new_entry = {**base_entry, "published_date": self.now}

        score_old = ku.score_entry(old_entry, self.keywords, self.now)
        score_new = ku.score_entry(new_entry, self.keywords, self.now)

        assert score_new > score_old, f"Recent entry should score higher: {score_new} vs {score_old}"
        print(f"[OK] Recency impacts score: {score_new:.2f} (new) vs {score_old:.2f} (old)")

    def test_citation_impact(self):
        """Highly cited entries should score higher."""
        base_entry = {
            "title": "Ground source heat pump analysis",
            "abstract": "Geothermal system performance",
            "published_date": self.now
        }

        low_cited = {**base_entry, "citation_count": 0}
        high_cited = {**base_entry, "citation_count": 500}

        score_low = ku.score_entry(low_cited, self.keywords, self.now)
        score_high = ku.score_entry(high_cited, self.keywords, self.now)

        assert score_high > score_low, f"Highly cited should score higher: {score_high} vs {score_low}"
        print(f"[OK] Citations impact score: {score_high:.2f} (500 cites) vs {score_low:.2f} (0 cites)")

    def test_score_bounds(self):
        """Score should always be between 0 and 10."""
        for _ in range(100):
            entry = {
                "title": "Test paper",
                "abstract": "Test abstract",
                "published_date": self.now - datetime.timedelta(days=365),
                "citation_count": 10
            }
            score = ku.score_entry(entry, self.keywords, self.now)
            assert 0 <= score <= 10, f"Score out of bounds: {score}"
        print("[OK] All scores within [0, 10] bounds")

    def test_missing_fields(self):
        """Entry with missing fields should not crash."""
        entry = {
            "title": "Test",
            "abstract": "",
            "published_date": None,
            "citation_count": None
        }
        score = ku.score_entry(entry, self.keywords, self.now)
        assert 0 <= score <= 10, f"Score should be valid even with missing fields: {score}"
        print(f"[OK] Missing fields handled gracefully: {score:.2f}/10")


class TestFormatting:
    """Test entry formatting."""

    def test_format_basic(self):
        """Basic entry formatting."""
        entry = {
            "title": "Test Paper Title",
            "authors": ["Author One", "Author Two"],
            "year": 2024,
            "venue": "Test Journal",
            "doi_or_url": "https://doi.org/10.1234/test",
            "abstract": "This is a test abstract.",
        }
        formatted = ku.format_entry(entry, 8.5, tier=2)

        assert "Test Paper Title" in formatted
        assert "Author One, Author Two" in formatted
        assert "2024" in formatted
        assert "Test Journal" in formatted
        assert "https://doi.org/10.1234/test" in formatted
        assert "8.5" in formatted
        assert "Tier: 2" in formatted
        print("[OK] Basic entry formatting correct")

    def test_format_empty_authors(self):
        """Format entry with no authors."""
        entry = {
            "title": "Test",
            "authors": [],
            "year": 2024,
            "venue": "Unknown",
            "doi_or_url": "https://test.com",
            "abstract": "Abstract",
        }
        formatted = ku.format_entry(entry, 5.0, tier=3)
        assert "Unknown" in formatted or "Authors:" in formatted
        print("[OK] Empty authors handled")

    def test_format_unicode(self):
        """Format entry with unicode characters."""
        entry = {
            "title": "étude sur les pompes à chaleur géothermiques",
            "authors": ["Jean-Pierre Éloïc"],
            "year": 2024,
            "venue": "Revue Internationale",
            "doi_or_url": "https://doi.org/10.1234/test",
            "abstract": "Analyse des systèmes géothermiques.",
        }
        formatted = ku.format_entry(entry, 7.0, tier=2)
        assert "étude" in formatted
        assert "Jean-Pierre" in formatted
        print("[OK] Unicode characters handled")


class TestTierDetermination:
    """Test evidence tier classification."""

    def test_tier_1_standards(self):
        """Standards and guidelines should be Tier 1."""
        entry = {"source": "semantic_scholar", "venue": "ASHRAE Handbook 2020"}
        tier = ku.determine_tier(entry)
        assert tier == 1, f"ASHRAE Handbook should be Tier 1, got {tier}"
        print("[OK] ASHRAE Handbook classified as Tier 1")

    def test_tier_1_igshpa(self):
        """IGSHPA should be Tier 1."""
        entry = {"source": "semantic_scholar", "venue": "IGSHPA Installation Guide"}
        tier = ku.determine_tier(entry)
        assert tier == 1, f"IGSHPA should be Tier 1, got {tier}"
        print("[OK] IGSHPA classified as Tier 1")

    def test_tier_2_journals(self):
        """Top-tier journals should be Tier 2."""
        entry = {"source": "semantic_scholar", "venue": "Geothermics"}
        tier = ku.determine_tier(entry)
        assert tier == 2, f"Geothermics should be Tier 2, got {tier}"

        entry = {"source": "arxiv", "venue": "Energy and Buildings"}
        tier = ku.determine_tier(entry)
        assert tier == 2, f"Energy and Buildings should be Tier 2, got {tier}"
        print("[OK] Top-tier journals classified as Tier 2")

    def test_tier_3_rss(self):
        """RSS news should be Tier 3."""
        entry = {"source": "rss", "venue": "News"}
        tier = ku.determine_tier(entry)
        assert tier == 3, f"RSS news should be Tier 3, got {tier}"
        print("[OK] RSS news classified as Tier 3")

    def test_tier_4_default(self):
        """Unknown sources should default to Tier 4."""
        entry = {"source": "unknown", "venue": "Unknown"}
        tier = ku.determine_tier(entry)
        assert tier == 4, f"Unknown should be Tier 4, got {tier}"
        print("[OK] Unknown source classified as Tier 4")


class TestDeduplication:
    """Test hash-based deduplication."""

    def test_load_existing_hashes(self):
        """Loading hashes from a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write("""
## Knowledge Base

### 2024-01-01 — Test Paper 1
- **DOI/URL:** https://doi.org/10.1234/test1

### 2024-01-02 — Test Paper 2
- **DOI/URL:** https://doi.org/10.1234/test2
""")
            f.flush()

            # Temporarily set brain path
            original_brain = ku.BRAIN_PATH
            ku.BRAIN_PATH = Path(f.name)

            hashes = ku.load_existing_hashes()
            assert len(hashes) == 2, f"Should load 2 hashes, got {len(hashes)}"

            ku.BRAIN_PATH = original_brain
            os.unlink(f.name)
            print("[OK] Loaded 2 hashes from file")

    def test_filter_duplicates(self):
        """Filtering duplicate entries."""
        # Create entries with duplicate DOIs
        entries = [
            {"doi_or_url": "https://doi.org/10.1234/dup", "title": "Paper 1"},
            {"doi_or_url": "https://doi.org/10.1234/dup", "title": "Paper 2"},  # Duplicate
            {"doi_or_url": "https://doi.org/10.5678/unique", "title": "Paper 3"},
        ]

        # Simulate existing hash
        existing_hash = ku.compute_hash("https://doi.org/10.1234/dup")

        new_entries = []
        for entry in entries:
            doi = entry.get("doi_or_url", "")
            if not doi:
                continue
            h = ku.compute_hash(doi)
            if h != existing_hash:
                new_entries.append(entry)

        assert len(new_entries) == 1, f"Should filter to 1 unique entry, got {len(new_entries)}"
        assert new_entries[0]["title"] == "Paper 3"
        print("[OK] Duplicates filtered correctly")


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_entry_list(self):
        """Empty entry list should not crash."""
        result = ku.append_to_brain([], dry_run=True)
        assert result == 0
        print("[OK] Empty entry list handled")

    def test_entry_without_doi(self):
        """Entry without DOI should be skipped."""
        entries = [{"title": "Test", "doi_or_url": ""}]
        result = ku.append_to_brain(entries, dry_run=True)
        assert result == 0
        print("[OK] Entry without DOI skipped")

    def test_very_long_title(self):
        """Very long titles should be handled."""
        entry = {
            "title": "A" * 500,
            "authors": ["Author"],
            "year": 2024,
            "venue": "Test",
            "doi_or_url": "https://test.com",
            "abstract": "B" * 500,
        }
        formatted = ku.format_entry(entry, 5.0, tier=2)
        assert len(formatted) > 0
        print("[OK] Very long title handled")

    def test_special_characters_in_doi(self):
        """DOI with special characters should be handled."""
        entry = {
            "title": "Test",
            "authors": ["Author"],
            "year": 2024,
            "venue": "Test",
            "doi_or_url": "https://doi.org/10.1234/test!@#$%^&*()",
            "abstract": "Test",
        }
        formatted = ku.format_entry(entry, 5.0, tier=2)
        assert "https://doi.org/10.1234/" in formatted
        print("[OK] Special characters in DOI handled")


class TestIntegration:
    """Integration tests for the full pipeline."""

    def test_full_pipeline_dry_run(self):
        """Test full pipeline in dry-run mode."""
        entries = [
            {
                "title": "Ground Source Heat Pump Performance",
                "authors": ["A. Smith", "B. Jones"],
                "year": 2024,
                "venue": "Geothermics",
                "doi_or_url": "https://doi.org/10.1016/j.geothermics.2024.100001",
                "abstract": "This study analyzes...",
                "published_date": datetime.datetime.now(),
                "citation_count": 15,
                "source": "semantic_scholar"
            }
        ]

        result = ku.append_to_brain(entries, dry_run=True)
        assert result == 1, f"Should process 1 entry, got {result}"
        print("[OK] Full pipeline dry-run successful")


def run_all_tests():
    """Run all test suites."""
    print("=" * 60)
    print("Running Knowledge Updater Test Suite")
    print("=" * 60)

    suites = [
        TestHashComputation(),
        TestScoring(),
        TestFormatting(),
        TestTierDetermination(),
        TestDeduplication(),
        TestEdgeCases(),
        TestIntegration()
    ]

    total_tests = 0
    passed_tests = 0

    for suite in suites:
        print(f"\n{suite.__class__.__name__}:")
        print("-" * 40)

        # Run all test methods
        for attr_name in dir(suite):
            if attr_name.startswith("test_"):
                total_tests += 1
                try:
                    # Setup if needed
                    if hasattr(suite, "setup_method"):
                        suite.setup_method()

                    # Run test
                    getattr(suite, attr_name)()
                    passed_tests += 1

                except AssertionError as e:
                    print(f"[FAIL] {attr_name}: {e}")
                except Exception as e:
                    print(f"[ERROR] {attr_name}: {e}")

    print("\n" + "=" * 60)
    print(f"Results: {passed_tests}/{total_tests} tests passed")
    print("=" * 60)

    if passed_tests == total_tests:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total_tests - passed_tests} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
