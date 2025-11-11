from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
import shutil

def make_delivery(folder_name: str, files: list, note_text: str):
    """
    Creates /deliveries/<folder_name>/ with your files + README.txt
    and a ZIP archive next to it. Returns paths.
    """
    root = Path(__file__).resolve().parents[1]
    base = root / "deliveries" / folder_name
    base.mkdir(parents=True, exist_ok=True)

# Copy files into folder (skip if already inside)
saved = []
for f in files:
    src = Path(f)
    if not src.exists():
        continue
    dst = base / src.name
    try:
        if src.resolve() == dst.resolve():
            # already in the delivery folder
            saved.append(dst)
        else:
            if dst.exists():
                # avoid overwrite if a same-named file already exists
                dst = base / f"{src.stem}_copy{len(saved)+1}{src.suffix}"
            shutil.copy2(src, dst)
            saved.append(dst)
    except Exception:
        # last-resort: don’t block packaging; just skip bad file
        continue

    # Write README
    (base / "README.txt").write_text(note_text.strip() + "\n", encoding="utf-8")

    # ZIP it
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = base.with_name(f"{base.name}_{stamp}.zip")
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as z:
        for p in base.iterdir():
            z.write(p, arcname=p.name)

    return str(base), str(zip_path)
