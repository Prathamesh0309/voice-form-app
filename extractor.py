import re


AUDIO_FILE = "meeting.wav"
EXCEL_FILE = "meeting_actions.xlsx"
RECORD_SECONDS = 15
SAMPLE_RATE = 16000


def extract_email(text):
    match = re.search(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        text
    )
    return match.group(0) if match else None

NUM_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3",
    "four": "4", "five": "5", "six": "6",
    "seven": "7", "eight": "8", "nine": "9"
}
MULTIPLIERS = {
    "double": 2,
    "triple": 3
}

def normalize_phone(text):
    tokens = text.lower().split()
    digits = []
    digit_count = 0
    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "double nine", "triple five"
        if token in MULTIPLIERS:
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]

                if next_token.isdigit():
                    digits.extend(next_token * MULTIPLIERS[token])
                    i += 2
                    digit_count += MULTIPLIERS[token]
                    continue

                if next_token in NUM_WORDS:
                    digits.extend(NUM_WORDS[next_token] * MULTIPLIERS[token])
                    i += 2
                    digit_count += MULTIPLIERS[token]
                    continue

            # Invalid pattern → skip safely
            i += 1
            continue

        # Normal digit
        if token.isdigit():
            digits.append(token)
            digit_count += 1
        elif token in NUM_WORDS:
            digits.append(NUM_WORDS[token])
            digit_count += 1

        i += 1
        if digit_count >= 10:
            break    
    phone = "".join(digits)

    # Safety check
    if len(phone) <= 10:
        return phone
    return None

def extract_pan(text):
    match = re.search(
        r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
        text.upper()
    )
    return match.group(0) if match else None

def extract_name(text):
    match = re.search(
        r'(my name is|i am|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        text,
        re.IGNORECASE
    )

    if not match:
        return None, None

    full_name = match.group(2)
    parts = full_name.split()

    first_name = parts[0]
    last_name = " ".join(parts[1:])

    return first_name, last_name

def extract_address(text):
    match = re.search(
        r'(address is|i live at|located at)\s+(.+)',
        text,
        re.IGNORECASE
    )
    return match.group(2).strip() if match else None

def extract_form_fields(text):
    data = {}
    confidence = {}
    needs_review = []

    email = extract_email(text)
    phone = normalize_phone(text)
    pan = extract_pan(text)
    first, last = extract_name(text)
    address = extract_address(text)

    data["first_name"] = first
    data["last_name"] = last
    data["email"] = email
    data["phone"] = phone
    data["pan"] = pan
    data["address"] = address

    confidence["email"] = 0.95 if email else 0.0
    confidence["phone"] = 0.85 if phone else 0.0
    confidence["pan"] = 0.98 if pan else 0.0
    confidence["name"] = 0.7 if first else 0.0
    confidence["address"] = 0.6 if address else 0.0

    for field, score in confidence.items():
        if score < 0.75:
            needs_review.append(field)

    return {
        "data": data,
        "confidence": confidence,
        "needs_review": needs_review
    }

