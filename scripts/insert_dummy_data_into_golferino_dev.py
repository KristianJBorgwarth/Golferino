import os
import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from data_importer import DataImporter

ur = DataImporter.create_user(first_name='foo', last_name='bar', email='foo@bar.com', password='Root123!')
lr = DataImporter.create_location(locationname='foocation', address='foodress', city='footy')
gcr = DataImporter.create_golfcourse(locationid=lr.data['data']['locationid'], numholes=5, name='foocourse')
ghr = DataImporter.create_golfhole(golfcourseid=gcr.data['data']['golfcourseid'], length=420, par=69, number=1)
rr = DataImporter.create_round(golfcourseid=gcr.data['data']['golfcourseid'], dateplayed='2024-05-01')
pr = DataImporter.create_playerround(playerid=ur.data['data']['id'], roundid=rr.data['data']['roundid'])
sr = DataImporter.create_score(playerroundid=pr.data['data']['playerroundid'], golfholeid=ghr.data['data']['golfholeid'], strokes=7)
