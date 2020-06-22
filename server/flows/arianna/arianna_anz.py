from framework.resources.resource import Resource
from framework.parsers.arianna_parser import AriannaParser

import pandas as pd
from collections import OrderedDict
import requests
import numpy as np
from datetime import datetime
import os
import json
import re
import hashlib


class Arianna(Resource):
    """ A Test Resource class using local files to test the TL of ETL """

    def __init__(self, resource_name, profile_id):
        """" Initialize all of variables and functions for Doubleclick Bid Manager to run  """
        super(Arianna, self).__init__(resource_name)
        self.profile_id = profile_id
        (
            self.advertiser_name,
            self.advertiser_match_table,
            self.campaign_key_number_match_table,
        ) = resource_name.split("/")
        self.location = "s3://phd-internal-archiving/PHDAKLDW/Arianna Reports/"

    def airtable_setup(self):
        # Set up Airtable API authorization

        return {"Authorization": "Bearer " + self.my_access_token}

    def get_airtable(self, tab):
        url = (
            "https://api.airtable.com/v0/"
            + self.profile_id
            + "/"
            + tab.replace(" ", "%20")
        )

        headers = self.airtable_setup()

        params = {
            "cellFormat": "string",
            "timeZone": "Pacific/Auckland",
            "userLocale": "Pacific/Auckland",
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()["records"]

            if "offset" in response.json():

                download_finished = False

                while download_finished is False:

                    params["offset"] = response.json()["offset"]
                    response = requests.get(url, headers=headers, params=params)
                    data += response.json()["records"]

                    if "offset" not in response.json():

                        download_finished = True

            data = [OrderedDict(datum["fields"]) for datum in data]

            return pd.DataFrame(data)

    def update_airtable(self, tab, dataframe):
        """ Upload new data to a table on Airtable """
        if dataframe.shape[0] > 0:
            url = (
                "https://api.airtable.com/v0/"
                + self.profile_id
                + "/"
                + tab.replace(" ", "%20")
            )

            headers = self.airtable_setup()
            headers["Content-Type"] = "application/json"

            data = dict()
            batch = []

            for record in dataframe.to_dict(orient="records"):
                if len(batch) == 10:
                    data["records"] = batch
                    batch = []
                    response = requests.post(
                        url, headers=headers, data=json.dumps(data)
                    )
                    data["records"] = list()

                batch.append({"fields": record})

            if len(batch):
                data["records"] = batch
                response = requests.post(url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                print("Data was successfully uploaded into " + tab + " table")

            else:
                print(
                    "Data failed to be upload into "
                    + tab
                    + " table (code: "
                    + response.status_code
                    + ")!"
                )

    def get_available_lastest_file_ids(self):
        """ Return a lastest file id sitting there waiting to be parsed """
        report_files = [
            report_file
            for report_file in self.fs.ls(self.location)
            if self.advertiser_name.lower() in report_file.lower()
            and ".csv" in report_file
        ]

        report_id = max(
            [
                datetime.strptime(
                    re.search(
                        "\d+_\d+_\d+", report_file.split("-")[-1].split(".")[0]
                    ).group(),
                    "%d_%m_%Y",
                )
                for report_file in report_files
            ]
        )

        return [report_id.strftime("%d_%m_%Y")]

    def download_file(self, file_id):
        """Create a local file and download data to the local file."""


    
    
    def get_anz_report(self):
        self.my_access_token = "key78NWdrIntYAHgD"
        try:
            for report_file in [
                report_file.split("/")[-1]
                for report_file in self.fs.ls(self.location)
                if self.advertiser_name.lower() in report_file.lower()
                and ".csv" in report_file
                and file_id in report_file
            ]:
                report_file_path = self.location + report_file
                target_df = pd.read_csv(
                    report_file_path,
                    skiprows=self.get_rows_to_skip(
                        report_file_path, header_end="Target"
                    ),
                    nrows=1,
                    encoding="ISO-8859-1",
                )
                print("Successfully read " + report_file_path + " file.")
                target_df = target_df.dropna(axis=1, how="all")
                df = pd.read_csv(
                    report_file_path,
                    skiprows=self.get_rows_to_skip(
                        report_file_path, header_end="Advertiser"
                    ),
                    encoding="ISO-8859-1",
                )
                df = df.dropna(axis=1, how="all")
                df = pd.concat([df, target_df], axis=1)
                df = df.fillna(method="ffill")
                df["Main Report Advertiser"] = self.advertiser_name
                report_file = report_file.split("-")
                df["File Source"] = "-".join(report_file[:4])

                match_df = self.get_airtable(self.advertiser_match_table)
                match_df = match_df.drop("Name", axis=1)
                match_columns = [
                    "Main Report Advertiser",
                    "Advertiser",
                    "Product",
                    "File Source",
                ]

                updating_match_df = self.get_updating_df(df, match_df, match_columns)
                self.update_airtable(self.advertiser_match_table, updating_match_df)

                df = df.merge(match_df, how="left", on=match_columns)
                df = df[df["Retain/Ignore"].str.contains("Retain", na=True)]

                df = df[~df["Client"].str.contains("IGNORE", na=False)]
                df["Week"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
                df["Week"] = df["Week"] - pd.to_timedelta(
                    df["Week"].dt.weekday + 1, unit="d"
                )
                df["Week"] = df["Week"].dt.strftime("%d/%m/%y")

                updating_match_df = df.loc[df["Client"] == "YES"]

                match_df = self.get_airtable(self.campaign_key_number_match_table)
                match_df = match_df.drop("Name", axis=1)
                match_columns = [
                    "Main Report Advertiser",
                    "Advertiser",
                    "Product",
                    "Advert",
                    "Week",
                ]

                updating_match_df = self.get_updating_df(
                    updating_match_df, match_df, match_columns
                )
                self.update_airtable(
                    self.campaign_key_number_match_table, updating_match_df
                )

                df = df.merge(match_df, how="left", on=match_columns)

                df = df.replace("n.a.", np.nan)
                df.Cost = (
                    df.Cost.astype(str)
                    .str.replace("$", "")
                    .str.replace("'", "")
                    .str.replace(",", "")
                    .str.strip()
                    .astype(float)
                )
                df.CPT = (
                    df.CPT.astype(str)
                    .str.replace("$", "")
                    .str.replace("'", "")
                    .str.replace(",", "")
                    .str.strip()
                    .astype(float)
                )
                df["Key Number"] = df["Advert"].apply(
                    lambda x: x.split("/")[0].replace(" ", "")
                    if x.split("/")[0]
                    else "Undefined"
                )
                #                df['Peak Check'] = 'Undefined'
                #                df['Position In Break'] = 'Undefined'
                #                df['Spot'] = np.nan

                df["Peak Check"] = df["Start Time"].apply(
                    lambda x: "Peak"
                    if x >= "18:00:00" and x <= "22:30:00"
                    else "Off Peak"
                )
                df["Position In Break"] = df.apply(self.get_position_in_break, axis=1)
                df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
                df["Strategy Name"] = (
                    df["Date"].dt.strftime("%d/%m/%Y")
                    + "_"
                    + df["Start Time"].apply(lambda x: ":".join(x.split(":")[:-1]))
                    + "_"
                    + df["Programme"].astype(str)
                    + "_"
                    + df["Arianna Abbrev"]
                )
                df["Date"] = df["Date"].dt.date
                df["Duration"] = df["Duration"].apply(
                    lambda x: str(
                        int(
                            (
                                datetime.strptime(x, "%H:%M:%S") - datetime(1900, 1, 1)
                            ).total_seconds()
                        )
                    )
                )

                match_df = self.store.get_redshift_table("Main_Publisher_Match_Table")
                match_df = match_df.drop("raw pub name", axis=1).drop_duplicates()

                df = df.merge(
                    match_df, how="left", left_on="Channel", right_on="site-channel"
                )

                # Prepare a local file to download the report contents to.
                file_name = file_id + ".csv"
                file_path = self.directory + "/" + file_name

                df = df.drop(
                    [
                        "Advertiser",
                        "Product",
                        "Week",
                        "Day Of Week",
                        "Start Time",
                        "Programme",
                        "Pos. in Break",
                        "Tot. Spots in Break\\Variables",
                        "CPT",
                        "Main Report Advertiser",
                    ],
                    axis=1,
                )

                if not os.path.isfile(file_path):
                    df.to_csv(file_path, index=False)
                else:  # else it exists so append without writing the header
                    df.to_csv(file_path, index=False, mode="a", header=False)

                print(
                    "File %s downloaded to %s"
                    % ("-".join(report_file), os.path.realpath(file_path))
                )

            return file_path

        except Exception as error:
            print(error)

    def get_position_in_break(self, df):
        if df["Pos. in Break"] == 1:

            return "True First"

        elif df["Pos. in Break"] == 2:

            return "First"

        elif df["Pos. in Break"] == df["Tot. Spots in Break\Variables"]:

            return "Last"

        else:

            return "Mid"

    def get_rows_to_skip(self, file_path, header_end=None):
        """ Find the number of rows to skip  based on the header end string """

        if header_end is not None:

            with self.fs.open(file_path, "r") as f:

                for count, value in enumerate(f, start=0):

                    if header_end in value:
                        # Then we've found the end of the header
                        f.close()

                        return count

        else:

            return None

    def hash_function(self, record):
        enconded_string = "".join(record.astype(str)).encode("utf-8")
        hashed_string = hashlib.sha512(enconded_string)

        return hashed_string.hexdigest()

    def get_updating_df(self, df, match_df, match_columns):
        df = df[match_columns].drop_duplicates()

        common = df.merge(match_df[match_columns], on=match_columns)

        df = df.set_index(df[match_columns].apply(self.hash_function, axis=1))
        common = common.set_index(
            common[match_columns].apply(self.hash_function, axis=1)
        )

        df = df[~df.isin(common)].dropna(how="all")

        return df.replace(np.nan, "")

    def generate_file_name(self):
        """Generates a report file name based on the file metadata."""

        file_name = "_Arianna_TV_Report"

        return self.advertiser_name.replace(" ", "_") + file_name + self.extension

    def get_parser(self):

        return AriannaParser()