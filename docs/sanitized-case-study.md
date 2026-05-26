# Sanitized Case Study

## Scenario

A team needs to ask questions about internal documents without exposing confidential material. The system must retrieve relevant context, draft a grounded answer and warn the user when evidence is weak.

## Demo Approach

This repository implements a safe substitute for that workflow:

- fictitious documents;
- deterministic local embeddings;
- in-memory retrieval;
- SQLite metadata;
- simple agent boundaries;
- no external model calls;
- no private prompts;
- no customer data.

## What Reviewers Can Evaluate

- API design
- modular Python code
- retrieval reasoning
- test coverage
- Docker readiness
- documentation quality
- security posture for public portfolio work

