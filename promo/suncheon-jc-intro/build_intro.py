#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""순천승주청년회의소 인트로 영상 빌더.

원본 영상에서 장면을 자동으로 골라 2분짜리 인트로를 만든다.
윈도우/리눅스 공용. ffmpeg 과 ffprobe 만 있으면 된다.

  python build_intro.py --source "원본.mp4"
"""
import argparse, json, os, platform, re, shutil, subprocess, sys
from pathlib import Path

IS_WIN = platform.system() == "Windows"


# ---------------------------------------------------------------- 유틸

def run(cmd, capture=False, check=True, cwd=None):
    """ffmpeg 계열 명령 실행. capture=True 면 출력을 문자열로 돌려준다."""
    if capture:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, encoding="utf-8", errors="replace", cwd=cwd)
        if check and p.returncode != 0:
            sys.stderr.write(p.stdout[-4000:] + "\n")
            raise SystemExit(f"명령 실패: {' '.join(map(str, cmd[:6]))} ...")
        return p.stdout
    p = subprocess.run(cmd, cwd=cwd)
    if check and p.returncode != 0:
        raise SystemExit(f"명령 실패: {' '.join(map(str, cmd[:6]))} ...")
    return ""


def need(prog):
    p = shutil.which(prog)
    if not p:
        raise SystemExit(f"{prog} 를 찾을 수 없습니다. PATH 에 등록한 뒤 다시 실행하세요.")
    return p


def probe(src):
    out = run(["ffprobe", "-v", "error", "-print_format", "json",
               "-show_format", "-show_streams", str(src)], capture=True)
    d = json.loads(out)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        raise SystemExit("영상 스트림이 없습니다.")
    num, den = (v.get("r_frame_rate") or "30/1").split("/")
    return {
        "duration": float(d["format"]["duration"]),
        "width": int(v["width"]), "height": int(v["height"]),
        "fps": (float(num) / float(den)) if float(den) else 30.0,
        "has_audio": a is not None,
    }


def pick_font(cands):
    """실제로 설치돼 있는 첫 한글 폰트 이름을 고른다."""
    have = ""
    if shutil.which("fc-list"):
        try:
            have = subprocess.run(["fc-list", ":lang=ko", "family"], stdout=subprocess.PIPE,
                                  text=True, encoding="utf-8", errors="replace").stdout
        except Exception:
            have = ""
    if have:
        for c in cands:
            if c.lower() in have.lower():
                return c
    if IS_WIN:
        roots = [Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
                 Path(os.environ.get("LOCALAPPDATA", "")) / r"Microsoft\Windows\Fonts"]
        names = " ".join(f.name.lower() for r in roots if r.is_dir() for f in r.iterdir())
        for c in cands:
            if c.lower().replace(" ", "") in names.replace(" ", ""):
                return c
        return "Malgun Gothic"          # 윈도우에는 항상 있다
    return cands[0]


# ---------------------------------------------------------------- 장면 분석

def scan_scenes(src, thresh, wd, fast=True, log=print):
    """장면이 바뀌는 지점(초)의 목록. 실패하면 빈 목록.

    metadata 필터 출력은 로그가 아니라 파일로 받는다. -v error 로 돌리면
    로그 레벨에 묻혀 한 줄도 안 나오기 때문이다.
    """
    base = ["ffmpeg", "-v", "error", "-nostdin"]
    if fast:
        base += ["-skip_frame", "nokey"]
    tag = "scene_fast.txt" if fast else "scene_full.txt"
    (wd / tag).unlink(missing_ok=True)
    cmd = base + ["-i", str(Path(src).resolve()), "-an", "-sn",
                  "-vf", f"scale=256:-2,select='gt(scene,{thresh})',"
                         f"metadata=mode=print:file={tag}",
                  "-f", "null", os.devnull]
    run(cmd, capture=True, check=False, cwd=str(wd))
    out = (wd / tag).read_text(encoding="utf-8", errors="replace") if (wd / tag).is_file() else ""
    times = []
    cur = None
    for line in out.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            cur = float(m.group(1))
        elif "lavfi.scene_score" in line and cur is not None:
            times.append(cur)
            cur = None
    times = sorted(set(round(t, 2) for t in times))
    log(f"  장면 전환 {len(times)}개 검출 ({'빠른' if fast else '정밀'} 스캔)")
    return times


def plan_cuts(dur, cuts, scenes, head_pct=0.02, tail_pct=0.03, log=print):
    """각 컷에 원본의 어느 구간을 쓸지 정한다.

    장면 전환으로 원본을 토막 내고, 그 토막들을 이어 붙인 좌표 위에 컷을 고르게
    뿌린다. 한 컷은 반드시 한 장면 안에서 시작해 끝나며, 앞 컷과 겹치지 않는다.

    장면을 하나도 못 찾았으면 원본 전체를 한 토막으로 보고 고르게 나눈다.
    """
    n = len(cuts)
    lo, hi = dur * head_pct, dur * (1 - tail_pct)
    pad = 0.30                                   # 전환 직후 남기는 여유

    bounds = [lo] + [x for x in scenes if lo < x < hi] + [hi]
    segs = []
    for a, b in zip(bounds, bounds[1:]):
        a2 = a + (pad if a > lo else 0.0)
        if b - a2 > 0.6:
            segs.append((a2, b))
    if not segs:
        segs = [(lo, hi)]
    avail = sum(b - a for a, b in segs)

    need_total = sum(c["dur"] for c in cuts if not c.get("card"))
    if avail < need_total:
        log(f"  주의: 쓸 수 있는 원본이 {avail:.0f}초뿐이라 컷 {need_total:.0f}초를"
            f" 다 채우려면 일부 구간이 겹칩니다")

    def to_time(x):
        """이어 붙인 좌표 x → (실제 시각, 그 토막 번호)"""
        for j, (a, b) in enumerate(segs):
            L = b - a
            if x <= L:
                return a + x, j
            x -= L
        return segs[-1][1], len(segs) - 1

    def place(after, need):
        """after 이후에서, 한 장면 안에 need 초가 통째로 들어가는 가장 이른 시작점"""
        for x, y in segs:
            st = max(x, after)
            if st + need <= y:
                return st
        return None

    plan, prev_end, rewound = [], lo, False
    real = [i for i, c in enumerate(cuts) if not c.get("card")]
    for k, i in enumerate(real):
        need = cuts[i]["dur"]
        want, _ = to_time(max(0.0, avail * (k + 0.5) / len(real) - need / 2))
        st = place(max(prev_end, want), need)       # 여유 있으면 고르게 퍼뜨리고
        if st is None:
            st = place(prev_end, need)              # 빡빡하면 앞 컷 바로 뒤로
        if st is None:                              # 원본을 다 썼다 — 앞으로 되감는다
            rewound = True
            st = place(lo, need)
        if st is None:                              # 어느 장면도 이 컷보다 짧다
            st = min(max(want, lo), max(lo, hi - need))
        prev_end = st + need
        plan.append({"idx": i, "start": round(st, 3), "dur": need})
    if rewound:
        log("  주의: 원본이 짧아 뒤쪽 컷 일부가 앞 장면을 다시 씁니다")

    for i, c in enumerate(cuts):                  # 엔드 카드는 원본을 안 쓴다
        if c.get("card"):
            plan.append({"idx": i, "start": 0.0, "dur": c["dur"], "card": True})
    plan.sort(key=lambda x: x["idx"])
    log(f"  장면 {len(segs)}토막 · 컷 {n}개 배치 완료 "
        f"(원본 {plan[0]['start']:.1f}초 ~ {max(p['start'] + p['dur'] for p in plan if not p.get('card')):.1f}초)")
    return plan


# ---------------------------------------------------------------- 오디오

def pick_audio_window(src, length, wd, log=print):
    """소리가 가장 꽉 찬 length 초짜리 구간의 시작 시각을 고른다."""
    (wd / "r128.txt").unlink(missing_ok=True)
    run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(Path(src).resolve()), "-vn",
         "-af", "ebur128=framelog=quiet:metadata=1,"
                "ametadata=mode=print:key=lavfi.r128.M:file=r128.txt",
         "-f", "null", os.devnull], capture=True, check=False, cwd=str(wd))
    out = (wd / "r128.txt").read_text(encoding="utf-8", errors="replace") \
        if (wd / "r128.txt").is_file() else ""
    pts, vals = [], []
    cur = None
    for line in out.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            cur = float(m.group(1))
        elif "lavfi.r128.M=" in line and cur is not None:
            try:
                vals.append(float(line.split("=")[-1]))
                pts.append(cur)
            except ValueError:
                pass
            cur = None
    if len(vals) < 20:
        log("  라우드니스 분석 불가 — 원본 앞부분을 그대로 씁니다")
        return 0.0
    best, bestscore = 0.0, -1e9
    step = max(1, len(pts) // 240)
    for i in range(0, len(pts), step):
        s = pts[i]
        if s + length > pts[-1]:
            break
        seg = [v for p, v in zip(pts, vals) if s <= p <= s + length and v > -70]
        if len(seg) < 10:
            continue
        mean = sum(seg) / len(seg)
        var = sum((v - mean) ** 2 for v in seg) / len(seg)
        score = mean - 0.05 * var          # 크고 고른 구간을 선호
        if score > bestscore:
            best, bestscore = s, score
    log(f"  음악 구간 {best:.1f}초 지점부터 {length:.0f}초 사용")
    return round(best, 2)


def build_audio(src, info, cfg, total, wd, log=print):
    a = cfg["audio"]
    bed = wd / "bed.wav"
    if info["has_audio"] and a.get("mode", "bed") != "none":
        start = a.get("start")
        if start is None:
            start = pick_audio_window(src, min(total, info["duration"] * 0.9), wd, log=log)
        if start + total > info["duration"]:
            start = max(0.0, info["duration"] - total)
        af = (f"afade=t=in:st=0:d={a['fade_in']},"
              f"afade=t=out:st={max(0.0, total - a['fade_out']):.2f}:d={a['fade_out']},"
              f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo")
        run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-ss", f"{start:.3f}",
             "-i", str(src), "-t", f"{total:.3f}", "-vn", "-af", af,
             "-c:a", "pcm_s16le", str(bed)])
    else:
        log("  원본에 오디오가 없어 무음 베드를 만듭니다")
        run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi",
             "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{total:.3f}",
             "-c:a", "pcm_s16le", str(bed)])

    if not a.get("cues"):
        out = wd / "audio.wav"
        run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(bed),
             "-af", f"loudnorm=I={a['loudnorm_i']}:TP=-1.5:LRA=11,"
                     f"aformat=sample_rates=48000:channel_layouts=stereo",
             "-c:a", "pcm_s16le", str(out)])
        return out

    # 이름이 공개되는 지점에 라이저 + 임팩트를 깔아 준다
    riser, impact = wd / "riser.wav", wd / "impact.wav"
    run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi",
         "-i", "anoisesrc=color=pink:duration=2.6:amplitude=0.7:r=48000",
         "-af", ("volume='pow(min(t/2.6,1),3)':eval=frame,highpass=f=380,"
                 "aformat=channel_layouts=stereo"),
         "-c:a", "pcm_s16le", str(riser)])
    run(["ffmpeg", "-v", "error", "-nostdin", "-y",
         "-f", "lavfi", "-i", "sine=frequency=48:duration=3.2:r=48000",
         "-f", "lavfi", "-i", "sine=frequency=97:duration=3.2:r=48000",
         "-filter_complex", ("[0:a][1:a]amix=inputs=2:weights=1 0.45,"
                             "volume='exp(-2.0*t)':eval=frame,volume=2.2,"
                             "aformat=channel_layouts=stereo[o]"),
         "-map", "[o]", "-c:a", "pcm_s16le", str(impact)])

    r_at = max(0.0, float(a.get("cue_riser_at", 0)) - 2.6)
    i_at = float(a.get("cue_impact_at", 0))
    out = wd / "audio.wav"
    run(["ffmpeg", "-v", "error", "-nostdin", "-y",
         "-i", str(bed), "-i", str(riser), "-i", str(impact),
         "-filter_complex",
         (f"[1:a]adelay={int(r_at * 1000)}|{int(r_at * 1000)},volume=0.45[r];"
          f"[2:a]adelay={int(i_at * 1000)}|{int(i_at * 1000)},volume=0.8[k];"
          f"[0:a][r][k]amix=inputs=3:duration=first:normalize=0,"
          f"loudnorm=I={a['loudnorm_i']}:TP=-1.5:LRA=11,alimiter=limit=0.89,"
          f"aformat=sample_rates=48000:channel_layouts=stereo[o]"),
         "-map", "[o]", "-c:a", "pcm_s16le", str(out)])
    return out


# ---------------------------------------------------------------- 자막(ASS)

WHITE, GOLD = "&H00FFFFFF", "&H004DC2FF"
OUTL, SHAD = "&H50000000", "&H80000000"


def ass_header(font):
    def st(name, size, col, bold=1, fsp=0, outline=2.6, shadow=3):
        return (f"Style: {name},{font},{size},{col},{col},{OUTL},{SHAD},"
                f"{bold},0,0,0,100,100,{fsp},0,1,{outline},{shadow},5,80,80,60,1")
    return "\n".join([
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "YCbCr Matrix: TV.709", "",
        "[V4+ Styles]",
        ("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
         " BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
         " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"),
        st("Ment",    96,  WHITE, fsp=1,  outline=3.0, shadow=4),
        st("VLabel",  42,  GOLD,  fsp=12, outline=2.4, shadow=3),
        st("VLine",   100, WHITE, fsp=1,  outline=3.0, shadow=4),
        st("Key",     128, WHITE, fsp=3,  outline=3.6, shadow=5),
        st("Title",   162, WHITE, fsp=8,  outline=3.8, shadow=6),
        st("TitleEn", 52,  WHITE, fsp=22, outline=2.4, shadow=3),
        st("EndName", 104, WHITE, fsp=6,  outline=2.8, shadow=4),
        st("Slogan",  74,  GOLD,  fsp=2,  outline=2.8, shadow=4),
        st("Rule",    40,  GOLD,  bold=0, outline=0, shadow=0),
        st("Scrim",   40,  WHITE, bold=0, outline=0, shadow=0),
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]) + "\n"


def ts(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t - h * 3600 - m * 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def ev(a, b, style, text, x, y, fad=(500, 500), extra=""):
    tags = f"\\an5\\pos({x},{y})\\fad({fad[0]},{fad[1]}){extra}"
    body = text.replace("\n", "\\N")
    return f"Dialogue: 1,{ts(a)},{ts(b)},{style},,0,0,0,,{{{tags}}}{body}"


def scrim(a, b, x, y, w, h, fad=(500, 500), alpha="&HA0&", blur=45):
    """글자 뒤에 깔리는 아주 옅은 그늘. 흐리게 처리해 사각형으로 보이지 않는다.

    libass 는 \\an5 + 음수 좌표 그리기를 제대로 앉히지 못한다(오른쪽 아래
    모서리를 기준점에 붙여 버린다). 그래서 왼쪽 위(\\an7) 기준으로 직접 계산한다.
    """
    x0, y0 = int(x - w / 2), int(y - h / 2)
    return (f"Dialogue: 0,{ts(a)},{ts(b)},Scrim,,0,0,0,,"
            f"{{\\an7\\pos({x0},{y0})\\fad({fad[0]},{fad[1]})\\p1\\bord0\\shad0"
            f"\\1c&H000000&\\1a{alpha}\\blur{blur}}}"
            f"m 0 0 l {w} 0 l {w} {h} l 0 {h}{{\\p0}}")


def make_ass(cfg, font, path):
    b = cfg["brand"]
    subs = {"@name_ko": b["name_ko"], "@name_en": b["name_en"], "@slogan": b["slogan"]}
    lines = [ass_header(font)]
    for m in cfg["ments"]:
        a, z = m["t"]
        txt = subs.get(m["text"], m["text"])
        s = m["style"]
        if s == "ment":
            lines.append(ev(a, z, "Ment", txt, 960, 786))
        elif s == "value":
            lines.append(ev(a, z, "VLabel", m["label"], 960, 690, fad=(420, 380)))
            lines.append(ev(a, z, "VLine", txt, 960, 800, fad=(420, 380)))
        elif s == "key":
            lines.append(ev(a, z, "Key", txt, 960, 790, fad=(320, 320)))
        elif s == "title":
            lines.append(scrim(a, z, 960, 540, 1920, 1080, fad=(900, 700),
                               alpha="&H9E&", blur=0))
            lines.append(ev(a, z, "Title", txt, 960, 478, fad=(900, 700)))
        elif s == "title_en":
            lines.append(ev(a, z, "TitleEn", txt, 960, 634, fad=(1100, 700),
                            extra="\\alpha&H1A&"))
        elif s == "endname":
            lines.append(ev(a, z, "EndName", txt, 960, 494, fad=(700, 700)))
            # 이름 아래 가는 금색 선
            lines.append(f"Dialogue: 1,{ts(a + 0.5)},{ts(z)},Rule,,0,0,0,,"
                         f"{{\\an7\\pos(770,590)\\fad(600,700)\\p1\\bord0\\shad0"
                         f"\\1c{GOLD}}}m 0 0 l 380 0 l 380 4 l 0 4{{\\p0}}")
        elif s == "slogan":
            lines.append(ev(a, z, "Slogan", txt, 960, 682, fad=(800, 700)))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------- 영상

def cut_filter(cfg, dur, move):
    o = cfg["output"]; g = cfg["grade"]
    W, H, FPS = o["width"], o["height"], o["fps"]
    MW, MH = int(W * 4 / 3), int(H * 4 / 3)          # 줌 여유분
    f = [f"fps={FPS}",
         f"scale={MW}:{MH}:force_original_aspect_ratio=increase:flags=lanczos",
         f"crop={MW}:{MH}"]
    if move in ("in", "out"):
        n = max(2, int(round(dur * FPS)))
        z = (f"1+0.090*on/{n}" if move == "in" else f"1.090-0.090*on/{n}")
        f.append(f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                 f":d=1:s={W}x{H}:fps={FPS}")
    else:
        f.append(f"scale={W}:{H}:flags=lanczos")
    if g.get("enabled"):
        f.append(f"eq=contrast={g['contrast']}:saturation={g['saturation']}:gamma={g['gamma']}")
        f.append("colorbalance=rs=-0.02:bs=0.04:rh=0.03:bh=-0.02")
        if g.get("vignette"):
            f.append("vignette=angle=PI/4.6")
    if o.get("cinema_bars"):
        bar = int(round((H - W / 2.39) / 2 / 2) * 2)
        f.append(f"drawbox=x=0:y=0:w={W}:h={bar}:color=black@1:t=fill")
        f.append(f"drawbox=x=0:y={H - bar}:w={W}:h={bar}:color=black@1:t=fill")
    f.append("setsar=1,format=yuv420p")
    return ",".join(f)


def render_cuts(src, cfg, plan, wd, log=print):
    o = cfg["output"]
    outs = []
    for p, c in zip(plan, cfg["cuts"]):
        dst = wd / f"cut{p['idx']:02d}.mp4"
        outs.append(dst)
        if c.get("card"):
            vf = "vignette=angle=PI/3.4,noise=alls=5:allf=t+u,format=yuv420p,setsar=1"
            run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi",
                 "-i", f"color=c=0x070B12:s={o['width']}x{o['height']}:r={o['fps']}",
                 "-t", f"{c['dur']:.3f}", "-vf", vf,
                 "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
                 "-pix_fmt", "yuv420p", "-an", str(dst)])
        else:
            run(["ffmpeg", "-v", "error", "-nostdin", "-y",
                 "-ss", f"{p['start']:.3f}", "-i", str(src), "-t", f"{c['dur']:.3f}",
                 "-vf", cut_filter(cfg, c["dur"], c.get("move", "in")),
                 "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
                 "-pix_fmt", "yuv420p", "-an", str(dst)])
        log(f"  컷 {p['idx'] + 1:02d}/{len(plan)}  {c['dur']:.1f}초"
            + ("  [엔드 카드]" if c.get("card") else f"  원본 {p['start']:.1f}초"))
    return outs


def xfade_chain(cuts_files, cfg, wd, log=print):
    o = cfg["output"]
    starts, t = [], 0.0
    for i, c in enumerate(cfg["cuts"]):
        if i == 0:
            starts.append(0.0); t = c["dur"]
        else:
            s = t - c["tdur"]
            starts.append(s); t = s + c["dur"]
    total = t

    ins, fc, prev = [], [], "0:v"
    for f in cuts_files:
        ins += ["-i", str(f)]
    for i in range(1, len(cuts_files)):
        c = cfg["cuts"][i]
        lab = f"x{i}"
        fc.append(f"[{prev}][{i}:v]xfade=transition={c['trans']}:"
                  f"duration={c['tdur']}:offset={starts[i]:.3f}[{lab}]")
        prev = lab
    master = wd / "master.mp4"
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-y"] + ins
    if fc:
        cmd += ["-filter_complex", ";".join(fc), "-map", f"[{prev}]"]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-r", str(o["fps"]), "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "14", "-pix_fmt", "yuv420p", str(master)]
    run(cmd)
    log(f"  전환 연결 완료 — {total:.2f}초")
    return master, total


def make_scrim_png(wd, W, H, log=print):
    """화면 아래쪽을 부드럽게 눌러 주는 투명 그라데이션.

    자막 뒤에 상자를 까는 대신 이걸 화면 전체에 한 장 얹는다.
    모서리가 없으니 눈에 띄지 않으면서 흰 글씨가 하늘 위에서도 읽힌다.
    """
    png = wd / "scrim.png"
    top = int(H * 0.40)
    run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi",
         "-i", f"color=c=black:s={W}x{H}",
         "-vf", (f"format=rgba,geq=r=0:g=0:b=0:"
                 f"a='if(lt(Y,{top}),0,150*pow((Y-{top})/{H - top},1.7))'"),
         "-frames:v", "1", str(png)])
    return png


def finalize(master, audio, ass, cfg, total, out, wd, log=print):
    o = cfg["output"]
    fontsdir = str(Path(ass).parent)
    a = str(ass).replace("\\", "/").replace(":", "\\\\:")
    png = make_scrim_png(wd, o["width"], o["height"], log=log)
    fc = (f"[0:v][2:v]overlay=0:0:format=auto[sc];"
          f"[sc]ass='{a}':fontsdir='{fontsdir}',"
          f"fade=t=in:st=0:d=1.6,fade=t=out:st={total - 1.8:.2f}:d=1.8[v]")
    run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(master), "-i", str(audio),
         "-i", str(png),
         "-filter_complex", fc, "-map", "[v]", "-map", "1:a:0", "-shortest",
         "-c:v", "libx264", "-preset", o["preset"], "-crf", str(o["crf"]),
         "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.1",
         "-c:a", "aac", "-b:a", o["audio_bitrate"], "-ar", "48000",
         "-movflags", "+faststart", str(out)])
    log(f"  최종 인코딩 완료 → {out}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="순천승주청년회의소 인트로 영상 빌더")
    ap.add_argument("--source", required=True, help="원본 영상 경로")
    ap.add_argument("--config", default=str(Path(__file__).with_name("config.json")))
    ap.add_argument("--out", default=None, help="출력 파일 (기본: 순천승주청년회의소_인트로.mp4)")
    ap.add_argument("--workdir", default=None, help="중간 파일 폴더")
    ap.add_argument("--audio-start", type=float, default=None, help="음악 시작 지점(초)")
    ap.add_argument("--scene-threshold", type=float, default=0.28)
    ap.add_argument("--full-scan", action="store_true", help="장면 정밀 스캔 (느림, 정확)")
    ap.add_argument("--subs-only", action="store_true", help="자막·오디오만 다시 (컷 재사용)")
    ap.add_argument("--plan-only", action="store_true", help="컷 배치만 출력하고 종료")
    args = ap.parse_args()

    need("ffmpeg"); need("ffprobe")
    src = Path(args.source).expanduser()
    if not src.is_file():
        raise SystemExit(f"원본 영상을 찾을 수 없습니다: {src}")
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    if args.audio_start is not None:
        cfg["audio"]["start"] = args.audio_start

    out = Path(args.out) if args.out else src.parent / "순천승주청년회의소_인트로.mp4"
    wd = Path(args.workdir) if args.workdir else src.parent / "_intro_build"
    wd.mkdir(parents=True, exist_ok=True)

    def log(*a):
        print(*a, flush=True)

    log(f"원본  : {src.name}")
    info = probe(src)
    log(f"        {info['width']}x{info['height']}  {info['fps']:.2f}fps  "
        f"{info['duration']:.1f}초  오디오 {'있음' if info['has_audio'] else '없음'}")

    total_target = round(sum(c["dur"] for c in cfg["cuts"])
                         - sum(c["tdur"] for c in cfg["cuts"]), 3)
    need_len = sum(c["dur"] for c in cfg["cuts"] if not c.get("card"))
    if info["duration"] < need_len * 1.15:
        log(f"주의  : 원본이 짧습니다({info['duration']:.0f}초). "
            f"컷 {need_len:.0f}초분을 뽑으려면 여유가 부족해 화면이 겹칠 수 있습니다.")

    log("\n[1/5] 장면 분석")
    cache = wd / "scenes.json"
    scenes = json.loads(cache.read_text()) if cache.is_file() else []
    if scenes and not args.full_scan:
        log(f"  캐시 사용 — 장면 전환 {len(scenes)}개")
    else:
        scenes = scan_scenes(src, args.scene_threshold, wd, fast=not args.full_scan, log=log)
        if len(scenes) < 6 and not args.full_scan:
            log("  검출이 적어 정밀 스캔으로 다시 시도합니다")
            scenes = scan_scenes(src, args.scene_threshold, wd, fast=False, log=log)
        cache.write_text(json.dumps(scenes))

    log("\n[2/5] 컷 배치")
    plan = plan_cuts(info["duration"], cfg["cuts"], scenes, log=log)
    (wd / "cuts.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
    if args.plan_only:
        for p in plan:
            print(f"  컷 {p['idx'] + 1:02d}  원본 {p['start']:7.2f}초 ~ "
                  f"{p['start'] + p['dur']:7.2f}초")
        return

    log("\n[3/5] 컷 렌더링")
    files = [wd / f"cut{i:02d}.mp4" for i in range(len(cfg["cuts"]))]
    if args.subs_only and all(f.is_file() for f in files) and (wd / "master.mp4").is_file():
        log("  기존 컷 재사용")
        master, total = wd / "master.mp4", total_target
    else:
        files = render_cuts(src, cfg, plan, wd, log=log)
        master, total = xfade_chain(files, cfg, wd, log=log)

    log("\n[4/5] 사운드")
    audio = build_audio(src, info, cfg, total, wd, log=log)

    log("\n[5/5] 자막 + 최종 인코딩")
    font = pick_font(["Pretendard", "Noto Sans CJK KR", "Malgun Gothic",
                      "NanumGothic", "Noto Sans KR"])
    log(f"  폰트: {font}")
    ass = make_ass(cfg, font, wd / "ments.ass")
    finalize(master, audio, ass, cfg, total, out, wd, log=log)

    fin = probe(out)
    mb = out.stat().st_size / 1024 / 1024
    log(f"\n완성  : {out}")
    log(f"        {fin['width']}x{fin['height']}  {fin['duration']:.2f}초  {mb:.1f}MB")


if __name__ == "__main__":
    main()
