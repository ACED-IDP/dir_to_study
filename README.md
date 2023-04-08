  
# dir_to_study

A utility to create a "bare bones" [ResearchStudy](https://hl7.org/fhir/r4b/researchstudy.html) with [DocumentReference](https://hl7.org/fhir/r4b/documentreference.html)


## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e . 
```

## Use

```
dir_to_study --help
Usage: dir_to_study [OPTIONS]

  Transform ResearchStudy, DocumentReference from matching files in input
  path.

Options:
  --project_id TEXT   program-project  [required]
  --input_path TEXT   Read files from this path  [required]
  --output_path TEXT  Write FHIR resources to this path  [required]
  --pattern TEXT      File names to match.  [default: **/*]
  --help              Show this message and exit.
  

dir_to_study  --project_id aced-test --input_path ./tests/fixtures/ --output_path /tmp/aced-test
$ tree /tmp/aced-test/
/tmp/aced-test/
├── DocumentReference.ndjson
└── ResearchStudy.ndjson
```


## Test

* fixtures

```
tests/
├── fixtures
│    ├── file-1.txt
│    ├── file-2.csv
│    └── sub-dir
│        ├── file-3.pdf
│        ├── file-4.tsv
│        └── file-5

```

* run

```
pip install -r requirements-dev.txt
pytest
$ pytest
====================================================================================== test session starts =======================================================================================
platform darwin -- Python 3.9.12, pytest-7.2.2, pluggy-1.0.0
rootdir: /Users/walsbr/aced/data_model/dir_to_study
collected 1 item

tests/test_dir_to_study.py .                                                                                                                                                               [100%]

======================================================================================= 1 passed in 0.02s ========================================================================================
```
