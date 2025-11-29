import httpx
from typing import Any, Dict

async def get_myvariant(gene: str, alteration: str) -> Dict[str, Any]:
    """Fetch variant data from MyVariant.info API."""
    url = "https://myvariant.info/v1/query"

    # Build search query for the variant
    # MyVariant.info uses HGVS notation, but we'll search by gene and dbSNP/COSMIC
    query = f"{gene} AND {alteration}"

    params = {
        "q": query,
        "fields": "dbsnp,cosmic,clinvar,cadd,dbnsfp,civic",
        "size": 5
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(url, params=params)
            if r.status_code != 200:
                return {}

            data = r.json()
            hits = data.get("hits", [])

            if not hits:
                return {}

            # Use the first hit (most relevant)
            variant = hits[0]

            # Extract relevant information
            result = {
                "gene": gene,
                "variant": alteration,
                "dbsnp_id": variant.get("dbsnp", {}).get("rsid", "") if isinstance(variant.get("dbsnp"), dict) else "",
                "cosmic_id": variant.get("cosmic", {}).get("cosmic_id", "") if isinstance(variant.get("cosmic"), dict) else "",
                "clinvar": variant.get("clinvar", {}),
                "cadd_score": variant.get("cadd", {}).get("phred", "") if isinstance(variant.get("cadd"), dict) else "",
                "dbnsfp": variant.get("dbnsfp", {}),
                "civic": variant.get("civic", {}),
                "raw_data": variant  # Include full response for comprehensive analysis
            }

            return result

        except Exception:
            return {}