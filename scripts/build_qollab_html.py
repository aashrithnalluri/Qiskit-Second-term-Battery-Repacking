"""Build the self-contained, root-entrypoint browser assets for Qollab."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE_FILE = ROOT / "web" / "js" / "quantumBridge.js"
APP_FILE = ROOT / "web" / "js" / "app.js"
HTML_FILE = ROOT / "index.html"
STYLES_FILE = ROOT / "styles.css"
ASSET_SOURCES = {
    "repackq-demo-future.json": ROOT / "web" / "data" / "demo" / "future.json",
    "repackq-demo-inventory.json": ROOT / "web" / "data" / "demo" / "inventory.json",
    "repackq-demo-classical.json": ROOT / "web" / "data" / "demo" / "classical.json",
    "repackq-demo-qaoa-replay.json": ROOT / "web" / "data" / "demo" / "qaoa-replay.json",
    "repackq-benchmark-summary.json": ROOT / "web" / "data" / "benchmark" / "summary.json",
    "repackq-benchmark-trials.json": ROOT / "web" / "data" / "benchmark" / "trials.json",
}


def build_main_js() -> str:
    bridge = BRIDGE_FILE.read_text(encoding="utf-8")
    bridge = re.sub(r"^export\s+", "", bridge, flags=re.MULTILINE)
    bridge = bridge.replace(
        "export ",
        "",
    )
    bridge = bridge.rstrip()
    bridge = f"""(() => {{
  {bridge}
  return {{
    registerRuntimeAdapter,
    getRuntimeAdapter,
    hasInteractiveRuntime,
    getCapabilities,
    getDemoState,
    evaluateSelection,
    runClassicalComparison,
    runQaoa,
    revealFuture,
  }};
}})()"""

    app = APP_FILE.read_text(encoding="utf-8")
    app = app.replace('import * as quantumBridge from "./quantumBridge.js";\n\n', "", 1)
    app = app.replace(
        'const ASSET_ROOT = new URL("../data/", import.meta.url).href.replace(/\\/$/, "");',
        'const ASSET_ROOT = new URL("./", document.baseURI).href.replace(/\\/$/, "");',
        1,
    )
    replacements = {
        "${ASSET_ROOT}/demo/future.json": "${ASSET_ROOT}/repackq-demo-future.json",
        "${ASSET_ROOT}/demo/inventory.json": "${ASSET_ROOT}/repackq-demo-inventory.json",
        "${ASSET_ROOT}/demo/classical.json": "${ASSET_ROOT}/repackq-demo-classical.json",
        "${ASSET_ROOT}/demo/qaoa-replay.json": "${ASSET_ROOT}/repackq-demo-qaoa-replay.json",
        "${ASSET_ROOT}/benchmark/summary.json": "${ASSET_ROOT}/repackq-benchmark-summary.json",
        "${ASSET_ROOT}/benchmark/trials.json": "${ASSET_ROOT}/repackq-benchmark-trials.json",
    }
    for before, after in replacements.items():
        app = app.replace(before, after)
    if 'const asset = await response.json();' not in app:
        raise ValueError("Could not find the held-out fixture load to inline lazily.")
    future_load = '''const response = await fetch(`${ASSET_ROOT}/repackq-demo-future.json`, { cache: "no-store" });
      if (!response.ok) throw new Error("The held-out fixture asset could not be loaded.");
      const asset = await response.json();'''
    if future_load not in app:
        raise ValueError("Could not find the held-out fixture fetch to replace.")
    app = app.replace(future_load, "const asset = JSON.parse(QOLLAB_INLINE_FUTURE_JSON);", 1)

    asset_anchor = 'const ASSET_ROOT = new URL("./", document.baseURI).href.replace(/\\/$/, "");'
    if asset_anchor not in app:
        raise ValueError("Could not find the asset root declaration to inline fixtures.")
    inline_assets = {
        filename: json.loads(source.read_text(encoding="utf-8"))
        for filename, source in ASSET_SOURCES.items()
        if filename != "repackq-demo-future.json"
    }
    future_json = ASSET_SOURCES["repackq-demo-future.json"].read_text(encoding="utf-8")
    inline_declarations = (
        "const QOLLAB_INLINE_ASSETS = "
        + json.dumps(inline_assets, ensure_ascii=False, separators=(",", ":"))
        + ";\nconst QOLLAB_INLINE_FUTURE_JSON = "
        + json.dumps(future_json, ensure_ascii=False)
        + ";"
    )
    app = app.replace(asset_anchor, asset_anchor + "\n" + inline_declarations, 1)

    old_load_json = '''async function loadJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`Could not load ${path}`);
  return response.json();
}'''
    new_load_json = '''async function loadJson(path) {
  const filename = new URL(path, document.baseURI).pathname.split("/").pop();
  if (Object.prototype.hasOwnProperty.call(QOLLAB_INLINE_ASSETS, filename)) {
    return JSON.parse(JSON.stringify(QOLLAB_INLINE_ASSETS[filename]));
  }
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`Could not load ${path}`);
  return response.json();
}'''
    if old_load_json not in app:
        raise ValueError("Could not find the preview JSON loader to inline fixtures.")
    app = app.replace(old_load_json, new_load_json, 1)
    if "import.meta" in app or "./quantumBridge.js" in app:
        raise ValueError("The browser app still has an ES-module dependency after bundling.")
    if "await initialize();" not in app:
        raise ValueError("Could not find the app initialization statement to bundle.")
    app = app.replace("await initialize();", "await initialize();", 1)

    return f'''/* Generated by scripts/build_qollab_html.py. Edit web/js sources, then rebuild. */
(function () {{
  "use strict";

  function reportStartupError(error) {{
    var status = document.querySelector("#workspace-status");
    if (!status) return;
    status.textContent = "RePack-Q could not initialize: " + (error && error.message ? error.message : "an unexpected browser error occurred.");
    status.dataset.kind = "error";
  }}

  function boot() {{
    if (typeof document === "undefined" || !document.querySelector("#main-content")) return;
    if (window.__REPACKQ_APP_BOOT_STARTED__) return;
    window.__REPACKQ_APP_BOOT_STARTED__ = true;
    var quantumBridge = {bridge};
    (async function startRePackQApp() {{
{_indent(app, 6)}
    }})().catch(reportStartupError);
  }}

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", boot, {{ once: true }});
  }} else {{
    boot();
  }}
}})();
'''


def _indent(value: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else "" for line in value.rstrip().splitlines())


def build_index_html() -> str:
    html = HTML_FILE.read_text(encoding="utf-8")
    styles = STYLES_FILE.read_text(encoding="utf-8")
    stylesheet_link = re.compile(r'<link\s+rel="stylesheet"\s+href="styles\.css"\s*>', re.IGNORECASE)
    embedded_styles = f'<style id="repackq-inline-styles">\n{styles}\n</style>'
    if stylesheet_link.search(html):
        return stylesheet_link.sub(lambda _match: embedded_styles, html, count=1)
    style_tag = re.compile(
        r'<style\s+id="repackq-inline-styles"\s*>.*?</style>',
        re.IGNORECASE | re.DOTALL,
    )
    if style_tag.search(html):
        return style_tag.sub(lambda _match: embedded_styles, html, count=1)
    raise ValueError("Could not find the stylesheet link or generated style block in index.html.")


def build(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "main.js").write_text(build_main_js(), encoding="utf-8", newline="\n")
    (output_dir / "index.html").write_text(build_index_html(), encoding="utf-8", newline="\n")
    for source in ASSET_SOURCES.values():
        if not source.is_file():
            raise FileNotFoundError(f"Required Qollab fixture asset is missing: {source}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT, help="directory for standalone index.html and main.js entrypoints")
    args = parser.parse_args()
    build(args.output_dir.resolve())
    print(f"Built Qollab HTML/JS assets in {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
