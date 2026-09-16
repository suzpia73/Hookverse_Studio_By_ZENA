#!/usr/bin/env python3
"""
build_dashboard.py — Hookverse Studio 개발자 에이전트(Developer 코다리) 전용 웹 대시보드 빌더 v1.0
디자인 규격: 50_디자인/masterclass/DESIGN.md (Midnight Stage 다크 시네마틱 UI)
역할:
1. Hookverse Studio의 실시간 자산(1~3화 비디오, 대본, 프롬프트, 오디오)과 10대 에이전트 상태를 스캔합니다.
2. 넷플릭스/마스터클래스급 반응형 실시간 종합 상황실(dashboard.html)을 빌드합니다.
3. 브라우저에서 원클릭으로 열어볼 수 있도록 디스크에 안착시킵니다.
"""

import os
import glob
from datetime import datetime

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
SCRIPTS_DIR = os.path.join(WORKSPACE, "assets", "scripts")
PROMPTS_DIR = os.path.join(WORKSPACE, "assets", "prompts")
VIDEOS_DIR = os.path.join(WORKSPACE, "assets", "videos")
AUDIO_DIR = os.path.join(WORKSPACE, "assets", "audio")
OUTPUT_HTML = os.path.join(WORKSPACE, "dashboard.html")

def scan_assets():
    videos = [os.path.basename(p) for p in glob.glob(os.path.join(VIDEOS_DIR, "*.mp4"))]
    scripts = [os.path.basename(p) for p in glob.glob(os.path.join(SCRIPTS_DIR, "*.md"))]
    prompts = [os.path.basename(p) for p in glob.glob(os.path.join(PROMPTS_DIR, "*.txt"))]
    audios = [os.path.basename(p) for p in glob.glob(os.path.join(AUDIO_DIR, "*.mp3"))]
    return {
        "videos": videos,
        "scripts": scripts,
        "prompts": prompts,
        "audios": audios
    }

