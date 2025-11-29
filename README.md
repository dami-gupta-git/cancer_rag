# CancerRAG

**LLM-powered cancer variant annotation using MyVariant.info**

CancerRAG combines the power of Large Language Models with the comprehensive MyVariant.info database to provide rapid, evidence-based interpretation of cancer genetic variants. Designed for clinicians, researchers, and bioinformaticians who need quick, contextual analysis of cancer mutations.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Comprehensive Variant Data**: Fetches variant information from MyVariant.info, aggregating data from multiple sources (COSMIC, dbSNP, ClinVar, CADD, dbNSFP, CIViC)
- **Multi-Database Integration**: Access to COSMIC IDs, dbSNP IDs, ClinVar annotations, and pathogenicity predictions
- **LLM-Powered Analysis**: Uses GPT-4, GPT-4o, or other OpenAI models for intelligent interpretation
- **Structured Output**: Returns JSON with classification, pathogenicity, therapy recommendations, and database identifiers
- **CLI Interface**: Simple command-line tool for rapid queries
- **Minimal Dependencies**: Lightweight implementation with just the OpenAI SDK

## Quick Start

### Installation

```bash
pip install cancerrag
```

### Setup

Create a `.env` file in your project directory with your API key:

```bash
# For OpenAI (default)
OPENAI_API_KEY=sk-...

# For other providers, see Configuration section
```

### Usage

```bash
# Basic usage with default tumor type
cancerrag BRAF V600E

# Specify tumor type
cancerrag BRAF V600E -t "Melanoma"
```

### Example Output
```json
{
  "gene": "BRAF",
  "variant": "V600E",
  "dbsnp_id": "rs113488022",
  "cosmic_id": "COSV57014428",
  "classification": "Oncogenic",
  "pathogenicity": "Pathogenic",
  "recommended_therapies": [
      "Vemurafenib",
      "Dabrafenib",
      "Trametinib"
  ],
  "summary": "The BRAF V600E variant is a well-established pathogenic oncogenic mutation commonly associated with melanoma and targeted by specific FDA-approved therapies."
}
```

## Installation from Source

For development or customization:

```bash
# Clone the repository
git clone https://github.com/yourusername/CancerRAG.git
cd CancerRAG

# Install in editable mode
pip install -e .
```

## Configuration

### Using Different Models

CancerRAG uses OpenAI's API. Edit [cancerrag/annotator.py](cancerrag/annotator.py) to configure your preferred model:

**Change the model:**
```python
# In annotator.py, line 61
response = await client.chat.completions.create(
    model="gpt-4o-mini",  # Change to: "gpt-4", "gpt-4-turbo", "gpt-4o", etc.
    messages=[...],
    temperature=0.1,
    max_tokens=500
)
```

**Supported OpenAI models:**
- `gpt-4o-mini` (default, fast and cheap)
- `gpt-4o` (latest, most capable)
- `gpt-4-turbo` (balanced performance)
- `gpt-4` (original GPT-4)

## Project Structure

```
CancerRAG/
├── cancerrag/
│   ├── __init__.py       # Package metadata
│   ├── cli.py            # Command-line interface (Typer)
│   ├── annotator.py      # Core annotation logic
│   ├── databases.py      # MyVariant.info API client
│   └── prompts.py        # Prompt template
├── examples/
│   ├── egfr.json         # Example EGFR output
│   └── braf.json         # Example BRAF output
├── pyproject.toml        # Project configuration
└── README.md
```

## How It Works

1. **Input**: User provides gene symbol, variant, and optionally tumor type
2. **Data Retrieval**: HTTP request fetches comprehensive variant data from MyVariant.info API
3. **Data Aggregation**: MyVariant.info aggregates information from COSMIC, dbSNP, ClinVar, CADD, dbNSFP, and CIViC
4. **Summarization**: Evidence is condensed and formatted for efficient LLM processing
5. **LLM Analysis**: Prompt instructs LLM to act as a genomic pathologist, considering all available evidence
6. **Structured Output**: LLM returns JSON with classification, pathogenicity, and therapy recommendations

## API Reference

### Command Line

```bash
cancerrag [GENE] [ALTERATION] [OPTIONS]

Arguments:
  GENE         Gene symbol (e.g., EGFR, BRAF, TP53)
  ALTERATION   Protein change (e.g., L858R, V600E)

Options:
  --tumor, -t  Tumor type (default: "Cancer")
  --help       Show help message
```

### Programmatic Usage

```python
import asyncio
from cancerrag.annotator import annotate

async def main():
    result = await annotate(
        gene="EGFR",
        alteration="L858R",
        tumor_type="Lung Adenocarcinoma"
    )
    print(result)

asyncio.run(main())
```

## Output Schema

```typescript
{
  "gene": string,                    // Gene symbol
  "variant": string,                 // Variant alteration
  "dbsnp_id": string,                // dbSNP identifier
  "cosmic_id": string,               // COSMIC database identifier
  "classification": string,          // Oncogenic | Likely Oncogenic | VUS | Benign
  "pathogenicity": string,           // Pathogenic | Likely Pathogenic | VUS | Likely Benign | Benign
  "recommended_therapies": string[], // List of therapy names
  "summary": string                  // Plain-English explanation
}
```

## Data Sources

**MyVariant.info** aggregates variant data from:
- **COSMIC**: Catalogue of Somatic Mutations in Cancer
- **dbSNP**: NCBI's Single Nucleotide Polymorphism database
- **ClinVar**: Public archive of relationships between variants and phenotypes
- **CADD**: Combined Annotation Dependent Depletion scores
- **dbNSFP**: Database for nonsynonymous SNPs' functional predictions (SIFT, PolyPhen, etc.)
- **CIViC**: Clinical Interpretation of Variants in Cancer

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_annotator.py

# Run with coverage
pytest --cov=cancerrag --cov-report=html
```

### Code Formatting

```bash
black cancerrag/
```

### Test Structure

The project includes comprehensive unit tests:
- `tests/test_databases.py`: Tests for MyVariant.info API integration
- `tests/test_annotator.py`: Tests for annotation logic and OpenAI integration
- `tests/test_prompts.py`: Tests for prompt templates

## Limitations

- **Not for Clinical Use**: This tool is for research and educational purposes only
- **LLM Hallucinations**: Always verify critical findings against primary sources
- **API Rate Limits**: MyVariant.info has usage limits for high-volume queries
- **Evidence Currency**: Database evidence may not reflect the latest research

## Roadmap

- [x] MyVariant.info integration for comprehensive variant data
- [ ] Add HGVS notation support for better variant matching
- [ ] Implement batch processing for VCF files
- [ ] Add evidence citation tracking with source URLs
- [ ] Support multi-model comparison
- [ ] Generate PDF reports for tumor boards
- [ ] Add germline vs somatic variant handling
- [ ] Add custom filtering for specific data sources

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Citation

If you use CancerRAG in your research, please cite:

```bibtex
@software{cancerrag2025,
  author = {Gupta, Dami},
  title = {CancerRAG: LLM-powered cancer variant annotation},
  year = {2025},
  url = {https://github.com/dami-gupta-git/cancer_rag}
}
```

## Acknowledgments

- MyVariant.info for comprehensive variant aggregation
- COSMIC, dbSNP, ClinVar, CADD, dbNSFP, and CIViC for their invaluable databases
- OpenAI, Anthropic, and xAI for LLM access

## Contact

For questions or support, please open an issue on GitHub or contact dami.gupta@gmail.com

---

**Disclaimer**: This tool is for research purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment.