---
title: Content Moderator API
sdk: docker
app_port: 7860
---

# Content Moderator API

A minimalist, high-performance microservice for binary text classification using microsoft/deberta-v3-xsmall.

## API Usage

**Endpoint:** `POST /predict`

**Request:**
```json
{
  "text": "Your text here"
}
