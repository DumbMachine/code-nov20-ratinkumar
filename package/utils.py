"""
Utilities used by other methods
"""
import os
import json
import random

import numpy as np
import pandas as pd

basedir = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
datadir = os.path.join(basedir, "data", "default.json")


def parse_bmi_native(data):
    """Extract BMi information from the each individual's information

    Args:
        person_dict (dict): Dict containing the :weight and :gender and :height
    """
    obese_itr = []
    for itr, person_dict in enumerate(data):
        required_keys = ["Gender", "HeightCm", "WeightKg"]
        assert set(required_keys).issubset(
            set(person_dict.keys())
        ), "Invalid format for person_dict"
        # convert the height to m2
        weight, height = person_dict["WeightKg"], person_dict["HeightCm"] / 100
        bmi = weight / (height ** 2)
        person_dict.update({"bmi": bmi})
        cat_info = bmi_classify(bmi)
        person_dict.update(cat_info)
        if person_dict["BMI Category"] == "Overweight":
            obese_itr.append(itr)
        data[itr] = person_dict

    return data, len(obese_itr)


def parse_bmi_matrix(data):
    """Extract BMi information from the each individual's information

    Args:
        person_dict (dict): Dict containing the :weight and :gender and :height
    """
    # data validation is skipped here as that was taken care of when creating the pandas dataframe
    weight, height = data["WeightKg"], data["HeightCm"] / 100
    data["bmi"] = weight / (height ** 2)
    data["BMI Category"], data["Health risk"] = zip(*data["bmi"].apply(lambda bmi: bmi_classify(bmi, format="np")))
    obese_len = len(data[data["BMI Category"] == "Overweight"])

    return data, obese_len

def bmi_classify(bmi, format="json"):
    if bmi < 18.4:
        remarks = ("Underweight", "Malnutrition risk")
    elif bmi >= 18.5 and bmi < 24.9:
        remarks = ("Normal Weight", "Low risk")
    elif bmi >= 25 and bmi < 29.9:
        remarks = ("Overweight", "Enhanced risk")
    elif bmi >= 30 and bmi < 34.9:
        remarks = ("Moderately obese", "Medium risk")
    elif bmi >= 35 and bmi < 39.9:
        remarks = ("Severely obese", "High risk")
    elif bmi >= 40:
        remarks = ("Very severly obese", "Very high risk")
    else:
        remarks = ("Invalid input", "Invalid input")

    if format == "json":
        return {
            "BMI Category": remarks[0], "Health risk": remarks[1]
        }
    return remarks


def load_data(location=datadir, format="json", length=0):
    data = json.load(open(location, "r"))
    if length != 0:
        r_indexes = [random.randint(0, len(data) - 1) for _ in range(length)]
        data = [data[index] for index in r_indexes]

    if format == "json":
        return data
    # matrix form
    else:
        # create a matrix for data, to avoid loop operations
        data = pd.DataFrame(data)
        return data
