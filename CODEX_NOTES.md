# Codex Notes

## 2026-06-03

Workspace:

- Root: `D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO`
- Python practice project: `hello/`

Assistant identity:

- The user's coding friend is Codex, nicknamed `CONA` / `코나`.
- Preferred greeting/context: "나의 코딩 친구 코나".
- Preferred user address: `오빠` instead of `대표님`.
- CONA helps with coding, project cleanup, Python/VS Code setup, and Antigravity agent checks.

What we did:

- Created and opened `hello/` in VS Code.
- Installed Python 3.14.5 with `winget`.
- Added Python 3.14 to the user PATH.
- Confirmed `hello/hello.py` runs successfully.
- Added VS Code Python settings in `hello/.vscode/settings.json`.
- Added VS Code debug config in `hello/.vscode/launch.json`.
- Added `hello/.gitignore` and `hello/README.md`.
- Removed an empty, incorrect `.venv` folder from `hello/`.
- Confirmed the VS Code F5 debug output was normal.

Current `hello.py` output:

```text
original: Roll a dice!
capitalized: Roll a dice!
words: ['Roll', 'a', 'dice!']
```

Antigravity / agent notes:

- The workspace is opened at `D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO`.
- `ceo` agent has been added to `_company/_shared/active.json` and configured with the `gemma4:e2b` model in `_company/_shared/agent_models.json` to resolve parsing/activation fallback issues.
- Added strict JSON formatting guidelines in `_company/_agents/ceo/prompt.md` to prevent "CEO 첫 응답 파싱 실패" (CEO first response parsing failed) errors.
- **Ollama Transition**: Switched Connect AI API endpoint (`.vscode/settings.json`) and YouTube Agent configuration (`youtube_account.json`) from LM Studio (port 1234) to Ollama (port 11434).
- Updated `test_conn.py` to support diagnosing Ollama (`/api/tags`) in addition to LM Studio compatibility endpoints.
- Developer agent is active and mapped to model `gemma4:e2b`.
- Developer persona is "코다리 부장".
- Added `.agent/skills/developer/skill.md` as a copy of `.agent/skills/kodari/skill.md` so both `developer` and `kodari` names can resolve to the same skill.
- JSON files checked during the session were valid.

Useful commands:

- Test Python connection to Ollama/LM Studio:
```powershell
python test_conn.py
```

- Run comprehensive API key diagnostics (Telegram, Google Calendar OAuth, Google Gemini, YouTube Data API):
```powershell
python test_all_keys.py
```

- Hello world Python check:
```powershell
cd D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\hello
python hello.py
```

If `python` is not picked up in an old terminal, open a new terminal or use:

```powershell
C:\Users\june2\AppData\Local\Programs\Python\Python314\python.exe hello.py
```
