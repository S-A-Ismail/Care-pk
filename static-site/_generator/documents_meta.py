#!/usr/bin/env python3
# ============================================================
#  CARE — policy document metadata (re-runnable)
#  ---------------------------------------------------------
#  Reads the PDFs in static-site/assets/documents/ with poppler's
#  `pdfinfo` / `pdftotext` (sudo apt install poppler-utils) and writes
#  static-site/assets/data/documents.json.
#
#  First run: creates every entry (status "pending-signature").
#  Later runs: refresh ONLY version, pages and bytes from the PDFs and keep
#  title, status, signedOn, publish and group exactly as they are in the JSON.
#
#  Re-upload flow (see static-site/README.md): replace the PDF with the SAME
#  filename, run this script, set status "signed" + signedOn, run build.py.
#  The PDFs are never modified by this script.
# ============================================================
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC_DIR = os.path.join(ROOT, "assets", "documents")
OUT = os.path.join(ROOT, "assets", "data", "documents.json")

GROUPS = ["Governance", "Programmes & patients", "People & conduct",
          "Fundraising & finance", "Website & media"]

# Expected values (from the review brief, 14 Nov 2026) — used only to FLAG mismatches.
# file stem: (title, version, own status line, pages, group)
EXPECTED = {
    "care-governance-policy": ("Governance Policy", "1.0", "Final Draft for Board Approval", 25, "Governance"),
    "care-student-council-university-department-representatives-advisory-council-and-patron-governance-policy": (
        "Student Council, University Department Representatives, Advisory Council and Patron Governance Policy",
        "1.1", "Draft for Board Review", 32, "Governance"),
    "care-financial-management-policy": ("Financial Management Policy", "1.0", "Final Draft for Board Approval", 32, "Fundraising & finance"),
    "care-procurement-and-asset-management-policy": ("Procurement and Asset Management Policy", "2.0", "Final Draft for Board Approval", 31, "Fundraising & finance"),
    "care-donations-and-fundraising-policy": ("Donations and Fundraising Policy", "2.0", "Final Draft for Board Approval", 31, "Fundraising & finance"),
    "care-zakat-and-sadaqah-management-policy": ("Zakat and Sadaqah Management Policy", "1.0", "Final Draft for Board Approval", 28, "Fundraising & finance"),
    "care-patient-assistance-policy": ("Patient Assistance Policy", "1.0", "Final Draft for Board Approval", 30, "Programmes & patients"),
    "care-medical-assistance-and-referral-policy": ("Medical Assistance and Referral Policy", "2.0", "Final Draft for Board Approval", 28, "Programmes & patients"),
    "care-safeguarding-policy": ("Safeguarding Policy", "2.0", "Final Draft for Board Approval", 27, "People & conduct"),
    "care-code-of-conduct-and-ethics": ("Code of Conduct and Ethics", "2.0", "Final Draft for Board Approval", 28, "People & conduct"),
    "care-anti-harassment-and-non-discrimination-policy": ("Anti-Harassment and Non-Discrimination Policy", "1.0", "Final Draft for Board Approval", 24, "People & conduct"),
    "care-complaints-and-whistleblowing-policy": ("Complaints and Whistleblowing Policy", "1.0", "Final Draft for Board Approval", 19, "People & conduct"),
    "care-volunteer-policy": ("Volunteer Policy", "1.0", "Draft for Review", 7, "People & conduct"),
    "care-photography-media-and-consent-policy": ("Photography, Media and Consent Policy", "1.0", "Final Draft for Board Approval", 23, "Website & media"),
    "care-website-privacy-notice": ("Website Privacy Notice", "1.0", "Draft for Board Review", 6, "Website & media"),
    "care-website-terms-and-conditions": ("Website Terms and Conditions", "1.0", "Draft for Board Review", 9, "Website & media"),
}
ORDER = list(EXPECTED)

STATUS_RE = re.compile(r"(Final Draft for Board Approval|Draft for Board Review|Draft for Board Approval|Draft for Review)", re.I)
VERSION_RE = re.compile(r"Version(?:\s*(?:No\.?|Number))?\s*[:\-]?\s*v?(\d+(?:\.\d+)+)", re.I)


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, errors="replace").stdout


def pdf_meta(path):
    info = run(["pdfinfo", path])
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    title_m = re.search(r"^Title:\s+(.*)$", info, re.M)
    text = run(["pdftotext", "-f", "1", "-l", "3", "-layout", path, "-"])
    vm = VERSION_RE.search(text)
    sm = STATUS_RE.search(text)
    return {
        "pages": pages,
        "bytes": os.path.getsize(path),
        "version": vm.group(1) if vm else None,
        "statusLine": " ".join(sm.group(1).split()) if sm else None,
        "pdfTitle": title_m.group(1).strip() if title_m else "",
    }


def main():
    existing = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            existing = {d["file"]: d for d in json.load(f)}

    files = sorted(fn for fn in os.listdir(DOC_DIR) if fn.lower().endswith(".pdf"))
    stems = [fn[:-4] for fn in files]
    stems.sort(key=lambda s: ORDER.index(s) if s in ORDER else len(ORDER))

    out, flags = [], []
    for stem in stems:
        fn = stem + ".pdf"
        path = os.path.join(DOC_DIR, fn)
        with open(path, "rb") as f:
            if f.read(4) != b"%PDF":
                flags.append("%s does not start with %%PDF" % fn)
        meta = pdf_meta(path)
        exp = EXPECTED.get(stem)
        if exp:
            title, ver, status_line, pages, group = exp
            if meta["version"] != ver:
                flags.append("%s: version in PDF = %s, expected %s" % (fn, meta["version"], ver))
            if (meta["statusLine"] or "").lower() != status_line.lower():
                flags.append("%s: status line in PDF = %r, expected %r" % (fn, meta["statusLine"], status_line))
            if meta["pages"] != pages:
                flags.append("%s: %d pages, expected %d" % (fn, meta["pages"], pages))
        else:
            title, group = stem.replace("care-", "").replace("-", " ").title(), "Website & media"
            flags.append("%s is not in the expected list — added with a guessed title/group, please review" % fn)

        prev = existing.get(fn, {})
        out.append({
            "file": fn,
            "title": prev.get("title", title),
            "version": meta["version"] or prev.get("version") or (exp[1] if exp else None),
            "status": prev.get("status", "pending-signature"),
            "signedOn": prev.get("signedOn", None),
            "pages": meta["pages"],
            "bytes": meta["bytes"],
            "publish": prev.get("publish", True),
            "group": prev.get("group", group),
        })

    for d in out:
        assert d["status"] in ("pending-signature", "signed"), d
        assert d["group"] in GROUPS, d
    data = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if data != old:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(data)
        print("documents.json written (%d documents)" % len(out))
    else:
        print("documents.json unchanged (%d documents)" % len(out))
    for d in out:
        print("  %-110s v%-4s %3d pp %7d B  %s" % (d["file"], d["version"], d["pages"], d["bytes"], d["status"]))
    if flags:
        print("\nMISMATCHES / FLAGS:")
        for fl in flags:
            print("  ! " + fl)
    else:
        print("\nCross-check: all versions, status lines and page counts match the expected table.")


if __name__ == "__main__":
    sys.exit(main())
