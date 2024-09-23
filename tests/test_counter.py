"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import pytest
from src.counter import app
from src import status

@pytest.fixture()
def client():
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    '''Test cases for counter related endpoints'''

    def test_create_a_counter(self, client):
        ''' It should create a counter '''
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        ''' It should return error for duplicates '''
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        # create a counter
        result = client.post('/counters/my_counter')
        assert result.status_code == status.HTTP_201_CREATED

        # save the base of our counter and make sure we start at 0
        data = result.json
        baseline = data['my_counter']
        assert baseline == 0

        # call the update counter method
        result2 = client.put(f"/counters/my_counter")

        #make sure that our update was successful.
        assert result2.status_code == status.HTTP_200_OK

        #make sure that are counters data is now one more than previous
        # baseline. 
        data2 = result2.json
        curr_value = data2['my_counter']
        assert curr_value == baseline + 1


    def test_read_a_counter(self, client):
        #create a counter
        result = client.post('/counters/some_counter')
        assert result.status_code == status.HTTP_201_CREATED

        #hold counter
        counter = result.json['some_counter']

        #read from counter
        counter_name = "some_counter"
        result2 = client.get(f'/counters/{counter_name}')
        assert result2.status_code == status.HTTP_200_OK

        #compare the counter we are reading with the original counter
        read_counter = result2.json[counter_name]
        assert counter == read_counter 


    def test_fail_update_a_counter(self, client):
        result = client.put('/counters/idontexist')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_fail_read_a_counter(self, client): 
        result = client.get('/counters/idontexist')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_a_counter(self, client):
        #create a counter
        result = client.post('/counters/cilab_counter')
        assert result.status_code == status.HTTP_201_CREATED
        
        #delete the created counter
        result2 = client.delete('/counters/cilab_counter')
        assert result2.status_code == status.HTTP_204_NO_CONTENT

        #try to delete again
        result3 = client.delete('/counters/cilab_counter')
        assert result3.status_code == status.HTTP_404_NOT_FOUND
