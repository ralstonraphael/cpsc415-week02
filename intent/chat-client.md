# Intent: One-question chat client

## Goal
A command-line program that sends one question to a language model and prints the answer, followed by a final line with the model name and the input and output token counts.

## Who it is for
The author, as a first program that calls a model API directly. Today the only way they talk to a model is through a chat app, which hides the request, the model, and the token counts.

## Constraints
- Python, standard library only. No packages.
- Calls OpenRouter's OpenAI-compatible chat endpoint. The base URL and model come from `CHAT_BASE_URL` and `CHAT_MODEL`; the key comes from `OPENROUTER_API_KEY`, which the author has already created with a small credit balance.
- Nothing secret in the code or the repository.

## Not in scope
Streaming, chat history, a web page, retries, and more than one provider at a time.

## Success looks like
1. It answers a question through OpenRouter and prints a usage line.
2. Changing only `CHAT_MODEL` points it at a different model.
3. The model name and token counts it prints match the request's entry on the OpenRouter Activity page.

## Open questions
None.

**Approved by:** _pending_
