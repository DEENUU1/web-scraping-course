import os
import json
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Params:
    key: str
    value: str

@dataclass
class Location:
    city: str
    region: str
    district: Optional[str] = None

@dataclass
class Offer:
    title: str
    url: str
    created_time: str
    description: str
    location: Optional[Location] = None
    params: List[Optional[Params]] = None

def get_all_filenames():
    res = []
    for file in os.listdir("./"):
        if file.startswith("olx_data"):
            res.append(file)

    return res


def read_file(filename: str):
    with open(filename, "r") as file:
        data = json.load(file)
        return data


def process_localization(location):
    district_name = None

    city_object = location.get("city", None)
    district_object = location.get("district", None)
    region_object = location.get("region", None)

    if district_object:
        district_name = district_object.get("name", None)

    if city_object and region_object:
        return Location(
            city=city_object.get("name"),
            region=region_object.get("name"),
            district=district_name
        )


def process_params(params):
    processed_params = []

    for param in params:
        key = param.get("key")
        value_container = param.get("value")
        value_key = value_container.get("key")

        if key == "price":
            processed_params.append(
                Params(
                    key=key,
                    value=str(value_container.get("value"))
                )
            )

        processed_params.append(
            Params(
                key=key,
                value=value_key
            )
        )

    return processed_params

def process(data):
    processed_data = []

    for d in data["data"]:
        title = d.get("title")
        url = d.get("url")
        date = d.get("created_time")
        desc = d.get("description")
        location = process_localization(d.get("location"))
        params = process_params(d.get("params"))

        processed_data.append(
            Offer(
                title=title,
                url=url,
                created_time=date,
                description=desc,
                location=location,
                params=params
            )
        )

    return processed_data


json_files = get_all_filenames()
for file in json_files:
    data = read_file(file)
    processed = process(data)

    for p in processed:
        print(f"{p.title} {p.url} {p.created_time}")
        print(p.description)
        print(p.location)
        print(p.params)
        print("\n\n\n")