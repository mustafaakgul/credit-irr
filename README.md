# Credit IRR Calculation Project
* This project is a simple credit IRR calculation project. The project is written in Python and uses the Pandas library for data manipulation and the NumPy library for numerical calculations.
* Ref: https://numpy.org/numpy-financial/latest/

## Terminal Test
* python
* import numpy_financial as npf
* round(npf.irr([-100, 60, 60, 60, 60]), 5)
* from credit.models import IRRTable
* IRRTable.objects.bulk_create([
    IRRTable(index=1, index_type='AY', amount=100),
    IRRTable(index=2, index_type='AY', amount=200),
])

### Running in Local
* python3 -m venv venv
* source venv/bin/activate
* which python
* pip install -r requirements.txt
* python manage.py runserver 185.117.120.164:8080

### Deployment in Production
* Comment out database settings in settings.py
* python manage.py createsuperuser adminprod rfa56hA23 adminprod@test.com
