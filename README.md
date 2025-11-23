---
title: Content Moderator API
emoji: 🛡️
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
---

# Content Moderator API

A minimalist, high-performance microservice for text moderation using DistilRoBERTa.

## API Usage

**Endpoint:** `POST /predict`

**Request:**
```json
{
  "text": "Your text here"
}
