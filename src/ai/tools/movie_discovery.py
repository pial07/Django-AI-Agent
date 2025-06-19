
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from tmdb import client as tmdb_client

@tool
def search_movies(query:str,limit:int=5,config:RunnableConfig={}):  
    """
    Search the most recent LIMIT movies from the movies database with maximum of 25.

    arguments:
    query: string or lookup search across title or content of document
    limit: number of results
    """
    configurable = config.get("configurable") or config.get('metadata')
    user_id = configurable.get('user_id')  # type: ignore
    print("searching with user:", user_id)
    response=tmdb_client.search_movie(query,raw=False)
    try:
        total_results=response.get("total_results") # type: ignore
    except:
        total_results=0  
    if total_results==0:
        return []     
    if total_results>25:
        limit=25     
    results=response.get("results")[:limit] # type: ignore
    return results

@tool
def movie_detail(movie_id:int,config:RunnableConfig={}):  
    """
    Movie detail from movie database if exists.

    arguments:
    movie_id: Integer from a movie search
    """
    configurable = config.get("configurable") or config.get('metadata')
    user_id = configurable.get('user_id')  # type: ignore
    print("searching with user:", user_id)
    response=tmdb_client.movie_detail(movie_id,raw=False)
    
    return response



movie_discovery_tools = [
    search_movies,
    movie_detail,
]