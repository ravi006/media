from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
import requests
from . import config
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()

class Band(Resource):

    def get(self, band_id):
        print("Call for: GET /bands/%s" % band_id)
        url = config.es_afiremedia_url['bands']+'/'+band_id
        resp = requests.get(url)
        data = resp.json()
        band = data['_source']
        return band

    def put(self, beer_id):
        """TODO: update functionality not implemented yet."""
        pass

    def delete(self, band_id):
        print("Call for: DELETE /bands/%s" % band_id)
        url = config.es_afiremedia_url['bands']+'/'+band_id
        resp = requests.delete(url)
        data = resp.json()
        return data

class BandsList(Resource):

    def get(self):
        print("Call for: GET /bands")
        url = config.es_afiremedia_url['bands']+'/_search'
        query = {
            "query": {
                "match_all": {}
            },
            "filter": {
                "has_child": {
                    "type": "youtube",
                    "query": {
                        "match": {
                            "bandname": {
                                "query": "Green Day",
                                "operator": "or"
                            }
                        }
                    }
                }
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        bands = []
        for hit in data['hits']['hits']:
            band = hit['_source']
            band['id'] = hit['_id']
            bands.append(band)
        return bands

class BandAndYoutube(Resource):

    def get(self):
        print("Call for: GET /bands")
        url = config.es_afiremedia_url['bands']+'/_search'
        query = {
            "query": {
                "match_all": {}
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        bands = []
        for hit in data['hits']['hits']:
            band = hit['_source']
            band['id'] = hit['_id']
            bands.append(band)
        return bands

class YoutubeList(Resource):

    def get(self):
        print("Call for /youtube")
        url = config.es_afiremedia_url['youtube']+'/_search'
        query = {
            "query": {
                "match_all": {}
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        youtube_list = []
        for hit in data['hits']['hits']:
            youtube = hit['_source']
            youtube['id'] = hit['_id']
            youtube_list.append(youtube)
        return youtube_list

class AfiremediaSearch(Resource):

    def get(self):
        print("Call for GET /search")
        parser.add_argument('q')
        query_string = parser.parse_args()
        url = config.es_afiremedia_url['bands']+'/_search'
        query = {
            "query": {
                "multi_match": {
                    "fields": ["bandname", "band_type", "members", "albums", "description"],
                    "query": query_string['q'],
                    "type": "cross_fields",
                    "use_dis_max": False
                }
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        bands = []
        for hit in data['hits']['hits']:
            band = hit['_source']
            band['id'] = hit['_id']
            bands.append(band)
        return bands

api.add_resource(Band, config.api_base_url+'/bands/<band_id>')
api.add_resource(BandsList, config.api_base_url+'/bands')
api.add_resource(BandAndYoutube, config.api_base_url+'/bandsyoutube')
api.add_resource(YoutubeList, config.api_base_url+'/youtubelist')
api.add_resource(AfiremediaSearch, config.api_base_url+'/afiresearch')


