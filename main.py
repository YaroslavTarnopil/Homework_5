import typer
import asyncio
from currency_service import CurrencyService
from validators import validate_days

app = typer.Typer()

@app.command()
def get_exchange_rates(days: int = typer.Argument(1, help="Number of days to fetch rates for (max 10)")):
    validate_days(days)
    service = CurrencyService()
    try:
        results = asyncio.run(service.get_exchange_rates(days))
        for date, rates in results.items():
            typer.echo(f"Date: {date}")
            typer.echo(f"EUR: {rates['EUR']}, USD: {rates['USD']}\n")
    except Exception as e:
        typer.echo(f"Error: {e}")

if __name__ == "__main__":
    app()
