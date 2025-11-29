import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from cancerrag.annotator import annotate


@pytest.mark.asyncio
async def test_annotate_success():
    """Test successful variant annotation."""
    mock_variant_data = {
        "gene": "BRAF",
        "variant": "V600E",
        "dbsnp_id": "rs113488022",
        "cosmic_id": "COSV57014428",
        "clinvar": {"clinical_significance": "Pathogenic"},
        "cadd_score": 25.3
    }

    expected_result = {
        "gene": "BRAF",
        "variant": "V600E",
        "dbsnp_id": "rs113488022",
        "cosmic_id": "COSV57014428",
        "classification": "Oncogenic",
        "pathogenicity": "Pathogenic",
        "recommended_therapies": ["Vemurafenib", "Dabrafenib"],
        "summary": "BRAF V600E is a pathogenic oncogenic mutation."
    }

    with patch("cancerrag.annotator.get_myvariant", new_callable=AsyncMock) as mock_get_variant, \
         patch("cancerrag.annotator.client") as mock_client:

        mock_get_variant.return_value = mock_variant_data

        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(expected_result)

        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await annotate("BRAF", "V600E", "Melanoma")

        assert result["gene"] == "BRAF"
        assert result["variant"] == "V600E"
        assert result["classification"] == "Oncogenic"
        assert "therapies" in result or "recommended_therapies" in result


@pytest.mark.asyncio
async def test_annotate_no_variant_data():
    """Test annotation when MyVariant.info returns no data."""
    expected_result = {
        "gene": "UNKNOWN",
        "variant": "X999X",
        "classification": "VUS",
        "summary": "No variant data available."
    }

    with patch("cancerrag.annotator.get_myvariant", new_callable=AsyncMock) as mock_get_variant, \
         patch("cancerrag.annotator.client") as mock_client:

        mock_get_variant.return_value = {}

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(expected_result)

        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await annotate("UNKNOWN", "X999X")

        assert result["gene"] == "UNKNOWN"
        assert result["variant"] == "X999X"


@pytest.mark.asyncio
async def test_annotate_invalid_json():
    """Test annotation when LLM returns invalid JSON."""
    mock_variant_data = {
        "gene": "EGFR",
        "variant": "L858R",
        "cosmic_id": "COSM6224"
    }

    with patch("cancerrag.annotator.get_myvariant", new_callable=AsyncMock) as mock_get_variant, \
         patch("cancerrag.annotator.client") as mock_client:

        mock_get_variant.return_value = mock_variant_data

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is not JSON"

        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await annotate("EGFR", "L858R")

        assert "error" in result
        assert result["error"] == "LLM returned invalid JSON"
        assert "raw_output" in result


@pytest.mark.asyncio
async def test_annotate_with_tumor_type():
    """Test annotation with specific tumor type."""
    mock_variant_data = {
        "gene": "EGFR",
        "variant": "L858R",
        "cosmic_id": "COSM6224"
    }

    expected_result = {
        "gene": "EGFR",
        "variant": "L858R",
        "classification": "Oncogenic",
        "summary": "EGFR L858R in lung adenocarcinoma."
    }

    with patch("cancerrag.annotator.get_myvariant", new_callable=AsyncMock) as mock_get_variant, \
         patch("cancerrag.annotator.client") as mock_client:

        mock_get_variant.return_value = mock_variant_data

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(expected_result)

        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await annotate("EGFR", "L858R", "Lung Adenocarcinoma")

        # Verify the OpenAI client was called with correct parameters
        call_args = mock_client.chat.completions.create.call_args
        assert call_args is not None
        messages = call_args.kwargs["messages"]
        assert "Lung Adenocarcinoma" in messages[0]["content"]
