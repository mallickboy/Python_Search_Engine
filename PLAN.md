# Python Search Engine – Build Plan

## Duration: 45 Days

---

## V3 - Core Features

### Phase 1

- [x] Create separate embedding service
- [x] Explore and benchmark other sentence transformer models for later update
- [x] Add separate search service
- [x] Implement persistent Pinecone index that supports high speed & automatic recovery
- [x] Implement search with URL sync and cached results in frontend
- [ ] Create user handler

### Phase 2

- [ ] Add caching with FastAPI
- [ ] Add batch embeding

### Phase 3

- [ ] Add analytics dashboard

### Phase 4

- [ ] Add database for search

### Phase 5

- [ ] Update the embedding model considering quality & speed

---

## V4 - Go & Dockerization

### Phase 1

- [ ] Convert user handler to Go

### Phase 2

- [ ] Convert caching handler to Go

### Phase 3

- [ ] Dockerize user handler
- [ ] Dockerize embedding service

### Phase 4

- [ ] Dockerize caching + search
- [ ] Ensure ephemeral nature of images

---

## Final Step

- [ ] Deploy to K8s or MicroK3s (V4.5)
- [ ] Redesign update client    (V5)
