# 💻 초경량 단일 웹앱 양산 & PayPal 인앱 결제 연동 (web_monetization)

> **목표**: 복잡한 빌드 도구 없이 단일 HTML 파일로 구동되는 수익화 웹앱(게임/사주)을 초고속으로 배포하고 PayPal 결제를 연동한다.

---

## 1. 2대 핵심 템플릿 아키텍처
1. **네온서바이버 (Neon Survivor Kit)**:
   - 44KB 단일 HTML/Canvas 뱀서라이크 게임.
   - 인게임 재화 구매 및 무기 업그레이드 시 PayPal 버튼 팝업 연동.
2. **도기 미스틱 (Doggie Mystic - 강아지 사주 AI)**:
   - 반려견 사진 및 생년월일 입력 ➡️ 사주/성격 분석 결과 리포트.
   - 1회 기본 무료 ➡️ "프리미엄 평생 사주 운세" PayPal 샌드박스 $2.99 결제 연동.

---

## 2. PayPal SDK 연동 표준 규칙
```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<div id="paypal-button-container"></div>
```
- 클라이언트 ID는 환경 설정에서 동적 주입.
- 결제 완료(onApprove) 시 즉시 잠금 해제 스크립트 실행.
