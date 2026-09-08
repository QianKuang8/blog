---
title: "Running a Software Factory Efficiently at Uber Scale"
source_url: "https://www.uber.com/us/en/blog/efficient-software-factory/"
domain: "uber.com"
description: "We just published a deep dive on how we keep AI coding costs under control at Uber, even as usage keeps climbing.\n\nSince February, weekly active employees across all functions on our agentic offerings grew 7x, and weekly agent requests grew 9.4x. Over that same stretch, total spend has relatively stabilized.\n\nWe broke total spend into an equation: users, sessions per user, turns per session, requests per turn, tokens per request, price per token, and treated each term as something we could measure and shrink on its own.\n\nA few examples: benchmark-driven model selection instead of a single fixed default, prompt-cache lifetimes matched to how long engineers actually pause mid-session, MCP tools resolved through a CLI instead of preloaded into every session's context, and a session dashboard that automatically flags more than a dozen categories of wasted spend."
author: "Uday Kiran Medisetty"
published_at: "2026-08-27"
retrieved_at: "2026-09-08T15:11:34+08:00"
extractor: "defuddle"
---
