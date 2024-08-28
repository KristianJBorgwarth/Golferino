from rest_framework.test import APIRequestFactory

from core.features.golfcourse.golfcourse_view import GolfcourseView
from core.features.golfhole.golfhole_view import GolfholeView
from core.features.location.location_view import LocationView
from core.features.player.player_view import PlayerView
from core.features.playerround.playerround_view import PlayerroundView
from core.features.round.round_view import RoundView
from core.features.score.score_view import ScoreView


class DataImporter:

    @classmethod
    def create_user(cls, first_name: str, last_name: str, email: str, password: str):
        factory = APIRequestFactory()
        view = PlayerView.as_view({'post': 'create'})

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

        # Construct the request
        request = factory.post('/players/create', data, format='json')
        response = view(request)
        # Call the view with the request
        if response.status_code in (200, 201):
            print("User created:")
            print(response.data)
        else:
            raise Exception(f"User creation failed (response: {response.status_code}) ... {response.data}")

        return response

    @classmethod
    def create_location(cls, locationname: str, address: str, city: str):
        factory = APIRequestFactory()
        view = LocationView.as_view({'post': 'create'})

        data = {
            "locationname": locationname,
            "address": address,
            "city": city
        }

        # Construct the request
        request = factory.post('/locations/create', data, format='json')
        response = view(request)
        # Call the view with the request
        if response.status_code in (200, 201):
            print("Location created:")
            print(response.data)
        else:
            raise Exception(f"Location creation failed (response: {response.status_code}) ... {response.data}")

        return response

    @classmethod
    def create_golfcourse(cls, locationid: int, numholes: int, name: str):
        factory = APIRequestFactory()
        view = GolfcourseView.as_view({'post': 'create'})

        data = {
            "locationid": locationid,
            "numholes": numholes,
            "name": name
        }

        # Construct the request
        request = factory.post('/golfcourses/create', data, format='json')
        response = view(request)
        # Call the view with the request
        if response.status_code in (200, 201):
            print("Golfcourse created:")
            print(response.data)
        else:
            raise Exception(f"Golfcourse creation failed (response: {response.status_code}) ... {response.data}")
        return response

    @classmethod
    def create_golfhole(cls, golfcourseid: int, length: int, par: int, number: int):
        factory = APIRequestFactory()
        view = GolfholeView.as_view({'post': 'create'})

        data = {
            "golfcourseid": golfcourseid,
            "length": length,
            "par": par,
            "number": number
        }

        # Construct the request
        request = factory.post('/golfholes/create', data, format='json')
        response = view(request)
        # Call the view with the request
        if response.status_code in (200, 201):
            print("Golfhole created:")
            print(response.data)
        else:
            raise Exception(f"Golfhole creation failed (response: {response.status_code}) ... {response.data}")
        return response

    @classmethod
    def create_round(cls, golfcourseid: int, dateplayed: str):
        factory = APIRequestFactory()
        view = RoundView.as_view({'post': 'create'})

        data = {
            "golfcourseid": golfcourseid,
            "dateplayed": dateplayed,
        }
        request = factory.post('/rounds/create', data, format='json')
        response = view(request)
        if response.status_code in (200, 201):
            print("Round created:")
            print(response.data)
        else:
            raise Exception(f"Round creation failed (response: {response.status_code}) ... {response.data}")
        return response

    @classmethod
    def create_playerround(cls, playerid: int, roundid: int):
        factory = APIRequestFactory()
        view = PlayerroundView.as_view({'post': 'create'})

        data = {
            "playerid": playerid,
            "roundid": roundid,
        }

        # Construct the request
        request = factory.post('/playerrounds/create', data, format='json')
        response = view(request)
        # Call the view with the request
        if response.status_code in (200, 201):
            print("Playerround created:")
            print(response.data)
        else:
            raise Exception(f"Playerround creation failed (response: {response.status_code}) ... {response.data}")
        return response

    @classmethod
    def create_score(cls, playerroundid: int, golfholeid: int, strokes: int):
        factory = APIRequestFactory()
        view = ScoreView.as_view({'post': 'create'})

        data = {
            "playerroundid": playerroundid,
            "golfholeid": golfholeid,
            "strokes": strokes
        }

        # Construct the request
        request = factory.post('/scores/create', data, format='json')
        response = view(request)
        # Call the view with the request
        if response.status_code in (200, 201):
            print("Score created:")
            print(response.data)
        else:
            raise Exception(f"Score creation failed (response: {response.status_code}) ... {response.data}")
        return response
