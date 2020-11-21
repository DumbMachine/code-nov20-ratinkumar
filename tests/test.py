import os
import sys
import pytest

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath("../package"))
from utils import bmi_classify, load_data, parse_bmi_matrix, parse_bmi_native


def test_parse_bmi_native():
    input_data = [{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]
    expected_data = ([{'Gender': 'Female',
                       'HeightCm': 167,
                       'WeightKg': 82,
                       'bmi': 29.402273297715947,
                       'BMI Category': 'Overweight',
                       'Health risk': 'Enhanced risk'}],
                     1)

    output = parse_bmi_native(input_data)

    assert expected_data == output


def test_parse_bmi_matrix():
    input_data = pd.DataFrame([{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}])
    expected_data = {'Gender': 'Female',
                       'HeightCm': 167,
                       'WeightKg': 82,
                       'bmi': 29.402273297715947,
                       'BMI Category': 'Overweight',
                       'Health risk': 'Enhanced risk'}

    information, stats = parse_bmi_matrix(input_data)
    output = information.loc[0].to_dict()

    assert expected_data == output
    assert 1 == stats


@pytest.mark.parametrize("bmi,expected", [(11, ("Underweight", "Malnutrition risk")), (27, ("Overweight", "Enhanced risk"))])
def test_bmi_classify(bmi, expected):
    """
    Parametized test to check the output against multiple inputs
    """
    output = bmi_classify(bmi, format="np")
    assert expected == output
