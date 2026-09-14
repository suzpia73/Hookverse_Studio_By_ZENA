# ✍️ Writer — IMF 전날 밤의 비밀 30초 대본 작성 및 py -3 _company/_agents/writer/tools/short_script.py "IMF전날밤의비밀" "타임슬립" 물리 실행

```json
{
  "stage": "planning",
  "steps": [
    {
      "description": "IMF 전날 밤의 비밀 대본 작성 (10초 단편)",
      "actions": [
        {"command": "<run_command>py -3 _company/_agents/writer/tools/short_script.py \"IMF전날밤의비밀\" \"타임슬립\" }",
        "task": "Author: 10초 단편 대본 작성" ,
        "details": {
          "notes": "이 부분은 작가(Writer)에게 의뢰 및 실행을 명시해야 합니다."
        }
      ],
      "target": "writer",
      "start_time": "2026-09-13T15:33:00.000Z", 
    }, 
    {
      "description": "IMF 전날 밤의 비밀 프롬프트 작성 (Hookverse Studio)",
      "actions": [
        {"command": "<run_command>py -3 _company/_agents/writer/tools/short_script.py \"IMF전날밤의비밀\" \"타임슬립\" },", 
        "task": "Author: Hookverse Studio에 대한 프롬프트 작성 및 실행",
        "details": {
          "notes": "Hookverse Studio와 작가(Writer)는 이 부분에서 교류를 통해 핵심 스토리를 정확하게 파악해야 합니다."
        }
      ], 
      "target": "writer",
      "start_time": "2026-09-13T15:33:00.000Z"
    },

  ]
}
```



