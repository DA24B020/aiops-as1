import argparse, csv, os
IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp"}
p = argparse.ArgumentParser()
p.add_argument("--root", default="data")
p.add_argument("--out", default="filelist.csv")
a = p.parse_args()
rows = []
for dirpath, _, filenames in os.walk(a.root):
    for fn in filenames:
        if os.path.splitext(fn)[1].lower() not in IMG_EXT:
            continue
        rel = os.path.relpath(os.path.join(dirpath, fn), a.root)
        parts = rel.split(os.sep)
        rows.append((fn, parts[0] if len(parts) > 1 else "",
                     parts[1] if len(parts) > 2 else "", rel))
rows.sort(key=lambda r: r[3])
with open(a.out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["filename", "split", "label", "relpath"])
    w.writerows(rows)
print(f"wrote {a.out}: {len(rows)} data rows (+1 header = {len(rows)+1} lines)")