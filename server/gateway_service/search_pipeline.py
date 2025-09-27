import random
def random_response(count: int = 2):
    return random.choices(
        [
        {"title": "Array in java", "link": "https://www.javatpoint.com/array-in-java", "desc": "Array in java"},
        {"title": "What is an array", "link": "https://www.geeksforgeeks.org/what-is-array", "desc": "What is an array"},
        {"title": "Java tutorial", "link": "https://www.w3schools.com/java", "desc": "Java tutorial"},
        {"title": "Python tutorial", "link": "https://www.w3schools.com/python", "desc": "Python tutorial"},
        {"title": "Golang Concurrency", "link": "https://www.w3schools.com/golang", "desc": "Golang Concurrency"}
    ],
    k= count
    )

async def perform_search(request):
    print(request)
    return random_response(3)