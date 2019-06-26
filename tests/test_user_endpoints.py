import json

import pytest
import requests_mock
from expects import be, be_above, expect, have_keys

from mci import app
from mci_database import db
from mci_database.db.models import Individual


class TestMCIAPI(object):
    def test_users_endpoint(self, mocker, database, individual, test_client, json_headers):
        '''
        Tests that the users endpoint returns expected content when the database has Individual entries.
        '''
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
        response = test_client.get('/users')

        assert response.status_code == 404
        assert response.json['users'] == []
        
        self._post_new_individual(individual, test_client, json_headers)

        response = test_client.get('/users')

        assert response.status_code == 200
        assert isinstance(response.json['users'][0], dict)
        assert 'mci_id' in response.json['users'][0].keys()

    def test_get_user_invalid(self, mocker, database, test_client):
        '''
        Tests that GETing an invalid user returns the correct error message.
        '''
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
        response = test_client.get('/users/123badid')

        assert response.status_code == 410
        assert response.json['message']
        assert response.json['message'] == 'An individual with that ID does not exist in the MCI.'
    
    def test_get_user_valid(self, mocker, database, individual, test_client, json_headers):
        '''
        Tests that GETing a valid user returns the JSON and 200 status code.
        '''
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)

        new_individual = self._post_new_individual(individual, test_client, json_headers)

        response = test_client.get('/users/{}'.format(new_individual['mci_id']))

        assert response.status_code == 200
        assert response.json
    
    def test_remove_pii_invalid_id(self, mocker, database, individual, test_client, json_headers):
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)

        response = test_client.post(
            '/users/remove-pii', data=json.dumps({"mci_id": "123fakeid"}), headers=json_headers)
        
        assert response.status_code == 410
        assert response.json['message'] == 'An individual with that ID does not exist in the MCI.'
    
    def test_remove_pii_valid_id(self, 
                                 mocker, 
                                 database, 
                                 individual, 
                                 test_client, 
                                 json_headers,
                                 app_configured):
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)

        new_individual = self._post_new_individual(individual, test_client, json_headers)
        
        with app_configured.app_context():
            assert database.session.query(Individual).filter_by(first_name=individual['first_name']).first()

            response = test_client.post(
                '/users/remove-pii',
                data=json.dumps({"mci_id": new_individual['mci_id']}),
                headers=json_headers)

            assert response.status_code == 201

            updated_individual = database.session.query(Individual).filter_by(mci_id=new_individual['mci_id']).first()
            assert updated_individual.first_name == None
            assert updated_individual.last_name == None
            assert updated_individual.middle_name == None
            assert updated_individual.date_of_birth == None
            assert updated_individual.email_address == None
            assert updated_individual.telephone == None
            assert updated_individual.ssn == None
        

    def _post_new_individual(self, individual, test_client, headers):
        '''
        Helper function for posting a new Individual to the MCI.
        Returns the JSON for the newly created Individual.
        '''
        with requests_mock.Mocker() as m:
            m.post("http://mcimatchingservice_mci_1:8000/compute-match",
                  json={"mci_id": "", "score": ""}, status_code=201)

            response = test_client.post('/users', data=json.dumps(individual), headers=headers)

            assert response.status_code == 201
            assert response.json['first_name'] == individual['first_name']
            assert response.json['last_name'] == individual['last_name']
        
        return response.json
