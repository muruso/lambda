# -*- coding: utf-8 -*-
import os
import json
import logging
import datetime
import urllib.request

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_slack_event(slack_event: dict, context) -> str:

    logging.info(json.dumps(slack_event))

    if "challenge" in slack_event:
        return slack_event.get("challenge")

    if is_bot(slack_event) or not is_message_event(slack_event):
        return "OK"

    if is_template_request(slack_event):
        post_daily_report_template_to_slack_channnel(slack_event.get("event").get("channel"))
    else:
        post_daily_report_to_docbase(slack_event.get("event").get("text"), "tamurar", slack_event.get("event").get("channel"))
    return "OK"
    
def is_template_request(slack_event: dict) -> bool:
    return slack_event.get("event").get("text") == "#日報"

def is_bot(slack_event: dict) -> bool:
    return slack_event.get("event").get("subtype") == "bot_message"

def is_message_event(slack_event: dict) -> bool:
    return slack_event.get("event").get("type") == "message"

def post_message_to_slack_channel(message: str, channel: str):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "AUTHORIZATION_TOKEN"
    }
    data = {
        "token": "TOKEN",
        "channel": channel,
        "text": "提出完了!\n"+message,
        "username": "docbase"
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    urllib.request.urlopen(req)
    return

def post_daily_report_template_to_slack_channnel(channel: str):
    
    template = "## 本日の作業内容\n\n## 本日の作業時間\n\n## 発生した問題\n\n## 次の作業予定\n\n## 所感\n\n## 昨日の晩ごはん\n"

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "AUTHORIZATION_TOKEN"
    }
    data = {
        "token": "TOKEN",
        "channel": channel,
        "text": template,
        "username": "NAME"
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    urllib.request.urlopen(req)
    
    return


def post_daily_report_to_docbase(report: str, name: str, channel: str):
    
    today = datetime.datetime.now()
    today = today.strftime("%Y/%m/%d")
    
    scope = "group"
    groups = GROUP_ID

    url = "DOCBASE URL"
    headers = {
        "X-DocBaseToken": "DOCBASE_TOKEN",
        "Content-Type": "application/json"
    }
    data = {
        "title": "日報 "+name+" "+today,
        "body": report,
        "draft": True,
        "scope": scope,
        "notice": False,
        "groups": groups
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    with urllib.request.urlopen(req) as res:
        data = json.load(res).get("url")
        post_message_to_slack_channel(data, channel)

    
    return