"""Quiz generation from uploaded learning material.

Engine 1 (best): Claude via the Anthropic Messages API, used when the
ANTHROPIC_API_KEY environment variable is set on the backend.
Engine 2 (fallback, no key needed): a simple heuristic that turns sentences of
the material into fill-in-the-blank multiple-choice questions.
"""
import json
import os
import random
import re
import uuid
from collections import Counter
from typing import Any, Dict, List, Tuple

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MAX_CHARS = 20000
LETTERS = ["A", "B", "C", "D"]

STOPWORDS = set(
    """about above after again against because before being below between could during each
    either further having himself herself their theirs there these those through under until
    where which while would should shall other another among within without whether therefore
    however thereby whose whom such than then them they this that with will were what when
    your yours from into onto over also been does doing done more most much many some very""".split()
)


class QuizGenerationError(ValueError):
    pass


def _normalise(items: List[Dict[str, Any]], engine: str, difficulty: str, competency: str, title: str) -> List[Dict[str, Any]]:
    out = []
    for it in items:
        opts = [str(o).strip() for o in it["options"]][:4]
        correct_text = opts[int(it["correct_index"])]
        random.shuffle(opts)
        out.append(
            {
                "id": f"gen-{uuid.uuid4().hex[:8]}",
                "text": str(it["text"]).strip(),
                "type": "MCQ",
                "options": [{"key": LETTERS[i], "text": o} for i, o in enumerate(opts)],
                "correct_option": LETTERS[opts.index(correct_text)],
                "explanation": str(it.get("explanation", "")).strip(),
                "difficulty": difficulty,
                "competency": competency,
                "confidence": 0.9 if engine == "claude" else 0.6,
                "source": {
                    "document_title": title,
                    "page_number": 1,
                    "section": str(it.get("source_excerpt", "Uploaded material"))[:90],
                },
                "status": "draft",
            }
        )
    return out


async def _generate_with_claude(text: str, n: int, difficulty: str) -> List[Dict[str, Any]]:
    import httpx  # imported lazily so the heuristic works without it

    prompt = (
        f"Write {n} multiple-choice questions ({difficulty} difficulty) based ONLY on the material below. "
        "Each question needs exactly 4 options with one correct answer, plausible distractors, and a one-sentence "
        "explanation that cites the material. Return ONLY a JSON array, no other text. Each element: "
        '{"text": str, "options": [str, str, str, str], "correct_index": 0-3, '
        '"explanation": str, "source_excerpt": short quote from the material}.\n\n'
        f"MATERIAL:\n{text}"
    )
    body = {
        "model": os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
        "max_tokens": 4000,
        "system": "You are an assessment designer for government statistics training. Output valid JSON only.",
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    async with httpx.AsyncClient(timeout=90) as client:
        resp = await client.post(ANTHROPIC_URL, headers=headers, json=body)
        resp.raise_for_status()
    raw = "".join(b.get("text", "") for b in resp.json()["content"] if b.get("type") == "text")
    raw = raw[raw.index("[") : raw.rindex("]") + 1]
    items = json.loads(raw)
    valid = []
    for it in items:
        try:
            if (
                isinstance(it["options"], list)
                and len(it["options"]) >= 4
                and 0 <= int(it["correct_index"]) <= 3
                and str(it["text"]).strip()
            ):
                valid.append(it)
        except (KeyError, ValueError, TypeError):
            continue
    return valid[:n]


def _generate_heuristic(text: str, n: int) -> List[Dict[str, Any]]:
    rng = random.Random(len(text))
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if 8 <= len(s.split()) <= 40]
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-]{5,}", text) if w.lower() not in STOPWORDS]
    freq = Counter(w.lower() for w in words)
    pool = [w for w, _ in freq.most_common(60)]
    if len(pool) < 4 or not sentences:
        raise QuizGenerationError("Not enough text to build questions. Provide a longer passage (at least a few sentences).")
    rng.shuffle(sentences)
    items = []
    for s in sentences:
        cands = [w for w in re.findall(r"[A-Za-z][A-Za-z\-]{5,}", s) if w.lower() in freq and w.lower() not in STOPWORDS]
        if not cands:
            continue
        answer = max(cands, key=lambda w: (freq[w.lower()], len(w)))
        distractors = [w for w in pool if w != answer.lower()]
        distractors.sort(key=lambda w: abs(len(w) - len(answer)))
        picks = distractors[:6]
        rng.shuffle(picks)
        opts = [answer.lower()] + picks[:3]
        blanked = re.sub(re.escape(answer), "_____", s, count=1)
        items.append(
            {
                "text": f"Fill in the blank: {blanked}",
                "options": opts,
                "correct_index": 0,
                "explanation": f'The material states: "{s}"',
                "source_excerpt": s,
            }
        )
        if len(items) >= n:
            break
    if not items:
        raise QuizGenerationError("Could not build questions from this text. Try a longer or more descriptive passage.")
    return items


async def generate_quiz(
    text: str, num_questions: int, difficulty: str, competency: str, title: str
) -> Tuple[str, List[Dict[str, Any]]]:
    text = re.sub(r"[ \t]+", " ", text).strip()[:MAX_CHARS]
    engine, items = "heuristic", []
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            items = await _generate_with_claude(text, num_questions, difficulty)
            engine = "claude"
        except Exception:
            items = []
    if not items:
        engine = "heuristic"
        items = _generate_heuristic(text, num_questions)
    return engine, _normalise(items, engine, difficulty, competency, title)
