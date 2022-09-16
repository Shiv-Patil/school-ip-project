# Student Analysis

## Steps to run locally

Recommended python version - 3.9 or above  

### Windows

Using a virtualenv:
```cmd
pip install virtualenv
virtualenv student_analysis
cd .\student_analysis
.\Scripts\activate
git clone https://github.com/Shiv-Patil/school-ip-project.git app
cd .\app
pip install -r requirements.txt
python .\main.py
```
Without virtualenv:
```cmd
git clone https://github.com/Shiv-Patil/school-ip-project.git app
cd .\app
pip install -r requirements.txt
python .\main.py
```

### Linux:

Using a virtualenv:
```sh
pip install virtualenv
virtualenv student_analysis
cd ./student_analysis
source ./bin/activate
git clone https://github.com/Shiv-Patil/school-ip-project.git app
cd ./app
pip install -r requirements.txt
python ./main.py
```
Without virtualenv:
```sh
git clone https://github.com/Shiv-Patil/school-ip-project.git app
cd ./app
pip install -r requirements.txt
python ./main.py
```
