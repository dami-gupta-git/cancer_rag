PROMPT = """You are an expert cancer genomic pathologist.

Variant: {gene} {alteration}
Tumor type: {tumor_type}

Real evidence retrieved from MyVariant.info:
{myvariant_summary}

Return ONLY valid JSON (no markdown, no extra text):

{{
  "gene": "{gene}",
  "variant": "{alteration}",
  "dbsnp_id": "dbSNP ID if available",
  "cosmic_id": "COSMIC ID if available",
  "classification": "Oncogenic | Likely Oncogenic | VUS | Benign",
  "pathogenicity": "Pathogenic | Likely Pathogenic | VUS | Likely Benign | Benign",
  "recommended_therapies": [],
  "summary": "One-sentence plain-English explanation based on available evidence"
}}"""
