#!/usr/bin/env python3
"""Send one question to a model and print the answer, then a usage line.

Usage:  python3 chat.py "your question"

Routes, chosen with CHAT_BACKEND:
  http        (default) OpenAI-compatible chat endpoint. Reads CHAT_BASE_URL
              (default https://openrouter.ai/api/v1), CHAT_MODEL, OPENROUTER_API_KEY.
  claude-cli  The `claude` command in headless mode on the existing Claude login.
              Reads CHAT_MODEL.
Optional: CHAT_SYSTEM (system message), CHAT_MAX_TOKENS (output limit).
Standard library only. The key comes from the environment and is never printed.
"""
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

DEFAULT_SYSTEM = "You are a helpful assistant. Answer briefly."


def ask_http(question, model, system, max_tokens):
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("error: OPENROUTER_API_KEY is not set")
    base = os.environ.get("CHAT_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    # The request: one system message and one user message, plus an output limit.
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        "max_tokens": max_tokens,
    }
    request = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.load(response)
    except urllib.error.HTTPError as err:
        sys.exit("error: HTTP %d: %s" % (err.code, err.read().decode("utf-8", "replace")[:200]))
    except urllib.error.URLError as err:
        sys.exit("error: network: %s" % err)
    choice = data["choices"][0]
    usage = data.get("usage") or {}
    return {
        "answer": choice["message"].get("content") or "",
        "model": data.get("model", model),          # what the provider says it used
        "tokens_in": usage.get("prompt_tokens", 0),
        "tokens_out": usage.get("completion_tokens", 0),
        "finish_reason": choice.get("finish_reason"),
        "record": None,
        "cost": usage.get("cost"),
    }


def ask_cli(question, model, system, max_tokens):
    command = [
        "claude", "-p", "--model", model, "--output-format", "json",
        "--system-prompt", system, "--tools", "", "--disable-slash-commands",
        "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--setting-sources", "local",
    ]
    env = dict(os.environ)
    if max_tokens:
        env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(max_tokens)
    try:
        done = subprocess.run(command, input=question, capture_output=True, text=True,
                              timeout=120, cwd=tempfile.gettempdir(), env=env)
    except FileNotFoundError:
        sys.exit("error: the `claude` command was not found")
    if done.returncode != 0:
        sys.exit("error: claude exited %d: %s" % (done.returncode, (done.stderr or done.stdout)[:300]))
    data = json.loads(done.stdout)
    if data.get("is_error"):
        sys.exit("error: claude reported: %s" % str(data.get("result"))[:300])
    usage = data.get("usage") or {}
    used = list((data.get("modelUsage") or {}).keys())
    return {
        "answer": data.get("result") or "",
        "model": used[0] if used else model,       # what the tool says it used
        "tokens_in": usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
                     + usage.get("cache_read_input_tokens", 0),
        "tokens_out": usage.get("output_tokens", 0),
        "finish_reason": data.get("stop_reason"),
        "record": data.get("session_id"),
        "cost": data.get("total_cost_usd"),
    }


def main(argv):
    if len(argv) != 2:
        print('usage: python3 chat.py "your question"', file=sys.stderr)
        return 2
    model = os.environ.get("CHAT_MODEL")
    if not model:
        sys.exit("error: CHAT_MODEL is not set")
    system = os.environ.get("CHAT_SYSTEM", DEFAULT_SYSTEM)
    max_tokens = int(os.environ.get("CHAT_MAX_TOKENS", "500"))
    backend = os.environ.get("CHAT_BACKEND", "http")
    if backend == "http":
        out = ask_http(argv[1], model, system, max_tokens)
    elif backend == "claude-cli":
        out = ask_cli(argv[1], model, system, max_tokens)
    else:
        sys.exit("error: CHAT_BACKEND must be http or claude-cli")
    print(out["answer"].strip() or "(empty answer)")
    line = "model=%s tokens in=%d out=%d finish=%s" % (
        out["model"], out["tokens_in"], out["tokens_out"], out["finish_reason"])
    if out["cost"] is not None:
        line += " cost=$%.5f" % out["cost"]
    if out["record"]:
        line += " session=%s" % out["record"]
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
