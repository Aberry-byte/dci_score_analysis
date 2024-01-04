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
# it's just easier to pull the last 10 years manually
YEAR_URLS = ["https://www.dci.org/scores/final-scores/2013-dci-world-championship-finals",
            "https://www.dci.org/scores/final-scores/2014-dci-world-championships-world-class-finals",
            "https://www.dci.org/scores/final-scores/2015-dci-world-championship-world-class-finals",
            "https://www.dci.org/scores/final-scores/2016-dci-world-championships-finals",
            "https://www.dci.org/scores/final-scores/2017-dci-world-championship-finals",
            "https://www.dci.org/scores/final-scores/2018-dci-world-championship-finals",
            "https://www.dci.org/scores/final-scores/2019-dci-world-championship-finals",
            "https://www.dci.org/scores/final-scores/2020-dci-world-championship-finals",
            "https://www.dci.org/scores/final-scores/2021-dci-world-championship-finals",
            "https://www.dci.org/scores/final-scores/2022-dci-world-championship-finals",
            "https://www.dci.org/scores/final-scores/2023-dci-world-championship-finals"]


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
    for year, url in tqdm(zip(range(2013, 2024, 1), YEAR_URLS), total=len(YEAR_URLS)): # 2016-2023
        # get webpage
        request = requests.get(url, timeout=5)
        soup = BeautifulSoup(request.text, "html.parser")
        tr_sections: bs4.element.ResultSet = soup.find_all("tr") # get every section of scores
        for section in tr_sections:
            section_list = section.contents
            part_list = [parts.text for parts in section_list]
            if part_list[0].isdigit():
                write_to_csv(year, part_list)

        sleep(3) # stop from getting found out
