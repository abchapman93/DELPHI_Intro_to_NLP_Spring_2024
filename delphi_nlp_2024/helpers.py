import sys
sys.path.append("..")

import os, glob
import re

from .quizzes.quizzes import *
#from quizzes.module_1_exercise_quizzes import *
import ipywidgets as widgets
import pandas as pd

import numpy as np
def square(x):
    return x**2

def add(x, y):
    return x + y

def print_name(first, last, middle=None):
    if middle is None:
        print(f"My name is {first.title()} {last.title()}")
    else:
        print(f"My name is {first.title()} {middle[0].title()}. {last.title()}")


def build_nlp_context(rules=True):
    import medspacy
    from medspacy.target_matcher import TargetRule
    if rules:
        nlp = medspacy.load()
    else:
        nlp = medspacy.load()
        nlp.remove_pipe("medspacy_context")
        nlp.add_pipe("medspacy_context", config={"rules": None})

    target_rules = [
        TargetRule("pneumonia", "DIAGNOSIS"),
        TargetRule("bronchitis", "DIAGNOSIS"),
        TargetRule("nephrectomy", "PROCEDURE"),
        TargetRule("pneumothorax", "DIAGNOSIS"),
        TargetRule("breast cancer", "DIAGNOSIS"),
        TargetRule("warfarin", "MEDICATION"),
        TargetRule("rash", "SIGN/SYMPTOM"),
        TargetRule("diabetes", "DIAGNOSIS"),

        TargetRule("COVID-19", "DIAGNOSIS", pattern=r"covid-?(19)?"),
        TargetRule("SARS-COV-2", "DIAGNOSIS")
    ]

    nlp.get_pipe("medspacy_target_matcher").add(target_rules)

    return nlp

import pickle
def load_pneumonia_data(split_set="train", directory=None):
    if split_set not in ("train", "test"):
        raise ValueError(f"split_set must be one of ('train', 'test'), not {split_set}")
    if directory is None:
        url = "https://github.com/abchapman93/DELPHI_Intro_to_NLP_Spring_2024/raw/main/data/pneumonia_data/{}.pkl"
        df = pd.read_pickle(url.format(split_set))
    else:
        fp = os.path.join(directory, split_set+".pkl")
        with open(fp, "rb") as f:
            df = pickle.load(f)
    return df

LABEL_MAPPING = {'PNEUMONIA_DOC_YES': 1, 'PNEUMONIA_DOC_NO': 0}

regexes = [
    re.compile('[_]{3,}'),
    re.compile('\[\*\*[\d\-a-z\s\(\)]+\*\*\]')
]



def read_original_pneumonia_data(directory):
    text_files = glob.glob(os.path.join(directory, 'subject*.txt'))

    record_data = []
    for text_file in text_files:
        d = {}

        record_id = os.path.splitext(os.path.basename(text_file))[0]
        anno_file = os.path.join(directory, '{}.ann'.format(record_id))
        d['record_id'] = record_id

        with open(text_file) as f:
            d['text'] = f.read()
            # d['preprocessed_text'] = preprocess(d['text'])

        with open(anno_file) as f:
            lines = f.readlines()
            d['annotations'] = lines
            for line in lines:
                anno = line.split('\t')[1]
                anno_label = anno.split(' ')[0]
                if anno_label not in LABEL_MAPPING:
                    continue

                d['document_classification'] = LABEL_MAPPING[anno_label]

        record_data.append(d)

    return pd.DataFrame(record_data)


def preprocess(text):
    text = text.strip()
    for regex in regexes:
        text = regex.sub('', text)
    return text


def read_pneumonia_documents(directory):
    text_files = glob.glob(os.path.join(directory, 'subject*.txt'))
    dicts = []
    for file in text_files:
        name = os.path.splitext(os.path.basename(file))[0]
        text = open(file).read()
        dicts.append(dict(text=text, name=name))
    return pd.DataFrame(dicts)