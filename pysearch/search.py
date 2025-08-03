import os
# from dotenv import load_dotenv
# load_dotenv()
# from pinecone import Pinecone 
from config import MODEL, SEARCH_CLIENT, GET_RESULT_COUNT


def search_pinecone(client, model,query,table,namespace,res):
    # pc=Pinecone(api_key=os.getenv("PINECONE_KEY"),environment=os.getenv("PINECONE_ENVIRONMENT"))
    index=client.Index(table)
    
    result=index.query(
        namespace=namespace,
        vector=model.encode(query).tolist(),
        top_k=res,
        include_values=False,
        include_metadata=True,
        # filter={"genre": {"$eq": "action"}}
    )
    prev=[]
    new_res=[]
    for i,res in    enumerate(result['matches']): 
        show=res['metadata']
        title=show['title']
        if title not in prev:
            new_res.append(res)
            prev.append(title)
    return new_res

def get_title_and_link_and_desc(obj):    
    descList = obj['metadata']['desc'].split('|@|')
    desc = ' '.join(descList)    
    return {'title': obj['metadata']['title'], 'link': obj['metadata']['link'], 'desc': desc}

def perform_search(query):
    objarray=search_pinecone(SEARCH_CLIENT, MODEL,query,'search','ns2', GET_RESULT_COUNT)# matches top GET_RESULT_COUNT and serves them
    result_array = [get_title_and_link_and_desc(o) for o in objarray]
    return result_array