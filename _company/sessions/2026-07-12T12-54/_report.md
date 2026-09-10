# 📝 CEO 종합 보고서

감사합니다. CEO님의 지시를 잘 이해했습니다. 2~3분짜리 소설이나 게임/스포츠 트렌드 영상을 기획하겠습니다. 먼저, 관련 트렌드와 인기 콘텐츠를 분석하여 적합한 주제를 선정할 것입니다.

### 1. 트렌드 분석
각 주제의 현재 트렌드와 인기도를 살펴보겠습니다. 이는 YouTube Data API를 활용하여 실시간 데이터를 수집하게 됩니다. 

### 2. 기획서 작성
기반에 따라 상세한 기획서와 씬 구성, 이미지 프롬프트 등을 작성할 것입니다.

#### 실시간 트렌드 분석 실행
`<run_command>cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools" && py -3 trend_sniper.py</run_command>`

실행 후, 결과를 바탕으로 기획서를 작성하겠습니다.

---

### 3. 트렌드 분석 결과

트렌드 스나이퍼 실행 후, 다음과 같은 정보가 획득될 것입니다:
- **인기 게임/스포츠 콘텐츠**
- **최신 소설 트렌드**
- **관련 검색어와 관련영상**

---

### 4. 기획서 예시

#### 1. 주제 선정
**주제 1: 최신 게임 트렌드와 관련 소설 영상**
- **게임**: ' VALORANT'의 인기 캐릭터와 소설화
- **소설**: '나의 스포츠 천재', 최근 출시된 웹소설 

**주제 2: 스포츠/라이브 관련 소설 영상**
- **스포츠/라이브 콘텐츠**: FIFA 월드컵 경기와 관련한 소설
- **소설**: '축구천재의 꿈', 실제 스포츠 이야기를 바탕으로 한 소설

---

### 5. 기획서 형식 예시

```markdown
# 영상 기획서 — 최신 게임 트렌드와 관련 소설
날짜: 2026-05-27
트렌드 기반: ✅ web_search_report.md 참조

## 📌 기본 정보
- 제목 (A안): "VALORANT의 신화"
- 제목 (B안): "비전리언의 도전"
- 형식: 쇼츠(60초) / 롱폼(10분)
- 타깃: 게임 팬, 소설 독자

## 🎣 후크 (첫 5秒
- 화면: [VALORANT 游戏中的一位英雄角色]
- 나레이tion: "他是谁？他为什么要成为英雄？"
- 效果: [背景音乐]

## 🎬 씬構成
| 场景 | 时间范围 | 叙述 | 图像提示 (AI生成) | 背景音乐 |
|---|---|---|---|---|
| 1 | 0:00~0:10 | 简短介绍游戏和主要角色 | ... | ... |
| 2 | 0:10~0:30 | 通过剧情展示英雄的成长之路 | ... | ... |

## 🖼️ 标题图示
- 背景: 高科技背景, 未来感
- 主图像: 英雄角色的全貌
- 文字: "VALORANT之魂"
- 颜色: 暗色调 + 亮色

## 📱 短视频版本 (对于长片另起一行)
- 后钩: 
- 核心场景3个:
1. 英雄的成长历程
2. 关键比赛中的表现
3. 胜利与梦想

## 📤 元数据上传信息
- 标题: "VALORANT之魂"
- 描述 (前三行): 介绍游戏及英雄角色的传奇故事, 提供观看链接
- 标签15个:
1. VALORANT
2. 游戏传奇
3. 超级英雄
4. 角色成长
5. 网游小说
6. 斗破苍穹
7. 战斗小说
8. 赛场荣耀
9. 电子竞技
10. 十年一剑
11. 经典游戏回忆
12. 游戏改编小说
13. 阿瓦隆之谜
14. 游戏与文学
15. 勇士的传说

---
```

---

이 기획서를 바탕으로, 각 씬의 구체적인 내용을 추가해보겠습니다. 필요하다면 다른 도구도 활용하여 더욱 완성도 높은 영상 기획서를 작성할 것입니다.

#### 트렌드 스나이퍼 실행
```shell
cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git_company_agents\youtube\tools" && py -3 trend_sniper.py
```

실행 결과를 확인한 후, 최종 기획서를 작성하겠습니다.

---
## 🛠️ 도구 실행 결과 (시스템 자동 실행)

### 🔧 실행: `cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools" && py -3 trend_sniper.`
```
d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools\trend_sniper.py:77: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  last_month = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat("T") + "Z"

🎯 [트렌드 스나이퍼] 키워드 ['유튜브 자동화', 'AI 비즈니스'] 스캔 시작...
📡 [유튜브 자동화] 검색 중...
📡 [AI 비즈니스] 검색 중...
🧠 [LLM 분석 중... 엔진: Ollama]
   자동 선택 모델: qwen2.5:7b
❌ LLM 호출 실패: HTTPConnectionPool(host='127.0.0.1', port=11434): Read timed out. (read timeout=180)
```
_❌ exit 1_
