"""
make_narration.py
나레이션 시트(narration_sheet.txt)를 읽어서
씬마다 속도/높낮이를 다르게 음성을 만들고 하나의 mp3로 이어 붙입니다.

사용법:
    python make_narration.py                  (기본 시트 사용)
    python make_narration.py 다른시트.txt      (다른 시트 사용)

결과물: narration_out 폴더 안에
    scene_01.mp3, scene_02.mp3 ...  (씬별 음성)
    narration_full.mp3              (전체 이어 붙인 것)
"""
import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

import edge_tts

BASE = Path(__file__).parent
OUT_DIR = BASE / "narration_out"
DEFAULT_VOICE = "ko-KR-SunHiNeural"
ALLOWED_KEYS = {"rate", "pitch", "volume", "voice"}


def parse_sheet(path):
    """[씬이름 | rate=-5% | pitch=-1Hz | pause=0.8] 블록을 읽어 씬 목록으로 만든다."""
    scenes = []
    current = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            parts = [p.strip() for p in line[1:-1].split("|")]
            current = {
                "name": parts[0],
                "rate": "+0%",
                "pitch": "+0Hz",
                "volume": "+0%",
                "voice": DEFAULT_VOICE,
                "pause": 0.5,
                "text": [],
            }
            for p in parts[1:]:
                if "=" not in p:
                    continue
                key, value = (s.strip() for s in p.split("=", 1))
                if key == "pause":
                    current["pause"] = float(value)
                elif key in ALLOWED_KEYS:
                    current[key] = value
            scenes.append(current)
        elif current is not None:
            current["text"].append(line)  # type: ignore[union-attr]
    for s in scenes:
        s["text"] = " ".join(s["text"])
    return [s for s in scenes if s["text"]]


async def make_scene(scene, out_path):
    communicate = edge_tts.Communicate(
        scene["text"],
        scene["voice"],
        rate=scene["rate"],
        pitch=scene["pitch"],
        volume=scene["volume"],
    )
    await communicate.save(str(out_path))


def merge(scene_files, pauses, final_path):
    """ffmpeg가 있으면 씬 사이 쉬는 시간을 넣어 이어 붙이고, 없으면 그냥 이어 붙인다."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        padded = []
        for f, pause in zip(scene_files, pauses):
            p = f.with_name(f.stem + "_pad.mp3")
            subprocess.run(
                [ffmpeg, "-y", "-loglevel", "error", "-i", str(f),
                 "-af", f"apad=pad_dur={pause}",
                 "-c:a", "libmp3lame", "-q:a", "2", str(p)],
                check=True,
            )
            padded.append(p)
        list_file = OUT_DIR / "list.txt"
        list_file.write_text(
            "".join(f"file '{p.name}'\n" for p in padded), encoding="utf-8"
        )
        subprocess.run(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(list_file), "-c", "copy", str(final_path)],
            check=True,
        )
        return True
    with open(final_path, "wb") as out:
        for f in scene_files:
            out.write(f.read_bytes())
    return False


async def main():
    sheet = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "narration_sheet.txt"
    if not sheet.exists():
        print(f"시트 파일을 찾을 수 없어요: {sheet}")
        return
    scenes = parse_sheet(sheet)
    if not scenes:
        print("시트에서 씬을 하나도 못 읽었어요. [씬이름 | ...] 형식을 확인해주세요.")
        return

    OUT_DIR.mkdir(exist_ok=True)
    files = []
    for i, s in enumerate(scenes, 1):
        out = OUT_DIR / f"scene_{i:02d}.mp3"
        print(f"[{i}/{len(scenes)}] {s['name']}  (속도 {s['rate']}, 높낮이 {s['pitch']})")
        await make_scene(s, out)
        files.append(out)

    final = OUT_DIR / "narration_full.mp3"
    used_ffmpeg = merge(files, [s["pause"] for s in scenes], final)
    print(f"\n완성: {final}")
    if not used_ffmpeg:
        print("ffmpeg가 없어서 씬 사이 쉬는 시간 없이 이어 붙였어요.")


if __name__ == "__main__":
    asyncio.run(main())
