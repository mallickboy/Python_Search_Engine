# Plan

- Create custom thraed handler that return results          (done)
- Create web crawler class that returns metadata and no of new entry and old delete



# Tasks (Today 25th aug complete on or before 30 Aug)
- Concurrent function handeler with long array inputs       (done)
- Write web crawler
  - Implement Breth first search                            (done)
  - Implement URL Validation check                          (done)
  - Implement URL normalizer to avoid redundency            (done)
  - Implement fast keyword doc macthing with ahocorasick    (done)
  - Test the crawler                                        (done)
  - Implement metadata collection and 3rd discard rule      (prog)
  - Test the crawler                                        ()
  - Save discarding and update statistics (out of service, 
        discarded, new url, title/first p3 update)                   

- system based operation handeler (ophal) with partial saving and resume facility for network/shutdown conditions
- Implement crawler handeler , waiting and fallback incase of net issue or shutdown requirement (use ophal)
- Implement Update cycle and handler for vector database (use ophal)
- Test the entire system on desktop and piserver
- Dockerize worker client try to ophal as well
- deploy dockerized worker
- Dockerize and deploy existing server code
- Build CI/CD for server code update
- Explore k8s or micro k8s deployment if possible 