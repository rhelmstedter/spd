import json
import csv
from pathlib import Path
import pandas as pd
import plotext as plt
import typer
from rich import print
from rich.prompt import Confirm

CWD = Path.cwd()
cli = typer.Typer()


@cli.command()
def write_csv(
    json_file: str = typer.Option(
        "student_data.json",
        "--json",
        "-J",
        help="Json file to read"
    ),
    csv_file: str = typer.Option(
        "student_data.csv",
        "--csv",
        "-C",
        help="Csv file to write"
    ),
) -> None:
    """Writes a csv file based on the json data from PyBites"""
    json_path = CWD / json_file
    csv_path = CWD / csv_file
    if csv_path.is_file():
        print(f"[yellow]:warning: File already exists @ {csv_file}.")
        if not Confirm.ask("Do you want to overwrite the file?"):
            return
    with open(json_path) as f:
        data = json.load(f)
    with open(csv_path, "w") as out:
        writer = csv.writer(out)
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())
        print(f"Successfully created csv file @ {csv_file}")


@cli.command()
def plot(
    csv_file: str = typer.Option(
        "student_data.csv",
        "--csv",
        "-C",
        help="Csv file to read",
    ),
    sort: bool = typer.Option(
        False,
        "--sort",
        "-S",
        is_flag=True,
        help="Sort by total bites completed instead of class"
    ),
) -> None:
    """Plots average number of bites completed by class"""
    csv_path = CWD / csv_file
    df = pd.read_csv(csv_path)
    data = (
        df.where(df.class_ != "DEA")
        .assign(
            total_completed=lambda x: x.newbie_completed
            + x.intro_completed
            + x.regular_completed
        )
        .groupby(["class_"])
        .mean()
        .reset_index()
        .round(0)
    )
    if sort:
        data = data.sort_values('total_completed', ascending=True).reset_index()

    plt.bar(data.class_, data.total_completed, orientation="h", width=0.3, marker="fhd")
    plt.theme("pro")
    plt.plot_size(75, (2 * len(data.class_) - 1) + 4)
    plt.title("Average Bites completed by class")
    plt.xlim(0, 33)
    plt.show()


if __name__ == "__main__":
    cli()
