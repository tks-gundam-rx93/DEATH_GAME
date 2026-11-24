#!/usr/bin/env python3
"""Overlay actual cinematic MP4s on the 510-second Japanese-audio workprint.

Keep existing dialogue and subtitles. Missing assets are never substituted.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True, type=Path)
    parser.add_argument('--manifest', default=Path(__file__).with_name('EP01_CINEMATIC_ASSET_MANIFEST.json'), type=Path)
    parser.add_argument('--assets', default=Path(__file__).with_name('cinematic_assets'), type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--allow-partial', action='store_true')
    parser.add_argument('--limit', type=float, default=510.)
    args = parser.parse_args()
    if not args.base.is_file():
        parser.error('Japanese-voiced base MP4 is missing')
    entries = json.loads(args.manifest.read_text(encoding='utf-8'))['assets']
    available, missing = [], []
    for entry in entries:
        p = args.assets / entry['file']
        if p.is_file() and p.stat().st_size > 1024 and entry['at'] < args.limit:
            available.append((entry, p))
        else:
            missing.append(entry)
    if missing and not args.allow_partial:
        print('Missing real cinematic assets: no render performed', file=sys.stderr)
        for e in missing:
            print(e['scene'], e['file'], e['task_id'], file=sys.stderr)
        return 2
    if not available:
        print('No real cinematic assets imported: refusing no-op output', file=sys.stderr)
        return 3
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-y', '-i', str(args.base)]
    for _, path in available:
        cmd.extend(['-i', str(path)])
    filters, previous = [], '[0:v]'
    for i, (entry, _) in enumerate(available, 1):
        start = float(entry['at'])
        seconds = min(float(entry['seconds']), args.limit - start)
        if seconds <= 0: continue
        fade = min(0.28, max(0.04, seconds / 8))
        label, output = f'[cin{i}]', f'[out{i}]'
        filters.append(
            f'[{i}:v]fps=24,scale=1280:720:force_original_aspect_ratio=increase,'
            f'crop=1280:720,trim=duration={seconds:.3f},setpts=PTS-STARTPTS,'
            f'format=yuva420p,fade=t=in:st=0:d={fade:.3f}:alpha=1,'
            f'fade=t=out:st={max(0, seconds-fade):.3f}:d={fade:.3f}:alpha=1,'
            f'setpts=PTS+{start:.3f}/TB{label}'
        )
        filters.append(
            f"{previous}{label}overlay=x=0:y=0:eof_action=pass:shortest=0:"
            f"enable='between(t,{start:.3f},{start+seconds:.3f})'{output}"
        )
        previous = output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cmd += ['-filter_complex', ';'.join(filters), '-map', previous,
            '-map', '0:a:0', '-map', '0:s?', '-c:v', 'libx264',
            '-preset', 'veryfast', '-crf', '24', '-pix_fmt', 'yuv420p',
            '-r', '24', '-c:a', 'copy', '-c:s', 'mov_text',
            '-t', f'{args.limit:.3f}', '-movflags', '+faststart', str(args.output)]
    print(f'Actual imported cinematic clips: {len(available)}; missing: {len(missing)}', flush=True)
    subprocess.run(cmd, check=True)
    print('Rendered:', args.output, flush=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())
