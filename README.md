# Reproject GeoJSON on the fly from other CRS to EPSG 4326

Try the following

```
git clone https://github.com/ThomasG77/django-reproject-geojson.git
cd django-reproject-geojson
python3 -m venv venv # You may use python instead of python
source venv/bin/activate
pip install -r requirements.txt
cd geodjango
python manage.py runserver
```

Then open your browser to

http://127.0.0.1:8000/json-handler/?url=https://static.data.gouv.fr/resources/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/20240822-094641/qp-2024-epsg2154-20240820.geojson

The result is reprojected to EPSG 4326 whereas original source e.g https://static.data.gouv.fr/resources/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/20240822-094641/qp-2024-epsg2154-20240820.geojson is EPSG 2154 
