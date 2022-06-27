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
    location: Path = typer.Option(
        CWD,
        "--location",
        "-L",
        help="Directory to read and write from. Default: cwd",
    ),
    json_file: str = typer.Option(
        "cleaned_data.json",
        "--json",
        "-J",
        help="Json file to read. Default: cleaned_data.json",
    ),
    csv_file: str = typer.Option(
        "cleaned_data.csv",
        "--csv",
        "-C",
        help="Csv file to write. Default: cleaned_data.csv",
    ),
) -> None:
    """Writes a csv file based on the json data from PyBites."""
    json_path = location.resolve() / json_file
    csv_path = location.resolve() / csv_file
    if csv_path.is_file():
        print(f"[yellow]:warning: File already exists @ [/yellow]{csv_path}.")
        if not Confirm.ask("Do you want to overwrite the file?"):
            print("Exiting without creating a csv.")
            return
    data = pd.read_json(json_path)
    data.to_csv(csv_path)
    print(f"Successfully created csv file @ {csv_path}")


@cli.command()
def plot(
    location: Path = typer.Option(
        CWD, "--location", "-L", help="Directory to read csv. Default: cwd."
    ),
    csv_file: str = typer.Option(
        "cleaned_data.csv",
        "--csv",
        "-C",
        help="Csv file to read. Default: cleaned_data.csv.",
    ),
    sort_by_average: bool = typer.Option(
        False,
        "--sort-by-average",
        "-S",
        is_flag=True,
        help="Sort by average bites completed instead of class",
    ),
) -> None:
    """Plots average number of bites completed by class"""
    csv_path = location.resolve() / csv_file
    data = _clean_data(csv_path)
    if sort_by_average:
        data = data.sort_values("total_completed", ascending=True).reset_index()
    else:
        data = data.sort_values("class_", ascending=False).reset_index()

    plt.bar(data.class_, data.total_completed, orientation="h", width=0.3, marker="fhd")
    plt.theme("pro")
    plt.plot_size(75, (2 * len(data.class_) - 1) + 4)
    plt.title("Average Bites Completed by Class")
    plt.xlim(0, max(data.total_completed) * 1.1)
    plt.show()


@cli.command()
def stacked(
    location: Path = typer.Option(
        CWD, "--location", "-L", help="Directory to read csv. Default: cwd."
    ),
    csv_file: str = typer.Option(
        "cleaned_data.csv",
        "--csv",
        "-C",
        help="Csv file to read",
    ),
    sort_by_average: bool = typer.Option(
        False,
        "--sort-by-average",
        "-S",
        is_flag=True,
        help="Sort by average bites completed instead of class",
    ),
) -> None:
    """Plots average number of bites completed by class"""
    csv_path = location.resolve() / csv_file
    data = _clean_data(csv_path)
    if sort_by_average:
        data = data.sort_values("total_completed", ascending=False).reset_index()
    plt.plot_size((10 * len(data.class_) - 1 + 4), 30)
    plt.stacked_bar(
        data.class_,
        [data.newbie_completed, data.intro_completed, data.regular_completed],
        label=["Newbie", "Intro", "Regular"],
        width=0.6,
    )
    plt.ylim(0, max(data.total_completed) * 1.2)
    plt.theme("pro")
    plt.title("Average Bites Completed by Class")
    plt.show()


def _clean_data(csv_path: Path) -> pd.DataFrame:
    """Creates a pandas DataFrame from a csv file.

    :csv_path: Path to csv file
    :returns: pd.DataFrame
    """
    df = pd.read_csv(csv_path)
    return (
        df.where(df.class_ != "DEA")
        .assign(
            total_completed=lambda x: x.newbie_completed
            + x.intro_completed
            + x.regular_completed
        )
        .groupby(["class_"])
        .mean()
        .reset_index()
        .round(1)
    )


if __name__ == "__main__":
    cli()
