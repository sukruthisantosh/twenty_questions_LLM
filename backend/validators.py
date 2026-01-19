"""Minimal response validation utilities."""
import re


def validate_yes_no(answer):
    """Normalize yes/no answer to "yes" or "no".
    
    Returns:
        str: "yes" or "no", defaults to "no" if unclear
    """
    if not answer:
        return "no"
    
    answer = answer.strip().lower()
    
    if answer.startswith("yes") or answer.startswith("y"):
        return "yes"
    
    return "no"


def validate_guess(guess):
    """Extract object name from guess, removing common prefixes.
    
    Returns:
        str: Cleaned guess, or original if cleaning fails
    """
    if not guess:
        return None
    
    guess = guess.strip()
    
    patterns_to_remove = [
        r"^i (think|guess|believe) (it'?s |that it'?s )?",
        r"^it'?s (probably |maybe )?",
        r"^the (object|answer|thing) (is |might be )?",
        r"^(my guess is |i would say )",
        r"^is it (a |an )?",
        r"^could it be (a |an )?",
        r"\.$",
        r"\?$",
    ]
    
    cleaned = guess
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    
    cleaned = cleaned.strip()
    
    return cleaned if cleaned else guess

