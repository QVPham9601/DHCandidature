Before starting to generate new documents for the new semester, the folder `HOSO` (if exists) should be renamed
or deleted so that the new data won't mix with the old one.

Prerequisite: your machine need to have python3 installed to be able to run the scripts in this repo.

## (Do once) Install requirements
You can install the requirements in requirements.txt directly to your machine by executing
```
pip install -r requirements.txt
```
Or the better way to isolate your development environment is to create a virtual environment:

- Install virtualenv
```
sudo pip install virtualenv
```

- Create and activate virtual environment (using virtualenv)
```
virtualenv venv -p python3.5
source venv/bin/activate
```

- Install all the requirements
```
pip install -r requirements.txt
```

Every time you run the scripts in this repo, you'll need to activate the virtual environment by running: `source venv/bin/activate`

## Download and generate documents
Use the script `scripts/get_submissions.py`. Example:
- To download and generate candidate documents for semester `39` for Dong Hanh France, run:
```
python scripts/get_submissions.py -f fr -s 39
```
- To download and generate candidate documents for semester `39` for Dong Hanh Singapore, run:
```
python scripts/get_submissions.py -f sg -s 39
```
Documents are saved in `HOSO`. Interview forms are saved in `HOSO/fr/INTERVIEW` and `HOSO/sg/INTERVIEW`.

Note: candidates not having a motivation letter are put in the disqualified directory in each school.

### Merge documents by hand
Sometimes the program fails to merge the pdfs because the candidate has sent files in invalid format. All the failed files can be found in the `tmp` folder (e.g. `HOSO/fr/tmp/`)
The most common case is that the candidate uploaded a picture, but simply changed the extension of the file to .pdf to be able to upload.
In this case, we can try to change the extension of the file back to one of the format `.png`, `.jpeg` or `.jpg` and try to open them.
If successful, we can convert these files to pdf and merge them to the rest of the candidate's document by one of the available online/offline tool.
In case we can't recover the corrupted file, we can contact the student to resend them by mail.

## Simplify candidate data
1. Download csv files from 123formbuilder for each form e.g `Dulieu39_FR.csv` and `Dulieu39_SG.csv` and put in the project directory of this repo.

2 Run the following command to simplify the data in the csv where `39` is the semester number:
```
python scripts/simplify_candidate_data.py Dulieu39_FR.csv 39
python scripts/simplify_candidate_data.py Dulieu39_SG.csv 39
```
The output files have `_Simplified` suffix in the same directory as the input files.
These files can be shared with universities in Vietnam and they will be used as input source for Dong Hanh webapp (for evaluation)
