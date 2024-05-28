# accountgpt-scraping

## Run and build using the command `docker compose up --build`


### To run with vector db update functionality,
- Uncomment the import of *update_vector* and *update_vector task* inside beat schedule in **main.py**
- Uncomment the *update_vector_db* task in **task.py**
- Update **run_raptor.py** file to add relevant code to build the vector db


### This system uses google serp api to get urls for queries. 
- **search_api/custom_search.py** and **load_redis/load_urls.py** can be updated to replace *serp api* with *google custom search api*