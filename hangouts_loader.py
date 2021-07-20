import json

import numpy as np
import pandas as pd
import datetime


def get_participants(conv):
    participants = {}
    for p in conv["conversation"]["participant_data"]:
        name = p.get("fallback_name", "unknown")
        pid = p["id"]["gaia_id"]
        participants[pid] = name
    return participants


def process_segments(segs):
    text = []
    for segment in segs:
        if segment["type"] in ["TEXT", "LINE_BREAK", "LINK"]:
            text.append(segment["text"])
        else:
            print(segs)
    return " ".join(text)


def make_payload_for_standard_chat(event, participants):
    segs = event["chat_message"]["message_content"]["segment"]
    name = participants.get(event["sender_id"]["gaia_id"], "unknown")
    return {
        "sender_name": name,
        "timestamp_ms": int(event["timestamp"]) / 1000,
        "content": process_segments(segs),
        "platform": "Hangouts",
        "type": "Generic",
        "is_unsent": False,
    }


def make_payload_for_attachment(event, participants):
    url = event["chat_message"]["message_content"]["attachment"][0].get("url", "")
    name = participants.get(event["sender_id"]["gaia_id"], "unknown")
    return {
        "sender_name": name,
        "timestamp_ms": int(event["timestamp"]) / 1000,
        "share": {"link": url},
        "content": url,
        "type": "Share",
        "is_unsent": False,
        "platform": "Hangouts",
    }


def make_payload_for_hangout_event(event, participants):
    name = participants.get(event["sender_id"]["gaia_id"], "unknown")
    return {
        "content": np.nan,
        "timestamp_ms": int(event["timestamp"]) / 1000,
        "sender_name": name,
        "platform": "Hangouts",
        "type": "Call",
        "event_id": "event_id",
        "is_unsent": False,
    }


def reformat_payload(participants, event):
    if event.get("chat_message") and event["chat_message"]["message_content"].get(
        "segment"
    ):
        payload = make_payload_for_standard_chat(event, participants)
    elif event.get("chat_message") and event["chat_message"]["message_content"].get(
        "attachment"
    ):
        payload = make_payload_for_attachment(event, participants)
    elif event.get("hangout_event"):
        payload = make_payload_for_hangout_event(event, participants)
    return payload


def to_datetime(ts):
    return datetime.datetime.fromtimestamp(float(ts) / 1000)


def get_message_length(message):
    if type(message) is str:
        return len(message)
    else:
        return len(str(message))


def load_hangouts(filename="Hangouts.json"):
    with open(filename, encoding="utf-8") as h:
        the_json = json.load(h)

    messages = []

    for conversation in the_json["conversations"]:
        ev = conversation["events"]
        conv = conversation["conversation"]
        participants = get_participants(conv)

        for event in ev:
            try:
                payload = reformat_payload(participants, event)
                messages.append(payload)
            except Exception as error:
                # print("error:\n", error, event, "\n")
                pass

    df = pd.DataFrame(messages)

    df["datetime"] = df.timestamp_ms.apply(to_datetime)
    df["message_length"] = df.content.apply(get_message_length)
    return df


if __name__ == "__main__":
    print(load_hangouts().shape)
