from app.models.pinecone_db import MODEL, query_pinecone
from app.config import PINECONE_NAMESPACE, PINECONE_SEARCH_RESULTS

def search_pinecone_service(query, top_k=PINECONE_SEARCH_RESULTS):
    vector = MODEL.encode(query).tolist()
    matches = query_pinecone(vector, top_k=top_k, namespace=PINECONE_NAMESPACE)
    
    # Deduplicate by title
    seen = set()
    unique_res = []
    for r in matches:
        title = r['metadata']['title']
        if title not in seen:
            unique_res.append(r)
            seen.add(title)
    return unique_res

def format_results(obj):
    desc_list = obj['metadata']['desc'].split('|@|')
    desc = ' '.join(desc_list)
    return {
        'title': obj['metadata']['title'],
        'link': obj['metadata']['link'],
        'desc': desc
    }

def perform_search(query):
    try:
        objarray = search_pinecone_service(query)
        return [format_results(o) for o in objarray]
    except Exception as e:
        return {"error": str(e)}
