# Agent Design

The agent layer separates workflow steps into small, testable classes.

## IngestionAgent

Input: document text and source labels.

Output: indexed chunks and source metadata.

Responsibility: prepare documents, call chunking and store embeddings.

## RetrievalAgent

Input: user question and `top_k`.

Output: ranked search results.

Responsibility: retrieve relevant chunks without drafting the final answer.

## AnswerAgent

Input: question and retrieved context.

Output: concise grounded answer.

Responsibility: draft an answer only from retrieved context.

## ValidationAgent

Input: answer and retrieved context.

Output: confidence and warnings.

Responsibility: make weak or missing context explicit.

## Why Split The Steps

Separating ingestion, retrieval, answer generation and validation makes the code easier to test and explain. It also mirrors production GenAI systems where each stage may have different failure modes, metrics and owners.