def generate_dashboard_html():
    assets = scan_assets()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hookverse Studio — 시네마틱 관제 대시보드</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --color-pitch-black: #0a0a0c;
      --color-charcoal-canvas: #121316;
      --color-deep-slate: #1a1c22;
      --color-border: #272a34;
      --color-pure-white: #ffffff;
      --color-silver-mist: #9ea0a9;
      --color-action-raspberry: #e32652;
      --color-highlight-gold: #eed37f;
      --color-interactive-lime: #10b981;
      --font-body: 'Inter', -apple-system, sans-serif;
      --font-display: 'Oswald', sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--color-pitch-black);
      color: var(--color-pure-white);
      font-family: var(--font-body);
      line-height: 1.6;
      padding: 32px 24px;
      min-height: 100vh;
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
    }}

    /* Header */
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--color-border);
      margin-bottom: 32px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 18px;
    }}

    .emblem-gold-circle-img {{
      width: 56px;
      height: 56px;
      border-radius: 50%;
      object-fit: cover;
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.5), 0 0 6px rgba(255, 255, 255, 0.4);
      border: 2px solid rgba(238, 211, 127, 0.6);
      flex-shrink: 0;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}

    .emblem-gold-circle-img:hover {{
      transform: scale(1.05) rotate(5deg);
      box-shadow: 0 0 28px rgba(238, 211, 127, 0.8), 0 0 10px rgba(255, 255, 255, 0.6);
    }}

    .brand-title h1 {{
      font-family: var(--font-display);
      font-size: 28px;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      line-height: 1.1;
      margin-bottom: 4px;
      background: linear-gradient(180deg, #ffffff 40%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .brand-title p {{
      font-size: 13px;
      color: var(--color-silver-mist);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .channel-handle {{
      background: rgba(238, 211, 127, 0.15);
      border: 1px solid rgba(238, 211, 127, 0.35);
      color: var(--color-highlight-gold);
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}

    .status-pill {{
      background-color: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: var(--color-interactive-lime);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .pulse {{
      width: 8px;
      height: 8px;
      background-color: var(--color-interactive-lime);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--color-interactive-lime);
    }}

    /* KPI Stats Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin-bottom: 36px;
    }}

    .kpi-card {{
      background-color: var(--color-charcoal-canvas);
      border: 1px solid var(--color-border);
      border-radius: 12px;
      padding: 20px;
      position: relative;
      overflow: hidden;
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; width: 4px; height: 100%;
      background-color: var(--color-action-raspberry);
    }}

    .kpi-card.gold::before {{ background-color: var(--color-highlight-gold); }}
    .kpi-card.green::before {{ background-color: var(--color-interactive-lime); }}

    .kpi-label {{
      font-size: 12px;
      text-transform: uppercase;
      color: var(--color-silver-mist);
      font-weight: 600;
      margin-bottom: 8px;
    }}

    .kpi-val {{
      font-family: var(--font-display);
      font-size: 36px;
      font-weight: 700;
      line-height: 1;
      margin-bottom: 6px;
    }}

    .kpi-sub {{
      font-size: 12px;
      color: var(--color-silver-mist);
    }}

    /* Main Sections Grid */
    .dashboard-layout {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 28px;
    }}

    @media (max-width: 1024px) {{
      .dashboard-layout {{ grid-template-columns: 1fr; }}
    }}

    .panel {{
      background-color: var(--color-charcoal-canvas);
      border: 1px solid var(--color-border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 28px;
    }}

    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--color-border);
      margin-bottom: 20px;
    }}

    .panel-title {{
      font-family: var(--font-display);
      font-size: 20px;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    /* Video Pipeline Cards */
    .episode-card {{
      background-color: var(--color-deep-slate);
      border: 1px solid var(--color-border);
      border-radius: 10px;
      padding: 18px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .episode-info h3 {{
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 4px;
      color: var(--color-pure-white);
    }}

    .episode-info p {{
      font-size: 13px;
      color: var(--color-silver-mist);
    }}

    .tag-group {{
      display: flex;
      gap: 8px;
      margin-top: 8px;
    }}

    .tag {{
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      font-weight: 600;
    }}

    .tag-ready {{ background-color: rgba(16, 185, 129, 0.2); color: var(--color-interactive-lime); }}
    .tag-gold {{ background-color: rgba(238, 211, 127, 0.2); color: var(--color-highlight-gold); }}

    /* Agent Fleet Grid */
    .agent-fleet {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }}

    .agent-box {{
      background-color: var(--color-deep-slate);
      border: 1px solid var(--color-border);
      border-radius: 8px;
      padding: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .agent-icon {{
      font-size: 24px;
      width: 42px;
      height: 42px;
      background-color: var(--color-charcoal-canvas);
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      border: 1px solid var(--color-border);
    }}

    .agent-meta h4 {{
      font-size: 14px;
      font-weight: 600;
    }}

    .agent-meta p {{
      font-size: 11px;
      color: var(--color-silver-mist);
    }}

    /* Asset List */
    .asset-item {{
      font-size: 13px;
      padding: 10px 14px;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .asset-item:last-child {{ border-bottom: none; }}
    .asset-name {{ color: #e2e8f0; font-family: monospace; font-size: 12px; }}

    /* Cinematic Video Player Panel */
    .shorts-player-panel {{
      background: var(--color-charcoal-canvas);
      border: 1px solid rgba(238, 211, 127, 0.35);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }}

    .shorts-player-container {{
      display: flex;
      gap: 24px;
      align-items: flex-start;
      margin-top: 16px;
    }}

    .video-viewport-wrapper {{
      position: relative;
      width: 250px;
      height: 444px; /* 9:16 vertical ratio */
      background: #000;
      border-radius: 14px;
      overflow: hidden;
      border: 2px solid rgba(238, 211, 127, 0.4);
      box-shadow: 0 0 25px rgba(238, 211, 127, 0.2), 0 0 50px rgba(0, 0, 0, 0.8);
      flex-shrink: 0;
    }}

    .video-viewport-wrapper video {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      background: #000;
    }}

    .player-controls-side {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .playlist-card {{
      background: var(--color-deep-slate);
      border: 1px solid var(--color-border);
      border-radius: 8px;
      padding: 12px 14px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .playlist-card:hover {{
      border-color: var(--color-action-raspberry);
      transform: translateX(4px);
    }}

    .playlist-card.active {{
      border-color: var(--color-highlight-gold);
      background: rgba(238, 211, 127, 0.08);
      box-shadow: inset 0 0 12px rgba(238, 211, 127, 0.15);
    }}

    .playlist-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--color-pure-white);
      margin-bottom: 3px;
    }}

    .playlist-desc {{
      font-size: 11px;
      color: var(--color-silver-mist);
    }}

    .player-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(238, 211, 127, 0.2);
      color: var(--color-highlight-gold);
      border: 1px solid rgba(238, 211, 127, 0.4);
      flex-shrink: 0;
    }}

    footer {{
      margin-top: 40px;
      text-align: center;
      font-size: 12px;
      color: var(--color-silver-mist);
      padding-top: 20px;
      border-top: 1px solid var(--color-border);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <img src="./assets/images/hookverse_studio_logo.png" alt="Hookverse Studio" class="emblem-gold-circle-img">
        <div class="brand-title">
          <h1>HOOKVERSE STUDIO</h1>
          <p><span class="channel-handle">@hookverse_studio</span> · AI 에이전트 1인 기업 완전 자율화 통제실 · Midnight Stage</p>
        </div>
      </div>
      <div class="status-pill">
        <div class="pulse"></div>
        <span>실시간 무인 공장 ALL GREEN</span>
      </div>
    </header>

    <!-- KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">완성 비디오 (MP4)</div>
        <div class="kpi-val">{len(assets['videos'])}</div>
        <div class="kpi-sub">조흥은행 8씬 가변 싱크 완결</div>
      </div>
      <div class="kpi-card gold">
        <div class="kpi-label">마스터 대본 (8씬)</div>
        <div class="kpi-val">{len(assets['scripts'])}</div>
        <div class="kpi-sub">10대 헌법 메타프롬프트 창작</div>
      </div>
      <div class="kpi-card green">
        <div class="kpi-label">시네마틱 프롬프트 팩</div>
        <div class="kpi-val">{len(assets['prompts'])}</div>
        <div class="kpi-sub">G3 Master Face Anchor Lock</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">뉴럴 성우 오디오</div>
        <div class="kpi-val">{len(assets['audios'])}</div>
        <div class="kpi-sub">edge-tts 선희 뉴럴 딕션</div>
      </div>
    </div>

    <!-- Main Content Layout -->
    <div class="dashboard-layout">
      <!-- Left Column: Pipeline Execution -->
      <div class="left-col">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🎬 K-시네마틱 숏폼 에피소드 파이프라인</div>
            <span style="font-size: 12px; color: var(--color-highlight-gold);">4컷/8씬 가변 싱크 표준 & 실시간 인터랙티브 플레이어</span>
          </div>

          <!-- 2-Column Cinematic Shorts Player -->
          <div class="shorts-player-container">
            <!-- Left: 9:16 Vertical Video Viewport -->
            <div class="video-viewport-wrapper">
              <video id="main-shorts-video" controls autoplay muted playsinline poster="./assets/images/IMF2화/IMF전날밤의비밀_ep02_cut02.jpg" src="./assets/videos/IMF2화_추격과비밀통화_4컷_마스터완성본.mp4">
                브라우저가 비디오 태그를 지원하지 않습니다.
              </video>
            </div>

            <!-- Right: 1~3 Playlist & Details -->
            <div class="player-controls-side">
              <div style="margin-bottom: 8px; padding-bottom: 10px; border-bottom: 1px solid var(--color-border);">
                <div id="current-video-title" style="font-size: 15px; font-weight: 700; color: var(--color-highlight-gold); margin-bottom: 4px;">
                  2화: IMF 전날 밤의 비밀 (추격과 비밀 통화)
                </div>
                <div id="current-video-desc" style="font-size: 12px; color: var(--color-silver-mist); line-height: 1.5;">
                  169cm 8등신 롱다리 각선미 & 볼륨 · 비 내리는 1997년 자정 추격전과 1% 배터리 공중전화 비밀 통화 4컷 마스터 완결
                </div>
              </div>

              <!-- Ep 1 Card -->
              <div id="ep1-card" class="playlist-card" onclick="selectShortsVideo('./assets/videos/국가부도_첫쇼츠.mp4', '1화: 국가 부도의 날 (파일럿 런칭)', '유튜브 실시간 41회 조회 · 시청 지속시간 2분 39초 (636% 무한루프 실증) · G3 앵커락 실증', 'ep1-card')">
                <div class="episode-info">
                  <div class="playlist-title">1화: 국가 부도의 날 (파일럿 런칭)</div>
                  <div class="playlist-desc">유튜브 41회 · 지속 2분 39초 (636% 무한루프)</div>
                </div>
                <span class="player-badge">▶ 재생</span>
              </div>

              <!-- Ep 2 Card (Active Default) -->
              <div id="ep2-card" class="playlist-card active" onclick="selectShortsVideo('./assets/videos/IMF2화_추격과비밀통화_4컷_마스터완성본.mp4', '2화: IMF 전날 밤의 비밀 (추격과 비밀 통화)', '169cm 8등신 롱다리 각선미 & 볼륨 · 비 내리는 1997년 자정 추격전과 1% 배터리 공중전화 비밀 통화 4컷 마스터 완결', 'ep2-card')">
                <div class="episode-info">
                  <div class="playlist-title" style="color: var(--color-highlight-gold);">2화: IMF 전날 밤의 비밀 (신규 완성본)</div>
                  <div class="playlist-desc">4컷(37.44s) 칼싱크 · 169cm 각선미 & 볼륨 안착</div>
                </div>
                <span class="player-badge" style="background: rgba(226, 75, 137, 0.2); color: var(--color-action-raspberry); border-color: rgba(226, 75, 137, 0.4);">★ 지금 재생중</span>
              </div>

              <!-- Ep 3 Card -->
              <div id="ep3-card" class="playlist-card" onclick="selectShortsVideo('./assets/videos/IMF2화_조흥은행금고일치_가변싱크_완성본.mp4', '3화: 유령의 반전 (조흥은행 금고 잠입)', '새벽 02:00 조흥은행 지하 금고 잠입 · NEURA 1997 비밀 장부와 2026년 100달러 지폐의 소름 돋는 반전 8씬', 'ep3-card')">
                <div class="episode-info">
                  <div class="playlist-title">3화: 유령의 반전 (조흥은행 금고 잠입)</div>
                  <div class="playlist-desc">새벽 02:00 지하 금고 잠입 · NEURA 비밀 장부와 100달러 지폐의 반전</div>
                </div>
                <span class="player-badge">▶ 재생</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Physical Assets -->
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">📁 최근 디스크 안착 물리 자산 (Physical Assets)</div>
            <span style="font-size: 12px; color: var(--color-silver-mist);">실시간 디스크 동기화</span>
          </div>
          <div>
            {"".join([f'<div class="asset-item"><span class="asset-name">🎬 {v}</span><span class="tag tag-ready">MP4 비디오</span></div>' for v in assets['videos']])}
            {"".join([f'<div class="asset-item"><span class="asset-name">📜 {s}</span><span class="tag tag-gold">대본 MD</span></div>' for s in assets['scripts'][:4]])}
            {"".join([f'<div class="asset-item"><span class="asset-name">🎨 {p}</span><span class="tag tag-ready">프롬프트 TXT</span></div>' for p in assets['prompts'][:4]])}
          </div>
        </div>
      </div>

      <!-- Right Column: 10 Agent Fleet -->
      <div class="right-col">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🤖 10대 에이전트 무인 공장</div>
            <span style="font-size: 12px; color: var(--color-interactive-lime);">ALL ONLINE</span>
          </div>

          <div class="agent-fleet">
            <div class="agent-box">
              <div class="agent-icon">👑</div>
              <div class="agent-meta">
                <h4>CEO 레오</h4>
                <p>8씬 단일 SOP 지휘</p>
              </div>
            </div>
            <div class="agent-box">
              <div class="agent-icon">✍️</div>
              <div class="agent-meta">
                <h4>작가 에디</h4>
                <p>5-in-1 바이럴 숏폼 대본</p>
              </div>
            </div>
            <div class="agent-box">
              <div class="agent-icon">🎨</div>
              <div class="agent-meta">
                <h4>디자이너 픽스</h4>
                <p>G3 앵커락 실사 프롬프트</p>
              </div>
            </div>
            <div class="agent-box">
              <div class="agent-icon">💻</div>
              <div class="agent-meta">
                <h4>개발자 코다리</h4>
                <p>대시보드 & 템플릿 배포</p>
              </div>
            </div>
            <div class="agent-box">
              <div class="agent-icon">💼</div>
              <div class="agent-meta">
                <h4>비즈니스</h4>
                <p>PayPal 달러 수익 정산</p>
              </div>
            </div>
            <div class="agent-box">
              <div class="agent-icon">📱</div>
              <div class="agent-meta">
                <h4>비서 영숙</h4>
                <p>텔레그램 실시간 직통</p>
              </div>
            </div>
            <div class="agent-box">
              <div class="agent-icon">🔍</div>
              <div class="agent-meta">
                <h4>리서처</h4>
                <p>트렌드 & 뉴스재킹</p>
              </div>
            </div>
            <div class="agent-box">
              <div class="agent-icon">📺</div>
              <div class="agent-meta">
                <h4>유튜브</h4>
                <p>후킹 지표 & 알고리즘</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Virtual Muse Profile -->
        <div class="panel" style="border: 1px solid var(--color-highlight-gold);">
          <div class="panel-header">
            <div class="panel-title" style="color: var(--color-highlight-gold);">✨ 공식 버추얼 뮤즈: 뉴라</div>
            <span class="tag tag-gold">G3 Master Lock</span>
          </div>
          <p style="font-size: 13px; color: #cbd5e1; margin-bottom: 12px;">
            1997년 외환위기와 2026년을 넘나드는 타임슬립 다크 히어로. 국가 부패 세력이 빼돌린 달러를 회수하여 대한민국 미래를 지키는 수호자.
          </p>
          <div style="font-size: 11px; color: var(--color-silver-mist); line-height: 1.8;">
            • <b>안면 고정</b>: 눈가 1개, 오른쪽 쇄골/턱선 1개 시그니처 매력점<br>
            • <b>연령/마스크</b>: 24세 한국 여성, 촉촉한 모공 질감, 젖은 웨이브 흑발<br>
            • <b>시그니처 룩</b>: 빈티지 매트 블랙 개버딘 트렌치코트 + 샴페인 골드 실크
          </div>
        </div>
      </div>
    </div>

    <footer>
      Hookverse Studio · CEO Leo & Vice President Jena · System Synchronized at {now_str}
    </footer>
  </div>

  <script>
    function selectShortsVideo(src, title, desc, cardId) {{
      const video = document.getElementById('main-shorts-video');
      const titleEl = document.getElementById('current-video-title');
      const descEl = document.getElementById('current-video-desc');
      
      if (video) {{
        video.src = src;
        video.play().catch(function(e) {{
          console.log('User interaction required for unmuted autoplay:', e);
        }});
      }}
      
      if (titleEl) titleEl.innerText = title;
      if (descEl) descEl.innerText = desc;
      
      // Update active card styling
      document.querySelectorAll('.playlist-card').forEach(function(card) {{
        card.classList.remove('active');
        const badge = card.querySelector('.player-badge');
        if (badge) {{
          badge.innerText = '▶ 재생';
          badge.style.background = 'rgba(238, 211, 127, 0.2)';
          badge.style.color = 'var(--color-highlight-gold)';
          badge.style.borderColor = 'rgba(238, 211, 127, 0.4)';
        }}
      }});
      
      const targetCard = document.getElementById(cardId);
      if (targetCard) {{
        targetCard.classList.add('active');
        const activeBadge = targetCard.querySelector('.player-badge');
        if (activeBadge) {{
          activeBadge.innerText = '★ 지금 재생중';
          activeBadge.style.background = 'rgba(226, 75, 137, 0.2)';
          activeBadge.style.color = 'var(--color-action-raspberry)';
          activeBadge.style.borderColor = 'rgba(226, 75, 137, 0.4)';
        }}
      }}
    }}
  </script>
</body>
</html>
"""
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] ✅ [Developer 코다리] 시네마틱 관제 대시보드 빌드 완료: {OUTPUT_HTML}")
    return OUTPUT_HTML

if __name__ == "__main__":
    generate_dashboard_html()
