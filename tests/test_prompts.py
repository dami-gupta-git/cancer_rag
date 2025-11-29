import pytest
from cancerrag.prompts import PROMPT


def test_prompt_exists():
    """Test that the prompt template is properly defined."""
    assert PROMPT is not None
    assert isinstance(PROMPT, str)
    assert len(PROMPT) > 0


def test_prompt_has_placeholders():
    """Test that prompt has all required placeholders."""
    assert "{gene}" in PROMPT
    assert "{alteration}" in PROMPT
    assert "{tumor_type}" in PROMPT
    assert "{myvariant_summary}" in PROMPT


def test_prompt_formatting():
    """Test that prompt can be formatted with variables."""
    formatted = PROMPT.format(
        gene="BRAF",
        alteration="V600E",
        tumor_type="Melanoma",
        myvariant_summary="COSMIC ID: COSV57014428\ndbSNP ID: rs113488022"
    )

    assert "BRAF" in formatted
    assert "V600E" in formatted
    assert "Melanoma" in formatted
    assert "COSMIC ID: COSV57014428" in formatted
    assert "dbSNP ID: rs113488022" in formatted

    # Ensure placeholders were replaced
    assert "{gene}" not in formatted
    assert "{alteration}" not in formatted
    assert "{tumor_type}" not in formatted
    assert "{myvariant_summary}" not in formatted


def test_prompt_contains_instructions():
    """Test that prompt contains key instructions."""
    assert "expert cancer genomic pathologist" in PROMPT.lower()
    assert "JSON" in PROMPT
    assert "classification" in PROMPT.lower()
    assert "pathogenicity" in PROMPT.lower()


def test_prompt_output_schema():
    """Test that prompt defines expected output schema."""
    # Check for required output fields
    assert '"gene"' in PROMPT
    assert '"variant"' in PROMPT
    assert '"dbsnp_id"' in PROMPT
    assert '"cosmic_id"' in PROMPT
    assert '"classification"' in PROMPT
    assert '"pathogenicity"' in PROMPT
    assert '"recommended_therapies"' in PROMPT
    assert '"summary"' in PROMPT


def test_prompt_json_structure():
    """Test that prompt contains valid JSON structure template."""
    # Should contain double braces for literal braces in format string
    assert "{{" in PROMPT
    assert "}}" in PROMPT
