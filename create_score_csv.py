#!/usr/bin/env python3
"""
    Create CSV file for dci scores from 2016 - 2023
"""
from time import sleep
from tqdm import tqdm
import requests
import bs4
from bs4 import BeautifulSoup


HEADER = "year,corps_name,rank,score\n"


def write_to_csv(score_year: int, score_list: list) -> None:
    """
    Write data to our csv
    """
    with open("scores.csv", "a", encoding="ASCII") as outfile:
        outfile.write(f"{score_year},{score_list[1]},{score_list[0]},{score_list[2]}\n")


if __name__ == "__main__":
    # write header to scores
    with open("scores.csv", "w", encoding="ASCII") as file:
        file.write(HEADER)

    # get scores by year
    for year in tqdm(range(2016, 2024, 1)): # 2016-2023
        base_url: str = f"https://www.dci.org/scores/final-scores/{year}-dci-world-championship-finals"
        if year == 2016:
            base_url = base_url.replace("championship", "championships")
        # get webpage
        request = requests.get(base_url, timeout=5)
        soup = BeautifulSoup(request.text, "html.parser")
        tr_sections: bs4.element.ResultSet = soup.find_all("tr") # get every section of scores
        for section in tr_sections:
            section_list = section.contents
            part_list = [parts.text for parts in section_list]
            if part_list[0].isdigit():
                write_to_csv(year, part_list)

        sleep(5) # stop from getting found out
