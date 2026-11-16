# Rider Matcher

A Python starter project using LangGraph to match the supplied ride requests with candidate drivers.

For each request, the graph considers candidates marked `available` and picks the smallest road pickup time. Ties are broken by straight-line distance, then driver ID. Requests without an available candidate return `null`. Each request is evaluated independently: this is a snapshot comparison, not a dispatch system, and it does not reserve drivers across requests. It uses the supplied statuses and estimates as-is.

## Run

Requires Python 3.10 or newer. From this directory:

```sh
python -m venv .venv
```

Activate the environment (`.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` on macOS/Linux), then:

```sh
python -m pip install -e .
python rider_matcher.py
```

The command prints JSON results. The two source CSVs are in `data/`; no API key or language model is needed.

## OpenRouter configuration

Add your key to the local `.env` file as `OPENROUTER_API_KEY=your-key`. This file is ignored by Git. `config.py` loads it into the environment and reads the key from `OPENROUTER_API_KEY`; an already-set environment variable takes precedence. The OpenRouter model ID is configured in `config.py`.

The current matching graph is deterministic and does not yet call OpenRouter, so it can run without a key.
