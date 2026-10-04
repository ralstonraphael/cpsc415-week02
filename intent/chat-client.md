# Intent: One-question chat client

## Goal
A command-line program that sends one question to a language model and prints the answer, followed by a final line with the model name and the input and output token counts.

## Who it is for
The author, as a first program that calls a model API directly. Today the only way they talk to a model is through a chat app, which hides the request, the model, and the token counts.

## Constraints
- Python, standard library only. No packages.
- The default route is OpenRouter's OpenAI-compatible chat endpoint: base URL and model from `CHAT_BASE_URL` and `CHAT_MODEL`, key from `OPENROUTER_API_KEY`. The author has no OpenRouter key; he has a Claude subscription. So the program also has a second route, `CHAT_BACKEND=claude-cli`, that reaches Claude models through the `claude` command-line tool he is already logged into. Changing models is still one variable.
- Nothing secret in the code or the repository.

## Not in scope
Streaming, chat history, a web page, retries, and more than one provider at a time.

## Success looks like
1. It answers a question and prints a usage line, through the `claude-cli` route now and through OpenRouter whenever a key exists.
2. Changing only `CHAT_MODEL` points it at a different model.
3. The model name and token counts it prints match a record the program did not write. With no OpenRouter account there is no Activity page, so the record is the session log the `claude` tool saves for each request.

## Open questions
None.

**Approved by:** Ralston Raphael, October 4, 2026
