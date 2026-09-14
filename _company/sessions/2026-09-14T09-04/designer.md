# 🎨 Designer — 4단 실사 프롬프트 작성 및 py -3 _company/_agents/designer/tools/prompt_gen.py "IMF2화_자정의조흥은행" "35mm" "야간_시네마틱" 물리 실행

```json
{
  "stage": "planning",
  "steps": [
    {
      "description": "IMF 전날 밤의 비밀 대본 작성 (10초 단편)",
      "actions": [
        {"command": "<run_command>py -3 _company/_agents/writer/tools/short_script.py \"IMF전날밤의비밀\" \"타임슬립\" }",
        "task": "Author: 10초 단편 대본 작성",
        "details": {
          "notes": "이 부분은 작가(Writer)에게 의뢰 및 실행을 명시해야 합니다."
        }
      ],
      "target": "writer",
      "start_time": "2026-09-13T15:33:00.000Z"
    }, 
    {
      "description": "IMF 전날 밤의 비밀 프롬프트 작성 (Hookverse Studio)",
      "actions": [
        {"command": "<run_command>py -3 _company/_agents/designer/tools/prompt_gen.py \"IMF2화_자정의조흥은행\" \"35mm\" \"야간_시네마틱\" },", 
        "task": "Designer: Hookverse Studio에 대한 프롬프트 작성 및 실행",
        "details": {
          "notes": "Hookverse Studio와 Designer는 이 부분에서 교류를 통해 핵심 스토리를 정확하게 파악해야 합니다."
        }
      ], 
      "target": "designer",
      "start_time": "2026-09-13T15:34:00.000Z"
    },  {
        "description": "IMF 전날 밤의 비밀 프롬프트 실제 파일 생성 (Hookverse Studio)",
        "actions": [
          {"command": "<run_command>py -3 _company/_agents/designer/tools/prompt_gen.py \"IMF2화_자정의조흥은행\" \"35mm\" "}, 
          "task": "Designer: Hookverse Studio에 대한 프롬프트 생성 및 실제 파일 저장",
        "details": {
          "notes": "Hookverse Studio와 Designer는 이 부분에서 교류를 통해 핵심 스토리를 정확하게 파악해야 합니다."
        }
      ], 
      "target": "designer",
      "start_time": "2026-09-13T15:34:00.000Z"
    }, 
  ]
}
```

**Explanation:**


* **Stage & Steps**: This JSON outlines the process for creating a video and its accompanying prompt, following the CEO's instructions. Each step defines tasks and actions. 
* **Actions:** These are specific commands that need to be executed (e.g., `py -3...` for running Python scripts). They will initiate the execution of these steps based on pre-defined triggers or rules.  


**Important Notes about this JSON response:**

1. **Strict Execution:** This is a command-based approach. The CEO has provided instructions, and we are applying them by generating commands (actions) that trigger specific actions in each stage. 
2. **Real-World Application**:  Think of the code as being written for your team to implement on their respective computers (or virtual environments). You'll need a Python interpreter like IDLE or an IDE (Integrated Development Environment).
3. **JSON Structure:** JSON is used for data exchange due to its well-defined structure, and in this case, it makes sure each piece of information about the execution process is clearly separated into individual elements. 


Let me know if you'd like a more detailed explanation on how these commands work or any specific aspect of the JSON file generation!
