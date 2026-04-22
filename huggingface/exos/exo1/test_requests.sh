#!/usr/bin/env bash

BASE_URL="http://localhost:8000"

echo "---- Health check ----"
curl -s "$BASE_URL/health" | jq
echo -e "\n"

echo "---- Detect (valid) ----"
curl -s -X POST "$BASE_URL/detect" \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour tout le monde"}' | jq
echo -e "\n"

echo "---- Detect (invalid: empty text) ----"
curl -s -X POST "$BASE_URL/detect" \
  -H "Content-Type: application/json" \
  -d '{"text": ""}' | jq
echo -e "\n"

echo "---- Detect (missing field) ----"
curl -s -X POST "$BASE_URL/detect" \
  -H "Content-Type: application/json" \
  -d '{}' | jq
echo -e "\n"

echo "---- Batch detect (valid) ----"
curl -s -X POST "$BASE_URL/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Bonjour tout le monde",
      "Hello world",
      "Hola mundo"
    ]
  }' | jq
echo -e "\n"

echo "---- Batch detect (invalid: too many items simulation) ----"
curl -s -X POST "$BASE_URL/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": []}' | jq
echo -e "\n"

echo "---- Batch detect (invalid: wrong type) ----"
curl -s -X POST "$BASE_URL/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": "not a list"}' | jq
echo -e "\n"
