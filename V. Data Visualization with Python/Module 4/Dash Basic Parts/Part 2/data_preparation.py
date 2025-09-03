# Import required libraries
import os
import time

import pandas as pd
import requests

dir_path = os.path.join("..", "..", "data")
os.makedirs(dir_path, exist_ok=True)


def download_file(url: str) -> str:
    print("Try to download file.")
    print("=" * 20)
    time.sleep(0.25)
    with requests.get(url=url, stream=True) as response:
        response.raise_for_status()

        filepath = os.path.join(dir_path, url.rsplit("/", 1)[-1])
        total_size = int(response.headers.get("Content-Length", 0))
        chunk_size = 1024 ** 2
        download_size = 0

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue

                file.write(chunk)
                download_size += len(chunk)

                if total_size > 0:
                    progress = (download_size / total_size) * 100
                    print(f"Downloading: {progress:.2f}% ({download_size} / {total_size} bytes)")

    time.sleep(0.25)
    print("Download Complete.")
    print("=" * 20)
    return filepath


# Read the airline data into the pandas dataframe
def data_preparing() -> pd.DataFrame:
    data_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv"
    filename = download_file(url=data_url)
    airline_data = pd.read_csv(filename, encoding="ISO-8859-1",
                               dtype={"Div1Airport": str, "Div1TailNum": str, "Div2Airport": str, "Div2TailNum": str})
    return airline_data
