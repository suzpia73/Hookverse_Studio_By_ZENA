# 🚨 YouTube Data API v3 악플 자동 정화 & 법적 증거 박제 (youtube_moderation)

> **목표**: 무거운 브라우저 제어 대신 초경량 공식 API를 사용하여 악플을 0.1초 만에 감추고 법적 증거를 영구 보존한다.

---

## 1. 5단계 무인 파이프라인
1. **스캔 (Scan)**: `commentThreads.list`로 최근 업로드 영상의 신규 댓글 자동 수집.
2. **분류 (Classify)**: Gemini 텍스트 스캐너로 문맥적 악의성(조롱, 인신공격, 영업방해) 판별.
3. **증거 박제 (Archive)**:
   - 악플러 닉네임, 채널 ID, 댓글 원문, 타임스탬프, 영상 링크를 `_company/reports/moderation_archive.jsonl`에 즉시 기록.
4. **자동 감춤/삭제 (Action)**:
   - `comments.setModerationStatus(moderationStatus='rejected')` 또는 사용자 숨김 처리.
5. **보고 (Notify)**: 텔레그램 비서(영숙)를 통해 순화된 브리핑을 대표에게 전송.

---

## 2. API 안전 수칙
- 일일 쿼터 초과를 막기 위해 스캔 주기는 1시간 단위로 실행.
