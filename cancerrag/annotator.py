
import asyncio
import json
import os
from openai import AsyncOpenAI
from cancerrag.databases import get_myvariant
from cancerrag.prompts import PROMPT

from dotenv import load_dotenv
load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def annotate(gene: str, alteration: str, tumor_type: str = "Cancer") -> dict:
    """Annotate a cancer variant using MyVariant.info data and LLM analysis."""

    # Fetch variant data from MyVariant.info
    variant_data = await get_myvariant(gene, alteration)

    # Format MyVariant.info data for the prompt
    if variant_data:
        myvariant_parts = []

        # COSMIC ID
        cosmic_id = variant_data.get("cosmic_id", "")
        if cosmic_id:
            myvariant_parts.append(f"COSMIC ID: {cosmic_id}")

        # dbSNP ID
        dbsnp_id = variant_data.get("dbsnp_id", "")
        if dbsnp_id:
            myvariant_parts.append(f"dbSNP ID: {dbsnp_id}")

        # ClinVar information
        clinvar = variant_data.get("clinvar", {})
        if clinvar and isinstance(clinvar, dict):
            clinical_sig = clinvar.get("clinical_significance", "")
            if clinical_sig:
                myvariant_parts.append(f"ClinVar Significance: {clinical_sig}")

        # CADD score
        cadd_score = variant_data.get("cadd_score", "")
        if cadd_score:
            myvariant_parts.append(f"CADD Score: {cadd_score}")

        # dbNSFP predictions
        dbnsfp = variant_data.get("dbnsfp", {})
        if dbnsfp and isinstance(dbnsfp, dict):
            sift = dbnsfp.get("sift", {})
            polyphen = dbnsfp.get("polyphen2", {})
            if sift:
                myvariant_parts.append(f"SIFT: {sift}")
            if polyphen:
                myvariant_parts.append(f"PolyPhen: {polyphen}")

        myvariant_summary = "\n".join(myvariant_parts) if myvariant_parts else "No MyVariant.info data available"
    else:
        myvariant_summary = "No MyVariant.info data found"

    # Call OpenAI API
    response = await client.chat.completions.create(
        model="gpt-4o-mini",  # change to gpt-4, gpt-4-turbo, etc.
        messages=[{
            "role": "user",
            "content": PROMPT.format(
                gene=gene,
                alteration=alteration,
                tumor_type=tumor_type,
                myvariant_summary=myvariant_summary
            )
        }],
        temperature=0.1,
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()

    # Parse JSON response
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "LLM returned invalid JSON", "raw_output": raw}
