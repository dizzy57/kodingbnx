#!/usr/bin/env python3

import json
import requests

limit = 3000

url = "https://leetcode.com/graphql/"
body = {
    "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ",
    "variables": {
        "categorySlug": "",
        "skip": 0,
        "limit": limit,
        "filters": {},
    },
}
headers = {
    "Content-Type": "application/json",
}

res = requests.get(url, headers=headers, json=body)
res.raise_for_status()

questions = res.json()["data"]["problemsetQuestionList"]["questions"]
urls_to_names = {
    f'https://leetcode.com/problems/{x["titleSlug"]}/': f'{x["title"]} ({x["difficulty"][0]})'.replace(
        "\n", " "
    )
    for x in questions
    if not x["paidOnly"]
}

with open("coding_tasks/static/coding_tasks/task_urls.js", "w") as f:
    f.write('"use strict";\nconst TASK_URLS_TO_NAMES = ')
    f.write(json.dumps(urls_to_names, indent=0))
    f.write("\n")
