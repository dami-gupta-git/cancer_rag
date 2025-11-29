import asyncio
import json
import typer
from cancerrag.annotator import annotate

app = typer.Typer(help="CancerRAG — LLM-powered variant annotation")

@app.command()
def run(
    gene: str = typer.Argument(..., help="Gene symbol, e.g. EGFR"),
    alteration: str = typer.Argument(..., help="Protein change, e.g. L858R or V600E"),
    tumor: str = typer.Option("Cancer", "--tumor", "-t", help="Tumor type")
):
    """Annotate a cancer variant in one command."""
    result = asyncio.run(annotate(gene, alteration, tumor))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    app()