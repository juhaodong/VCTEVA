import requests
import json
import gzip
import shutil
import time
import os
from io import BytesIO

def main(LEAGUE, YEAR):

    S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

    def download_gzip_and_write_to_json(file_name):
        if os.path.isfile(f"{file_name}.json"):
            return False

        remote_file = f"{S3_BUCKET_URL}/{file_name}.json.gz"
        response = requests.get(remote_file, stream=True)

        if response.status_code == 200:
            gzip_bytes = BytesIO(response.content)
            with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
                with open(f"../DATA/{file_name}.json", 'wb') as output_file:
                    shutil.copyfileobj(gzipped_file, output_file)
                print(f"{file_name}.json written")
            return True
        elif response.status_code == 404:
            # Ignore
            return False
        else:
            print(response)
            print(f"Failed to download {file_name}")
            return False


    def download_esports_files():
        directory = f"{LEAGUE}/esports-data"

        if not os.path.exists(f"../DATA/{directory}"):
            os.makedirs(f"../DATA/{directory}")

        esports_data_files = ["leagues", "tournaments",
                            "players", "teams", "mapping_data_v2"]
        for file_name in esports_data_files:
            download_gzip_and_write_to_json(f"{directory}/{file_name}")
            

    def download_games():
        start_time = time.time()

        local_mapping_file = f"../DATA/{LEAGUE}/esports-data/mapping_data_v2.json"
        with open(local_mapping_file, "r") as json_file:
            mappings_data = json.load(json_file)

        local_directory = f"../DATA/{LEAGUE}/games/{YEAR}"
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        game_counter = 0

        for esports_game in mappings_data:
            s3_game_file = f"{LEAGUE}/games/{YEAR}/{esports_game['platformGameId']}"

            response = download_gzip_and_write_to_json(s3_game_file)
            
            if (response == True):
                game_counter += 1
                if game_counter % 10 == 0:
                    print(f"----- Processed {game_counter} games, current run time: {round((time.time() - start_time)/60, 2)} minutes")
    download_esports_files()
    #download_games()

if __name__ == "__main__":
    main("game-changers", 2022)
    #Failed to download game-changers/games/2023/val:cedd61d9-0fab-4615-bea5-7a446ee3c2ed