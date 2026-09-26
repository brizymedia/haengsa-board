"""실사 사진으로 히어로 배경 영상을 만든다 (천천히 확대·이동 + 교차 전환).

AI 영상은 한글·간판을 뭉갠다(프로이벤트 작업 교훈) → 고객의 실제 현장 사진만 쓴다.
사용: python make_hero.py <출력폴더> 사진1 사진2 ... (6~8장 권장)
결과: hero.mp4(1920x1080, 무음) · hero_sm.mp4(960x540, 폰) · hero_poster.webp
"""
import os, subprocess, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
out, imgs = sys.argv[1], sys.argv[2:]
os.makedirs(out, exist_ok=True)
DUR, FADE, FPS = 4.0, 0.8, 30
W, H = 1920, 1080
moves = [  # (시작 배율, 끝 배율, x 방향, y 방향)
    (1.0, 1.12, 0, 0), (1.12, 1.0, 1, 0), (1.0, 1.1, -1, 0),
    (1.08, 1.0, 0, 1), (1.0, 1.12, 1, -1), (1.1, 1.0, -1, 1),
]
parts = []
frames = int(DUR * FPS)
for i, p in enumerate(imgs):
    z0, z1, dx, dy = moves[i % len(moves)]
    z = f"{z0}+({z1}-{z0})*on/{frames}"
    x = f"(iw-iw/zoom)/2+{dx}*(iw-iw/zoom)/2*(on/{frames}-0.5)"
    y = f"(ih-ih/zoom)/2+{dy}*(ih-ih/zoom)/2*(on/{frames}-0.5)"
    seg = os.path.join(out, f"_seg{i}.mp4")
    vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
          f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p")
    subprocess.run([FF, '-y', '-loglevel', 'error', '-loop', '1', '-i', p, '-vf', vf,
                    '-t', str(DUR), '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', seg], check=True)
    parts.append(seg)
# 교차 전환으로 잇기
args = [FF, '-y', '-loglevel', 'error']
for s in parts:
    args += ['-i', s]
fc, prev, off = [], '[0:v]', DUR - FADE
for i in range(1, len(parts)):
    lab = f'[v{i}]'
    fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}{lab}")
    prev, off = lab, off + DUR - FADE
big = os.path.join(out, 'hero.mp4')
args += ['-filter_complex', ';'.join(fc) if fc else 'null', '-map', prev if fc else '0:v',
         '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '25', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', big]
subprocess.run(args, check=True)
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', big, '-vf', 'scale=960:540', '-an', '-c:v', 'libx264',
                '-crf', '27', '-preset', 'slow', '-movflags', '+faststart', os.path.join(out, 'hero_sm.mp4')], check=True)
subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', '0.5', '-i', big, '-frames:v', '1', '-q:v', '80',
                os.path.join(out, 'hero_poster.webp')], check=True)
for s in parts:
    os.remove(s)
for f in ('hero.mp4', 'hero_sm.mp4', 'hero_poster.webp'):
    print(f, os.path.getsize(os.path.join(out, f)) // 1024, 'KB')
