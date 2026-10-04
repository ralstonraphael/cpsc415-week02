# Checks

Question for every run: "In one sentence, what is a context window?" All runs on October 4, 2026.

No OpenRouter account exists, so the hosted runs use `CHAT_BACKEND=claude-cli` (the `claude` tool on a Claude subscription) and the local run uses the `http` backend against Ollama. Costs are the list prices the `claude` tool reports; the subscription does not bill per call.

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| Question through a hosted model | An answer and a usage line | Haiku 4.5 answered in one sentence. Usage line: `model=claude-haiku-4-5-20251001 tokens in=554 out=105 finish=end_turn` | Pass |
| Usage record matches | Same model; same or close token counts | No OpenRouter Activity page (no account). Checked instead against the session log the `claude` tool writes for that request (`~/.claude/projects/.../8c9dc772-....jsonl`), which the program never reads: model `claude-haiku-4-5-20251001`, input 554, output 105. Exact match. | Pass |
| System prompt changed | Answer style changes accordingly | `CHAT_SYSTEM="You are a pirate. Answer in pirate speak, one sentence."` gave "Arrr, a context window be the amount o' text and tokens a language model can process and remember at once, like the cargo hold o' me ship, savvy!" Output tokens rose from 116 to 282. | Pass |
| Output limit = 20 | Truncated or empty answer; tokens still billed | No answer at all. The `claude` tool returned an error ("response exceeded the 20 output token maximum") after 4 attempts, with 80 output tokens billed, all of them thinking tokens, and input grown to about 2,300 by the retries. Cost $0.0027 at list price, more than the normal call. The program exits with the error rather than printing a partial answer. | Pass (empty, tokens billed) |
| Model swapped | Different model name in usage; answer may differ | `CHAT_MODEL=claude-sonnet-5`: `model=claude-sonnet-5 tokens in=693 out=38`. Near-identical answer, a third of Haiku's output tokens. | Pass |
| Local model | Answer from localhost; no hosted entry | `CHAT_BACKEND=http CHAT_BASE_URL=http://localhost:11434/v1 CHAT_MODEL=qwen3.5:9b` through Ollama. With a 800-token limit it was cut off mid-sentence ("A context window is the maximum number", `finish=length`). With 4,000 it finished: 34 tokens in, 959 out. | Pass |

## Costs observed (list price, as reported by the `claude` tool)

| Model | Tokens in / out | Cost |
|---|---|---|
| claude-haiku-4-5-20251001 | 552 / 116 | $0.00113 |
| claude-sonnet-5 | 693 / 38 | $0.00177 |
| qwen3.5:9b (local) | 34 / 959 | free, runs on this machine |
