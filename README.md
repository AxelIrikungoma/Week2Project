# Validity and Spam Checks for Phone Numbers

## Description
The [main program](phone_validation.py) asks a user to input a phone number and checks whether
the phone number is valid or not per this [API](https://www.abstractapi.com/) and whether it has
been reported as a spam number per this [dataset](dnc_complaint_numbers_2021-07-08.csv) from the
[FTC (Federal Trade Commission)'s Do Not Call (DNC) Reported Calls Data](https://www.ftc.gov/site-information/open-government/data-sets/do-not-call-data), 
with daily updates.

All valid numbers are stored in a [SQL file](phone_number_file.sql) and a corresponding database
so that the API is not called if a phone number input by the user is already in the database.

The [second program](ds_analysis.py) creates a heatmap representing the number of spam calls by
state and by subject matter reported in the FTC's dataset.

Included in this project is also a [file](phone_num_test.py) to test a couple functions
that are part of the [main program code](phone_validation.py). Ultimately, this file test will be run each
and every time new changes are pushed to this GitHub repo.

## Developer Info
Name: Axel Irikungoma          | Email address: axel.irikungoma@vanderbilt.edu

Name: Chris Berniel Cobashatse | Email address: cc4536@columbia.edu

## Actions upon a push to GitHub
![check_style](https://github.com/cbcobashatse/Week2Project/actions/workflows/check_style.yaml/badge.svg)
![unittest](https://github.com/cbcobashatse/Week2Project/actions/workflows/unittest.yaml/badge.svg)

## License
[Click here for the license](license)