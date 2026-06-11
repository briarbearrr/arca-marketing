#!/usr/bin/env python3
"""
silence_cut.py — remove dead air / awkward pauses from a talking-head clip.

The hard-won lesson: neither signal alone is enough.
  * ffmpeg silencedetect misses pauses filled with ambient / breath above the
    noise floor.
  * whisper word timestamps are imprecise around pauses and will report two
    words as contiguous across a real ~1s gap.
So we CUT where EITHER is true (acoustic silence OR a transcript word-gap),
only remove the dead middle when it is long enough, keep short natural gaps,
and micro-fade every join to avoid clicks. Always re-run silencedetect on the
OUTPUT to confirm only short breath gaps remain — then RE-TRANSCRIBE the output
(every timestamp has shifted; never remap the old transcript).

Usage:
  python silence_cut.py --src src.mp4 --audio audio_clean.m4a \
      --transcript transcript.json --out tight.mp4 \
      [--cut-min 0.5] [--noise -33] [--sil-d 0.35] [--pad-pre 0.09] [--pad-post 0.09]

transcript.json: [{"text": "...", "start": s, "end": s}, ...]  (word level)
"""
import argparse, json, re, subprocess, sys, tempfile, os


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe_duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path])
    return float(r.stdout.strip())


def silencedetect(audio, noise, d):
    r = run(["ffmpeg", "-i", audio, "-af",
             f"silencedetect=noise={noise}dB:d={d}", "-f", "null", "-"])
    log = r.stderr
    return [(float(a), float(b)) for a, b in
            re.findall(r"silence_start: ([0-9.]+)\s*\n.*?silence_end: ([0-9.]+)", log)]


def build_ranges(words, sil, src_dur, cut_min, pad_pre, pad_post):
    win_s = max(0.0, words[0]["start"] - 0.12)
    win_e = min(src_dur, words[-1]["end"] + 0.18)
    # wordless gaps between consecutive words
    wl = [(p["end"], n["start"]) for p, n in zip(words, words[1:])
          if n["start"] - p["end"] > 0.45]
    cuts = sorted([(s, e) for s, e in sil if e > win_s + 0.2 and s < win_e - 0.2] + wl)
    # merge overlapping cut intervals
    merged = []
    for s, e in cuts:
        if merged and s <= merged[-1][1] + 0.02:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    # keep = complement; leave pad of speech on each side; only cut long dead middles
    keep, cur = [], win_s
    for s, e in merged:
        cs, ce = max(s + pad_post, cur), e - pad_pre
        if ce - cs > cut_min:
            if cs - cur > 0.18:
                keep.append([cur, cs])
            cur = max(ce, cur)
    if win_e - cur > 0.18:
        keep.append([cur, win_e])
    return [[round(a, 3), round(b, 3)] for a, b in keep]


def filtergraph(ranges):
    L, V, A = [], [], []
    for i, (a, b) in enumerate(ranges):
        fo = max(0.0, (b - a) - 0.012)
        L.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];")
        L.append(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:st=0:d=0.01,afade=t=out:st={fo:.3f}:d=0.012[a{i}];")
        V.append(f"[v{i}]"); A.append(f"[a{i}]")
    L.append("".join(v + a for v, a in zip(V, A)) +
             f"concat=n={len(ranges)}:v=1:a=1[v][a]")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--audio", required=True, help="denoised audio aligned to src timecodes")
    ap.add_argument("--transcript", required=True, help="word-level json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cut-min", type=float, default=0.5)
    ap.add_argument("--noise", type=int, default=-33)
    ap.add_argument("--sil-d", type=float, default=0.35)
    ap.add_argument("--pad-pre", type=float, default=0.09)
    ap.add_argument("--pad-post", type=float, default=0.09)
    args = ap.parse_args()

    words = json.load(open(args.transcript))
    src_dur = probe_duration(args.src)
    sil = silencedetect(args.audio, args.noise, args.sil_d)
    ranges = build_ranges(words, sil, src_dur, args.cut_min, args.pad_pre, args.pad_post)
    new_dur = sum(b - a for a, b in ranges)
    print(f"RANGES {len(ranges)}  NEW_DUR {new_dur:.2f}s  (removed {src_dur - new_dur:.2f}s)")
    for a, b in ranges:
        print(f"  {a:6.2f}-{b:6.2f}  ({b - a:.2f})")

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(filtergraph(ranges)); fg = f.name
    cmd = ["ffmpeg", "-y", "-i", args.src, "-i", args.audio,
           "-filter_complex_script", fg, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-crf", "18", "-preset", "medium",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", args.out]
    r = subprocess.run(cmd)
    os.unlink(fg)
    if r.returncode != 0:
        sys.exit("ffmpeg failed")
    print(f"\nwrote {args.out} ({probe_duration(args.out):.2f}s)")
    print("NEXT: verify with  ffmpeg -i", args.out,
          '-af "silencedetect=noise=-33dB:d=0.45" -f null -   (expect only short breath gaps)')
    print("THEN: re-transcribe the OUTPUT for caption timing.")


if __name__ == "__main__":
    main()
