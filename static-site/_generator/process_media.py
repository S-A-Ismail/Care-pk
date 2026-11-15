#!/usr/bin/env python3
# ============================================================
#  CARE — event media pipeline (idempotent)
#  ---------------------------------------------------------
#  Reads   static-site/assets/data/media.json
#  Sources ../../Pictures            (READ-ONLY originals — never modified)
#  Writes  static-site/assets/images/events/   (consent != "required")
#          static-site/assets/videos/events/   (videos, copied as-is)
#          ../../_held-media/                  (consent == "required"; OUTSIDE the repo)
#          static-site/assets/data/media-outputs.json  (published outputs + sizes, read by build.py)
#          static-site/assets/logo-192.png + favicon-48.png
#          docs/media-publication-checklist.md
#
#  Run (WSL):
#      python3 -m venv ~/.venvs/care && ~/.venvs/care/bin/pip install pillow
#      ~/.venvs/care/bin/python static-site/_generator/process_media.py
#  Needs ffmpeg on PATH for video poster frames (apt install ffmpeg).
#
#  Allowed edits only: crop, resize, format conversion, logo overlay.
#  No upscaling, no retouching, no generative edits (photography policy §18).
#  Files are only rewritten when their bytes would change, so a second run
#  reports "unchanged" for everything.
# ============================================================
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # static-site/
REPO = os.path.dirname(ROOT)                      # Care-pk/
CAREPK = os.path.dirname(REPO)                    # "Care PK"/
SRC_DIR = os.environ.get("CARE_PICTURES", os.path.join(CAREPK, "Pictures"))
HELD_DIR = os.environ.get("CARE_HELD", os.path.join(CAREPK, "_held-media"))
IMG_OUT = os.path.join(ROOT, "assets", "images", "events")
VID_OUT = os.path.join(ROOT, "assets", "videos", "events")
MEDIA_JSON = os.path.join(ROOT, "assets", "data", "media.json")
OUTPUTS_JSON = os.path.join(ROOT, "assets", "data", "media-outputs.json")
LOGO = os.path.join(ROOT, "assets", "logo.png")
CACHE = os.path.join(HERE, "_cache")
LOGO_WM = os.path.join(CACHE, "logo-wm.png")
CHECKLIST = os.path.join(REPO, "docs", "media-publication-checklist.md")

CARD_MAX = (900, 600)        # 3:2
FULL_LONG = 1600
CARD_BUDGET = 90 * 1024
FULL_BUDGET = 300 * 1024
Q_DEFAULT, Q_FALLBACK = 80, 72

stats = {"written": [], "unchanged": [], "removed": [], "warnings": []}


# ---- helpers ------------------------------------------------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def inside(path, root):
    path, root = os.path.realpath(path), os.path.realpath(root)
    return os.path.commonpath([path, root]) == root


