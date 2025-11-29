import pytest
from unittest.mock import AsyncMock, patch
from cancerrag.databases import get_myvariant


@pytest.mark.asyncio
async def test_get_myvariant_success():
    """Test successful MyVariant.info API call."""
    mock_response = {
        "hits": [
            {
                "dbsnp": {"rsid": "rs113488022"},
                "cosmic": {"cosmic_id": "COSV57014428"},
                "clinvar": {"clinical_significance": "Pathogenic"},
                "cadd": {"phred": 25.3},
                "dbnsfp": {
                    "sift": {"pred": "D"},
                    "polyphen2": {"hdiv_pred": "D"}
                }
            }
        ]
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_get = AsyncMock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        mock_client.return_value.__aenter__.return_value.get = mock_get

        result = await get_myvariant("BRAF", "V600E")

        assert result["gene"] == "BRAF"
        assert result["variant"] == "V600E"
        assert result["dbsnp_id"] == "rs113488022"
        assert result["cosmic_id"] == "COSV57014428"


@pytest.mark.asyncio
async def test_get_myvariant_no_results():
    """Test MyVariant.info API call with no results."""
    mock_response = {"hits": []}

    with patch("httpx.AsyncClient") as mock_client:
        mock_get = AsyncMock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        mock_client.return_value.__aenter__.return_value.get = mock_get

        result = await get_myvariant("INVALID", "X999X")

        assert result == {}


@pytest.mark.asyncio
async def test_get_myvariant_api_error():
    """Test MyVariant.info API call with error status code."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_get = AsyncMock()
        mock_get.return_value.status_code = 500
        mock_client.return_value.__aenter__.return_value.get = mock_get

        result = await get_myvariant("BRAF", "V600E")

        assert result == {}


@pytest.mark.asyncio
async def test_get_myvariant_network_error():
    """Test MyVariant.info API call with network error."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_get = AsyncMock(side_effect=Exception("Network error"))
        mock_client.return_value.__aenter__.return_value.get = mock_get

        result = await get_myvariant("BRAF", "V600E")

        assert result == {}
