import pytest
import os
import json
from pathlib import Path

from spd import write_csv, plot, _clean_data

TEST_JSON = [
    {
        "name": "nottoday satan",
        "email": "nottoday.satan@pibites.org",
        "class_": "DEA",
        "profile_url": "https://codechalleng.es/profiles/nottodaysatan",
        "newbie_completed": 3,
        "intro_completed": 1,
        "regular_completed": 3,
        "certificates": ""
    },
    {
        "name": "nottoday satan",
        "email": "nottoday.satan@pibites.org",
        "class_": "period 2",
        "profile_url": "https://codechalleng.es/profiles/nottodaysatan",
        "newbie_completed": 2,
        "intro_completed": 8,
        "regular_completed": 1,
        "certificates": ""
    }
]

TEST_CSV = """
name,email,class_,profile_url,newbie_completed,intro_completed,regular_completed,certificates
nottoday satan,nottoday.satan@pibites.org,DEA,https://codechalleng.es/profiles/nottodaysatan,3,1,3,
nottoday satan,nottoday.satan@pibites.org,period 2,https://codechalleng.es/profiles/nottodaysatan,2,8,1,
"""


def test_csv_writer(tmp_path):
    d = tmp_path / "testing_dir"
    d.mkdir()
    json_file = 'test_data.json'
    with open(d / json_file, 'w') as f:
        json.dump(TEST_JSON, f)
    write_csv(location=d, json_file=json_file, csv_file='testing.csv')
    assert (d / 'testing.csv').is_file()


def test_plot(tmp_path, capfd):
    d = tmp_path / "testing_dir"
    d.mkdir()
    csv_file = 'test_csv.csv'
    with open(d / csv_file, 'w') as f:
        f.write(TEST_CSV.strip('\n'))
    plot(location=d, csv_file=csv_file)
    output = capfd.readouterr()[0].strip()
    assert "period 2" in output


def test_clean_data(tmp_path):
    d = tmp_path / "testing_dir"
    d.mkdir()
    csv_file = 'test_csv.csv'
    with open(d / csv_file, 'w') as f:
        f.write(TEST_CSV.strip('\n'))
    testing_data = _clean_data(d / csv_file)
    assert len(testing_data) == 1 # filters out the DEA
    assert testing_data.iloc[0]['total_completed'] == 11 # does the correct assinment for df.total_completed