def write_if_changed(path, data):
    """Write bytes only if different — this is what makes the script idempotent."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            if f.read() == data:
                stats["unchanged"].append(path)
                return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    stats["written"].append(path)
    return True


def to_srgb(img):
    """Normalise to 8-bit sRGB RGB; convert via the embedded ICC profile if one exists."""
    img = ImageOps.exif_transpose(img)
    icc = img.info.get("icc_profile")
    if icc:
        try:
            from PIL import ImageCms
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            dst = ImageCms.createProfile("sRGB")
            img = ImageCms.profileToProfile(img.convert("RGB"), src, dst, outputMode="RGB")
        except Exception as e:  # pragma: no cover — fall back to plain conversion
            stats["warnings"].append("ICC conversion failed (%s); using plain RGB" % e)
    return img.convert("RGB")


def encode_webp(img, budget, label):
    """WebP q80 method 6, no EXIF/ICC; drop to q72 if over budget."""
    for q in (Q_DEFAULT, Q_FALLBACK):
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=q, method=6)
        data = buf.getvalue()
        if len(data) <= budget:
            return data, q
    stats["warnings"].append("%s is %d KB at q%d (budget %d KB)" % (label, len(data) // 1024, Q_FALLBACK, budget // 1024))
    return data, Q_FALLBACK


def card_crop(img, focus):
    """3:2 crop centred on the focal point (computed box — NOT ImageOps.fit centering),
    then downscale to ≤900×600. Never upscales."""
    W, H = img.size
    fx, fy = focus
    if W / H > 1.5:
        ch, cw = H, int(round(H * 1.5))
    else:
        cw, ch = W, int(round(W / 1.5))
    left = int(round(clamp(fx * W - cw / 2, 0, W - cw)))
    top = int(round(clamp(fy * H - ch / 2, 0, H - ch)))
    out = img.crop((left, top, left + cw, top + ch))
    if cw > CARD_MAX[0]:
        out = out.resize(CARD_MAX, Image.LANCZOS)
    return out


def full_resize(img):
    W, H = img.size
    long_edge = max(W, H)
    if long_edge <= FULL_LONG:
        return img.copy()
    s = FULL_LONG / long_edge
    return img.resize((int(round(W * s)), int(round(H * s))), Image.LANCZOS)


# ---- watermark ----------------------------------------------
_wm_base = None


def wm_base():
    """CARE logo cropped to its alpha bbox, downscaled (step 1 of 2) and cached."""
    global _wm_base
    if _wm_base is not None:
        return _wm_base
    logo = Image.open(LOGO).convert("RGBA")
    bbox = logo.getchannel("A").getbbox()
    logo = logo.crop(bbox)
    h = 600
    w = int(round(logo.width * h / logo.height))
    step1 = logo.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    step1.save(buf, "PNG", optimize=True)
    write_if_changed(LOGO_WM, buf.getvalue())
    _wm_base = step1
    return step1


def apply_watermark(img, corner):
    if corner == "none":
        return img
    W, H = img.size
    short = min(W, H)
    size = int(round(clamp(0.14 * short, 64, 150)))          # logo height in px
    margin = int(round(max(12, 0.03 * short)))
    base = wm_base()
    lw = int(round(base.width * size / base.height))           # keep aspect — never stretch
    logo = base.resize((lw, size), Image.LANCZOS)              # step 2 of 2
    alpha = logo.getchannel("A")
    logo.putalpha(alpha.point(lambda a: int(round(a * 0.92))))

    # faint soft shadow for legibility on light backgrounds
    blur = max(1, int(round(size * 0.04)))
    pad = blur * 3
    shadow = Image.new("RGBA", (lw + 2 * pad, size + 2 * pad), (0, 0, 0, 0))
    sh_alpha = Image.new("L", shadow.size, 0)
    sh_alpha.paste(alpha.point(lambda a: int(round(a * 0.35))), (pad, pad))
    sh_alpha = sh_alpha.filter(ImageFilter.GaussianBlur(blur))
    shadow.putalpha(sh_alpha)

    x = margin if corner[1] == "l" else W - margin - lw
    y = margin if corner[0] == "t" else H - margin - size
    out = img.convert("RGBA")
    off = max(1, size // 64)
    out.alpha_composite(shadow, (x - pad + off, y - pad + off))
    out.alpha_composite(logo, (x, y))
    return out.convert("RGB")


# ---- video poster -------------------------------------------
def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg  # optional pip fallback
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def extract_frame(video, t):
    exe = ffmpeg_exe()
    if not exe:
        raise SystemExit("ffmpeg not found — install it (sudo apt install ffmpeg) and re-run.")
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "frame.png")
        subprocess.run([exe, "-v", "error", "-y", "-ss", str(t), "-i", video,
                        "-frames:v", "1", png], check=True)
        return to_srgb(Image.open(png))


# ---- logo derivatives ---------------------------------------
def logo_derivatives():
    logo = Image.open(LOGO).convert("RGBA")
    for name, px in (("logo-192.png", 192), ("favicon-48.png", 48)):
        im = logo.copy()
        im.thumbnail((px * 4, px * 4), Image.LANCZOS)   # two-step downscale
        im.thumbnail((px, px), Image.LANCZOS)
        canvas = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        canvas.alpha_composite(im, ((px - im.width) // 2, (px - im.height) // 2))
        buf = io.BytesIO()
        canvas.save(buf, "PNG", optimize=True)
        write_if_changed(os.path.join(ROOT, "assets", name), buf.getvalue())


# ---- Board of Directors portraits ------------------------------
BOARD_JSON = os.path.join(ROOT, "assets", "data", "board.json")
PORTRAIT = (640, 800)        # 4:5


def board_sources():
    with open(BOARD_JSON, encoding="utf-8") as f:
        return [m for m in json.load(f).get("members", []) if m.get("photoSource")]


def board_portraits():
    """4:5 crop around the face, max 640x800, WebP, no EXIF, no watermark, never upscaled.
    Only written when photoConsent is "confirmed"."""
    for m in board_sources():
        out = os.path.join(ROOT, m["photo"])
        if m.get("photoConsent") != "confirmed":
            if os.path.exists(out):
                os.remove(out)
                stats["removed"].append(out)
            continue
        img = to_srgb(Image.open(os.path.join(SRC_DIR, m["photoSource"])))
        W, H = img.size
        fx, fy = m.get("photoFocus", [0.5, 0.4])
        if W / H > 0.8:
            ch, cw = H, int(round(H * 0.8))
        else:
            cw, ch = W, int(round(W / 0.8))
        left = int(round(clamp(fx * W - cw / 2, 0, W - cw)))
        top = int(round(clamp(fy * H - ch / 2, 0, H - ch)))
        im = img.crop((left, top, left + cw, top + ch))
        if cw > PORTRAIT[0]:
            im = im.resize(PORTRAIT, Image.LANCZOS)
        data, _q = encode_webp(im, CARD_BUDGET, os.path.basename(out))
        write_if_changed(out, data)


# ---- main ---------------------------------------------------
def main():
    with open(MEDIA_JSON, encoding="utf-8") as f:
        media = json.load(f)
    assert not inside(HELD_DIR, ROOT), "Held-media folder must be outside static-site/"

    outputs = {}
    held_ids = []
    for m in media:
        mid = m["id"]
        src = os.path.join(SRC_DIR, m["source"])
        held = m["consent"] == "required"
        out_dir = HELD_DIR if held else (VID_OUT if m["type"] == "video" else IMG_OUT)
        if held:
            held_ids.append(mid)
        entry = {"type": m["type"]}

        if m["type"] == "image":
            img = to_srgb(Image.open(src))
            if img.size != (m["width"], m["height"]):
                stats["warnings"].append("%s: source is %dx%d, media.json says %dx%d"
                                         % (mid, img.width, img.height, m["width"], m["height"]))
            variants = [("full", full_resize(img), FULL_BUDGET)]
            if not m.get("poster"):
                variants.insert(0, ("card", card_crop(img, m["focus"]), CARD_BUDGET))
            for kind, im, budget in variants:
                # optional per-variant corner (set after visual review, e.g. badge over a hand in the 3:2 crop)
                corner = m.get("wmCard", m["wm"]) if kind == "card" else m["wm"]
                im = apply_watermark(im, corner)
                data, q = encode_webp(im, budget, "%s-%s" % (mid, kind))
                write_if_changed(os.path.join(out_dir, "%s-%s.webp" % (mid, kind)), data)
                entry[kind] = {"src": "assets/images/events/%s-%s.webp" % (mid, kind),
                               "width": im.width, "height": im.height, "bytes": len(data), "q": q}
        else:  # video: copy bytes as-is, poster from a frame
            with open(src, "rb") as f:
                write_if_changed(os.path.join(out_dir, m["source"]), f.read())
            frame = extract_frame(src, m.get("posterAt", 1.0))   # ffmpeg applies rotation metadata
            if frame.size != (m["width"], m["height"]):
                stats["warnings"].append("%s: displays at %dx%d, media.json says %dx%d"
                                         % (mid, frame.width, frame.height, m["width"], m["height"]))
            poster = card_crop(frame, m["focus"])
            data, q = encode_webp(poster, CARD_BUDGET, mid + "-poster")
            write_if_changed(os.path.join(out_dir if held else IMG_OUT, mid + "-poster.webp"), data)
            fdata, fq = encode_webp(full_resize(frame), FULL_BUDGET, mid + "-frame")
            write_if_changed(os.path.join(out_dir if held else IMG_OUT, mid + "-frame.webp"), fdata)
            entry.update({
                "video": {"src": "assets/videos/events/" + m["source"], "width": frame.width, "height": frame.height},
                "card": {"src": "assets/images/events/%s-poster.webp" % mid, "width": poster.width,
                         "height": poster.height, "bytes": len(data), "q": q},
                "frame": {"src": "assets/images/events/%s-frame.webp" % mid, "width": frame.width,
                          "height": frame.height, "bytes": len(fdata), "q": fq},
            })
        if not held:
            outputs[mid] = entry

    # Remove any stale site copies derived from now-held media (e.g. consent withdrawn).
    for d in (IMG_OUT, VID_OUT):
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if any(fn.startswith(h + "-") or fn.startswith(h + ".") for h in held_ids):
                    os.remove(os.path.join(d, fn))
                    stats["removed"].append(os.path.join(d, fn))

    write_if_changed(OUTPUTS_JSON, (json.dumps(outputs, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    logo_derivatives()
    board_portraits()

    # ---- consent assertion: nothing under static-site/ derives from a held image
    bad = []
    for dp, _dn, fns in os.walk(ROOT):
        for fn in fns:
            if any(fn.startswith(h + "-") or fn.startswith(h + ".") for h in held_ids):
                bad.append(os.path.join(dp, fn))
    assert not bad, "Consent-held media found under static-site/: %s" % bad
    print("CONSENT CHECK OK — no file under static-site/ derives from: %s" % ", ".join(held_ids))

    write_checklist(media, outputs)

    rel = lambda p: os.path.relpath(p, CAREPK)
    print("written:   %d" % len(stats["written"]))
    for p in stats["written"]:
        print("  + " + rel(p))
    print("unchanged: %d" % len(stats["unchanged"]))
    if stats["removed"]:
        print("removed (held): " + ", ".join(rel(p) for p in stats["removed"]))
    for w in stats["warnings"]:
        print("WARNING: " + w)


def write_checklist(media, outputs):
    risk = {"required": "High — patients / minors identifiable",
            "unverified": "Medium — identifiable people, consent not yet confirmed",
            "confirmed": "Recorded consent on file",
            "not-required": "Low — poster / no identifiable individuals"}
    listed = {m["source"] for m in media} | {m["photoSource"] for m in board_sources()}
    unlisted = sorted(fn for fn in os.listdir(SRC_DIR) if fn not in listed
                      and fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov")))
    lines = [
        "# Media publication checklist",
        "",
        "Generated by `static-site/_generator/process_media.py` from `static-site/assets/data/media.json`.",
        "Mirrors Schedule 3 of the CARE Photography, Media & Consent Policy (pending signatures).",
        "Fill in *Reviewed by / Date* by hand when consent is checked.",
        "",
        "| Media | Event | Consent | Risk | Status | Notes | Reviewed by | Date |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for m in media:
        status = "HELD (outside repo)" if m["consent"] == "required" else "Published"
        notes = []
        if m.get("lowRes"):
            notes.append("low-res source %dx%d" % (m["width"], m["height"]))
        if m["type"] == "video":
            notes.append("video, copied as-is")
        if m.get("poster"):
            notes.append("event poster")
        lines.append("| `%s` | %s | %s | %s | %s | %s | | |" % (
            m["id"], m.get("event") or "—", m["consent"], risk[m["consent"]], status, "; ".join(notes) or ""))
    held = [m["id"] for m in media if m["consent"] == "required"]
    unver = [m["id"] for m in media if m["consent"] == "unverified"]
    low = [m["id"] for m in media if m.get("lowRes")]
    lines += ["", "## Held (not in the repo — `_held-media/`)", ""] + ["- `%s`" % i for i in held]
    lines += ["", "## Needs consent confirmation before deploy (`unverified`, currently published)", ""]
    lines += ["- `%s`" % i for i in unver]
    lines += ["", "## Low-resolution sources (displayed no wider than native)", ""] + ["- `%s`" % i for i in low]
    if unlisted:
        lines += ["", "## Source files not in media.json (not processed, not published)", ""]
        lines += ["- `%s`" % fn for fn in unlisted]
    write_if_changed(CHECKLIST, ("\n".join(lines) + "\n").encode("utf-8"))
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
