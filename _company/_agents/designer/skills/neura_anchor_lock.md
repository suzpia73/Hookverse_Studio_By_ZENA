# 👑 뉴라(NEURA) G3 안면 앵커락 & Anti-AI 실사화 프롬프트 룰 (neura_anchor_lock)

> **목표**: 안면 일관성 100% 고정 및 AI 티가 전혀 나지 않는 극사실 포토그래피 프롬프트 산출.

---

## 1. 앵커락(Anchor Lock) 필수 키셋
뉴라가 등장하는 모든 프롬프트에는 아래 키셋을 100% 강제 삽입한다:
- `Korean woman in her early 20s, elegant and sharp gaze, natural black long wavy hair`
- **시그니처 매력점**: `a distinct beauty mark under her right jawline`
- **표정 및 앵글**: 장면에 맞게 `front view / 45-degree angle / close-up profile` 명시

---

## 2. Anti-AI 실사화 4대 수칙
1. **피부 질감**: `subtle skin pores, natural facial texture, delicate peach fuzz, slight skin imperfections` (도자기 인형 피부 금지).
2. **카메라/렌즈**: `35mm or 85mm DSLR lens, shallow depth of field, natural bokeh, 8k resolution candid snapshot`.
3. **조명**: `cinematic street lighting, tungsten night street lamp, neon reflection on wet pavement`.
4. **산출물 저장**: 반드시 `assets/prompts/` 폴더에 `.txt` 파일로 물리적 저장.
