from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
COMMIT = "035d84c655b4047bc9986c9a3db5106780d92f77"
REPO_PATH = "packing/src/sqpack/fractional/certificate.py"
URL = f"https://raw.githubusercontent.com/jlevy/squares/{COMMIT}/{REPO_PATH}"
with urlopen(Request(URL, headers={"User-Agent": "Codex-T1-M12-static-lock"}), timeout=30) as response:
    data = response.read()
    status = response.status
target = ROOT / "source" / "src" / "sqpack" / "fractional" / "certificate.py"
target.write_bytes(data)
row = {
    "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "commit": COMMIT,
    "repo_path": REPO_PATH,
    "url": URL,
    "status": status,
    "bytes": len(data),
    "sha256": hashlib.sha256(data).hexdigest(),
    "output": str(target.relative_to(ROOT)),
}
with (ROOT / "NETWORK_LOG.jsonl").open("a", encoding="utf-8") as log:
    log.write(json.dumps(row, ensure_ascii=False) + "\n")
print(json.dumps(row, ensure_ascii=False))
