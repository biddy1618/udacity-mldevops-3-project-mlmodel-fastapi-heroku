# Project structure

```bash
π¦path/to/project
 β£ π.dvc                           # DVC configuration folder
 β β£ π.gitignore
 β β πconfig
 β£ π.github                        # GitHub actions folder
 β β πworkflows
 β   β πpython-lint-pytest.yml     # Github actions for PEP8 and pytest checks
 β£ πsrc                            # Source files
 β β£ πapi_models                   # Definitions of API models
 β β β£ π__init__.py
 β β β£ πhelper.py
 β β β πmodels.py
 β β£ πapi_tests                    # API tests
 β β β£ π__init__.py
 β β β πtest_api.py
 β β£ πapi_tests_live               # Live API tests 
 β β β πtest_api_live.py
 β β£ πcheck_data                   # Tests for clean data (part of DVC stages)
 β β β£ π__init__.py
 β β β πtest_data.py
 β β£ πcheck_model                  # Tests for model pipeline and functions
 β β β£ π__init__.py
 β β β πtest_model.py
 β β£ πclean_data                   # Data cleaning folder (part of DVC stages)
 β β β£ π__init__.py
 β β β£ πclean_data.py
 β β β πhelper.py
 β β£ πdata                         # Folder to hold data
 β β β£ π.gitignore
 β β β πcensus.csv.dvc
 β β£ πeda                          # Folder for EDA of clean data and model ETL, EDA, and metrics check
 β β β πEDA.ipynb
 β β£ πevaluate_model               # Model evaluation folder for main metrics and slices (part of DVC stages)
 β β β£ π__init__.py
 β β β πevaluate_model.py
 β β£ πmetrics                      # Folder to hold metrics data
 β β β£ π.gitignore
 β β β πslice_output.txt           # File with slice metrics
 β β£ πmodel                        # Folder to hold model
 β β β π.gitignore
 β β£ πscreenshots                  # Screenshots
 β β β£ π.gitignore
 β β β£ πΌοΈapi-persons-path.png
 β β β£ πΌοΈapi-root-path.png
 β β β£ πΌοΈcoverage-report.png
 β β β£ πΌοΈdvc-dag.png
 β β β£ πΌοΈdvc-studio-metrics.png
 β β β£ πΌοΈdvc-studio-plots.png
 β β β£ πΌοΈgdrive-json-key.jpg
 β β β£ πΌοΈgdrive-service-account.jpg
 β β β£ πΌοΈgit-actions-secret.png
 β β β£ πΌοΈheroku-key.png
 β β β£ πΌοΈtests-general.png
 β β β£ πΌοΈtests-live-api.png
 β β β πΌοΈtests-sanity-check.png
 β β£ πsplit_data                   # Folder to split the data (part of DVC stages)
 β β β£ π__init__.py
 β β β πsplit_data.py
 β β£ πtrain_model                  # Folder to train the model (part of DVC stages)
 β β β£ πml                         # Folder to hold model helper functions
 β β β β£ π__init__.py
 β β β β£ πdata.py
 β β β β πmodel.py
 β β β£ π__init__.py
 β β β πtrain_model.py
 β β£ πREADME-deployment.md         # Information on the deployment
 β β£ πREADME-model-card.md         # Model card
 β β£ πREADME-data.md               # Information on the data
 β β£ πREADME.md                    # Information on the source code
 β β£ π__init__.py
 β β£ πconftest.py                  # PyTest fixtures
 β β£ πconstants.py                 # Module to hold constants
 β β£ βenvironment-dev.yml          # Conda environment definition for DEV mode
 β β£ πmain.py                      # Main script to start the API
 β β£ πrequirements-dev.txt         # Python packages for DEV mode
 β β£ πrequirements-test.txt        # Python packages for TEST mode
 β β πsanitycheck.py               # Some tests
 β£ π.dvcignore                     # DVC files to ignore
 β£ π.gitignore                     # GIT files to ignore
 β£ πAptfile                        # Apt file for Heroku to use
 β£ πLICENSE.txt                    # License
 β£ πProcfile                       # Main command to run for Heroku
 β£ πREADME-structure.md            # Structure of this project
 β£ πREADME.md                      # Main README file
 β£ βdvc.lock                       # DVC lock file
 β£ βdvc.yaml                       # DVC stages definition
 β£ βparams.yaml                    # Parameters to use for DVC
 β£ πpyproject.toml                 # Python project configuration
 β£ πrequirements.txt               # Production environment packages
 β πruntime.txt                    # Python runtime version for Heroku to use
```

## Tests

Configuration for the tests is at `src/conftest.py`.

* `src/api_tests/` - tests for the API.
* `src/check_data/` - tests for clean data.
* `src/check_model/` - tests for model pipeline functions.
* `src/check_api_live.py` - tests for live API (not part of the default PyTest tests).

In order to run the general tests, type following `pytest ./src/ -vv`:

![tests-general](src/screenshots/tests-general.png)

In order to test the live API, type following `pytest ./src/api_tests_live/ -vv`:

![tests-live-api](src/screenshots/tests-live-api.png)

### Note

Specify your own project URL in `src/api_tests_live/test_api_live.py` in `URL_TO_TEST` variable.

## Sanity check

Sanity check is passing as can be seen:

![sanity-check](src/screenshots/test-sanity-check.png)

## Test coverage

Run the following to get the report on the test coverage:
```bash
coverage run -m pytest . -vv
coverage report
```

![test-coverage-report](src/screenshots/coverage-report.png)

## DVC studio for metrics

Access the DVC metrics and plots through this [link](https://studio.iterative.ai/user/biddy1618/projects/udacity-mldevops-3-project-mlmodel-fastapi-heroku-vja0jevasy)

Metrics as follows:

![dvc-metrics](src/screenshots/dvc-studio-metrics.png)
Plots as follows:

![dvc-plots](src/screenshots/dvc-studio-plots.png)



