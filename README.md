# One-question chat client

CPSC 415 Week 2 lab. `chat.py` sends one question to a model, prints the answer, then a final line with the model name and token counts. Python 3, standard library only. Built with a coding agent (Claude Code), as the course requires; the commits carry `Co-Authored-By` trailers.

Submitted after the September 28 deadline.

## How to run it

**`http` (default):** any OpenAI-compatible endpoint, such as OpenRouter or a local Ollama.

```
export CHAT_BASE_URL=https://openrouter.ai/api/v1   # the default
export CHAT_MODEL=minimax/minimax-m3
export OPENROUTER_API_KEY=...                       # from the environment, never a file
python3 chat.py "In one sentence, what is a context window?"
```

For Ollama: `CHAT_BASE_URL=http://localhost:11434/v1`, any string as the key, and `CHAT_MODEL=qwen3.5:9b`.

**`claude-cli`:** the `claude` tool in headless mode, on the Claude login already on this machine. No key.

```
export CHAT_BACKEND=claude-cli
CHAT_MODEL=claude-haiku-4-5-20251001 python3 chat.py "In one sentence, what is a context window?"
```

Optional: `CHAT_SYSTEM` replaces the system message, `CHAT_MAX_TOKENS` sets the output limit (default 500).

## Two corrections to the intent draft

Both are in the commit "Correct and approve intent for the chat client".

1. **The draft said I already had an OpenRouter key with credit.** I don't. I have a Claude subscription. So the program got a second route, `CHAT_BACKEND=claude-cli`, and OpenRouter stays the default for when a key exists.
2. **The draft's success test was matching the OpenRouter Activity page.** Without an account that page doesn't exist for me. The independent record is the session log the `claude` tool saves for each request, which the program never reads. It matched exactly (see `CHECKS.md`).

## One line I can explain

```python
"messages": [
    {"role": "system", "content": system},
    {"role": "user", "content": question},
],
```

This is where the request is built, in `ask_http`. The model gets two messages: the system message sets how it should behave, and the user message is the question. Changing only the system message to "You are a pirate" changed the answer's style while the question stayed the same, which is how I checked that this is really what the model reads.

## Two models compared

Haiku 4.5 and Sonnet 5 gave near-identical one-sentence answers. Sonnet used a third of Haiku's output tokens (38 against 116) but cost more, $0.00177 against $0.00113, at the list prices the `claude` tool reports. These are observed costs for one question, not a benchmark, and the subscription does not bill per call.

## Local model

`qwen3.5:9b` through Ollama, same code with only `CHAT_BASE_URL` and `CHAT_MODEL` changed. It spent most of its output on hidden reasoning: with an 800-token limit it was cut off mid-sentence, and with 4,000 it used 959 output tokens for a one-sentence answer. Its input was only 34 tokens, against about 550 through the `claude` tool, which adds its own overhead.
