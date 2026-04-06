import math
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple


_COMMON_PASSWORDS = {
    "password",
    "password1",
    "p@ssw0rd",
    "123456",
    "123456789",
    "monkey",
    "dragon",
    "football",
    "baseball",
    "iloveyou",
    "welcome",
    "admin",
    "master",
}


_LOWER = "abcdefghijklmnopqrstuvwxyz"
_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_DIGITS = "0123456789"
# Approximate pool of common printable symbols.
_SYMBOLS = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""


def _char_class_counts(password: str) -> Tuple[int, Dict[str, bool]]:
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[^A-Za-z0-9]", password))
    flags = {
        "lower": has_lower,
        "upper": has_upper,
        "digit": has_digit,
        "symbol": has_symbol,
    }
    return sum(flags.values()), flags


def _detect_sequential_substring(password: str, min_run: int = 4) -> bool:
    """
    Detects simple ascending/descending runs like 'abcd'/'dcba' and '1234'/'4321'.
    This is intentionally conservative; it's heuristic feedback, not a security guarantee.
    """
    if len(password) < min_run:
        return False

    # Compare by consecutive code points.
    s = password
    for i in range(len(s) - min_run + 1):
        chunk = s[i : i + min_run]
        # Only consider chunks with consistent "step".
        deltas = [ord(chunk[j + 1]) - ord(chunk[j]) for j in range(len(chunk) - 1)]
        if all(d == 1 for d in deltas) or all(d == -1 for d in deltas):
            return True
    return False


def _has_triple_repeat(password: str) -> bool:
    # Example: 'aaa' or '111' or '!!!!'
    return bool(re.search(r"(.)\1\1", password))


def _common_password_penalty(password: str) -> int:
    p = password.strip().lower()
    if not p:
        return 0
    if p in _COMMON_PASSWORDS:
        return 35
    # Penalize common passwords appearing as a substring.
    for common in _COMMON_PASSWORDS:
        if common and common in p:
            return 18
    return 0


@dataclass(frozen=True)
class PasswordStrength:
    score: int  # 0..100
    label: str
    feedback: List[str]
    details: Dict[str, object]


def score_password(password: str) -> PasswordStrength:
    """
    Estimate password strength using a heuristic entropy model + rule-based penalties.
    Returns a score in [0, 100] with human-friendly feedback.
    """
    password = password or ""
    length = len(password)
    if length == 0:
        return PasswordStrength(score=0, label="Very Weak", feedback=["Enter a password to check."], details={})

    class_count, flags = _char_class_counts(password)

    # Build the effective character pool size.
    pool = 0
    if flags["lower"]:
        pool += len(_LOWER)
    if flags["upper"]:
        pool += len(_UPPER)
    if flags["digit"]:
        pool += len(_DIGITS)
    if flags["symbol"]:
        # We don't know the exact symbol set; approximate.
        pool += len(_SYMBOLS)

    # Entropy-ish estimate: log2(pool^length) = length * log2(pool).
    # If pool is tiny (e.g. only whitespace), keep it safe.
    pool = max(pool, 1)
    entropy_bits = length * math.log2(pool)

    # Map entropy to a 0..100 score.
    score = int(entropy_bits * 1.15)
    score = max(0, min(100, score))

    # Length-based adjustment.
    if length < 8:
        score = max(0, score - 25)
    elif length < 12:
        score = max(0, score - 8)
    elif length >= 16:
        score = min(100, score + 6)

    # Variety-based penalties.
    if class_count == 1:
        score = max(0, score - 22)
    elif class_count == 2:
        score = max(0, score - 10)
    elif class_count == 3:
        score = max(0, score - 4)

    # Pattern penalties.
    score -= _common_password_penalty(password)
    if _detect_sequential_substring(password):
        score = max(0, score - 14)
    if _has_triple_repeat(password):
        score = max(0, score - 10)

    # Final clamp.
    score = max(0, min(100, score))

    if score < 40:
        label = "Weak"
    elif score < 70:
        label = "Medium"
    elif score < 90:
        label = "Strong"
    else:
        label = "Very Strong"

    feedback: List[str] = []
    if length < 12:
        feedback.append("Increase length (aim for 12+ characters).")
    if class_count < 3:
        feedback.append("Add more character types (uppercase, digits, symbols).")
    if _common_password_penalty(password) > 0:
        feedback.append("Avoid common passwords and simple variations.")
    if _detect_sequential_substring(password):
        feedback.append("Avoid easy sequences like 'abcd' or '1234'.")
    if _has_triple_repeat(password):
        feedback.append("Avoid repeating the same character many times.")
    if not feedback:
        feedback.append("Nice. This password looks hard to guess.")

    return PasswordStrength(
        score=score,
        label=label,
        feedback=feedback,
        details={
            "length": length,
            "class_count": class_count,
            "effective_pool": pool,
            "estimated_entropy_bits": round(entropy_bits, 2),
        },
    )


def estimate_password_strength(password: str) -> Dict[str, object]:
    """
    Convenience wrapper returning a plain dict (useful for UI/JSON).
    """
    strength = score_password(password)
    return {
        "score": strength.score,
        "label": strength.label,
        "feedback": strength.feedback,
        "details": strength.details,
    }

