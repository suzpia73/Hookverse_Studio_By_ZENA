# 🎵 루나 스킬 라이브러리 — 사운드 감독

_재사용 가능한 패턴 모음. `memory.md`는 모든 활동의 로그(append-only firehose),
이 폴더는 **검증된 패턴만 골라낸 것**입니다. 각 `*.md` 파일은 다음 호출 시
루나의 system prompt에 자동 주입됩니다._

---

## 📌 어떤 스킬을 여기에 담나요?

루나(Editor)는 **BGM 생성·사운드 편집·영상 음향 연출** 전문가입니다. 다음 유형의 패턴을 저장하세요:

| 파일명 | 담을 내용 |
|---|---|
| `bgm_library.md` | 영상 톤별 BGM 레퍼런스 (장르·BPM·분위기·링크) |
| `mood_to_music.md` | 영상 키워드 → 음악 스타일 매핑 차트 |
| `audio_workflow.md` | BGM 생성 → 편집 → 합성 표준 워크플로우 |
| `signature_sound.md` | 채널 오프닝/엔딩 BGM 규격 및 사용 규칙 |
| `loop_fade_pattern.md` | 영상 길이별 loop/fade 자동 결정 공식 |

---

## 💡 루나 스킬의 핵심 기준

> **\"막연한 '신나는 곡' X — 장르·BPM·길이 명시\"**

스킬 파일에는 다음이 반드시 포함되어야 합니다:
1. **장르** — lo-fi hip hop, cinematic orchestral, ambient electronic 등 구체 명칭
2. **BPM 범위** — 예: 75~85 BPM (몽환적 집중 분위기)
3. **영상 길이 매핑** — 30초 쇼츠 vs 10분 롱폼 vs 60초 릴스 각각 구분
4. **도구/소스** — Suno AI, Udio, Pixabay, 직접 생성 등 명시

---

## 어떻게 채우나요?
- 텔레그램에서 `/skill` (직전 산출물 자동 승격)
- VS Code 명령 팔레트: `Connect AI: 방금 산출물 → 스킬로 저장`
- 직접 이 폴더에 `<주제>.md` 파일을 만들어도 됩니다 (`# 제목` + 본문)

`README.md` 자체는 system prompt에 주입되지 않습니다.
