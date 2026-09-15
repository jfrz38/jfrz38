#!/usr/bin/env python3
"""Fetch package data and safely refresh profile metrics assets."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
from pathlib import Path
import tempfile
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


USER_AGENT = "jfrz38-profile-metrics/1.0 (+https://github.com/jfrz38/jfrz38)"


def read_response(request: urllib.request.Request) -> bytes:
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code != 429 and exc.code < 500:
                raise RuntimeError(f"Request failed for {request.full_url}: {exc}") from exc
            last_error = exc
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
        if attempt < 2:
            time.sleep(2**attempt)
    raise RuntimeError(f"Request failed for {request.full_url}: {last_error}") from last_error


def request_json(
    url: str,
    *,
    data: dict[str, Any] | None = None,
    accept: str = "application/json",
) -> Any:
    body = None if data is None else json.dumps(data).encode("utf-8")
    headers = {"Accept": accept, "User-Agent": USER_AGENT}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers)
    try:
        return json.loads(read_response(request))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON response from {url}: {exc}") from exc


def request_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        return read_response(request).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"Invalid text response from {url}: {exc}") from exc


def npm_url(package: str) -> str:
    return "https://www.npmjs.com/package/" + package


def fetch_npm_version(package: str) -> dict[str, str]:
    encoded = urllib.parse.quote(package, safe="")
    metadata = request_json(f"https://registry.npmjs.org/{encoded}")
    version = metadata.get("dist-tags", {}).get("latest")
    if not version:
        raise RuntimeError(f"npm has no latest version for {package}")
    published_at = metadata.get("time", {}).get(version)
    result = {"version": str(version), "url": npm_url(package)}
    if isinstance(published_at, str):
        result["published_on"] = published_at[:10]
    return result


def fetch_npm_daily(package: str, start: dt.date, end: dt.date) -> dict[str, int]:
    encoded = urllib.parse.quote(package, safe="")
    period = f"{start.isoformat()}:{end.isoformat()}"
    try:
        payload = request_json(f"https://api.npmjs.org/downloads/range/{period}/{encoded}")
    except RuntimeError as exc:
        cause = exc.__cause__
        if isinstance(cause, urllib.error.HTTPError) and cause.code == 404:
            print(f"warning: npm download history is not available yet for {package}")
            return {}
        raise
    rows = payload.get("downloads")
    if not isinstance(rows, list) or not rows:
        raise RuntimeError(f"npm returned no download history for {package}")
    result: dict[str, int] = {}
    for row in rows:
        day = row.get("day")
        downloads = row.get("downloads")
        if not isinstance(day, str) or not isinstance(downloads, int) or downloads < 0:
            raise RuntimeError(f"npm returned invalid history for {package}")
        result[day] = downloads
    if start.isoformat() not in result or end.isoformat() not in result:
        raise RuntimeError(f"npm returned an incomplete date range for {package}")
    return result


def discover_npm_packages(maintainer: str) -> set[str]:
    query = urllib.parse.quote(f"maintainer:{maintainer}")
    payload = request_json(f"https://registry.npmjs.org/-/v1/search?text={query}&size=250")
    return {
        item["package"]["name"]
        for item in payload.get("objects", [])
        if item.get("package", {}).get("name")
    }


def crates_io_url(crate: str) -> str:
    return f"https://crates.io/crates/{crate}"


def fetch_crate(crate: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(crate, safe="")
    payload = request_json(f"https://crates.io/api/v1/crates/{encoded}")
    item = payload.get("crate", {})
    version = item.get("max_stable_version") or item.get("newest_version") or item.get("default_version")
    downloads = item.get("downloads")
    created_at = item.get("created_at")
    if not version or not isinstance(downloads, int) or downloads < 0:
        raise RuntimeError(f"crates.io returned invalid metadata for {crate}")
    result = {
        "version": str(version),
        "url": crates_io_url(crate),
        "downloads_total": downloads,
    }
    if isinstance(created_at, str):
        result["published_on"] = created_at[:10]
    return result


def fetch_crate_daily(crate: str, start: dt.date, end: dt.date) -> dict[str, int]:
    encoded = urllib.parse.quote(crate, safe="")
    payload = request_json(f"https://crates.io/api/v1/crates/{encoded}/downloads")
    rows = payload.get("version_downloads")
    if not isinstance(rows, list):
        raise RuntimeError(f"crates.io returned invalid download history for {crate}")
    result: dict[str, int] = {}
    for row in rows:
        day = row.get("date")
        downloads = row.get("downloads")
        if not isinstance(day, str) or not isinstance(downloads, int) or downloads < 0:
            raise RuntimeError(f"crates.io returned invalid download history for {crate}")
        if start.isoformat() <= day <= end.isoformat():
            result[day] = result.get(day, 0) + downloads
    return result


def discover_crates(owner_id: int) -> set[str]:
    query = urllib.parse.urlencode({"user_id": owner_id, "page": 1, "per_page": 100})
    payload = request_json(f"https://crates.io/api/v1/crates?{query}")
    return {item["name"] for item in payload.get("crates", []) if item.get("name")}


def fetch_maven(source: dict[str, Any]) -> dict[str, Any]:
    group_path = source["group"].replace(".", "/")
    base = f"https://repo1.maven.org/maven2/{group_path}/{source['artifact']}"
    root = ET.fromstring(request_text(f"{base}/maven-metadata.xml"))
    version = root.findtext("./versioning/release") or root.findtext("./versioning/latest")
    if not version:
        versions = [node.text for node in root.findall("./versioning/versions/version") if node.text]
        version = versions[-1] if versions else None
    if not version:
        raise RuntimeError(f"Maven metadata has no version for {source['id']}")
    portal = f"https://central.sonatype.com/artifact/{source['group']}/{source['artifact']}/{version}"
    return {"version": version, "url": portal}


def fetch_vscode(extension: str) -> dict[str, Any]:
    payload = {
        "filters": [
            {
                "criteria": [{"filterType": 7, "value": extension}],
                "pageNumber": 1,
                "pageSize": 1,
                "sortBy": 0,
                "sortOrder": 0,
            }
        ],
        "assetTypes": [],
        "flags": 914,
    }
    response = request_json(
        "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery",
        data=payload,
        accept="application/json;api-version=7.2-preview.1",
    )
    try:
        item = response["results"][0]["extensions"][0]
        version = item["versions"][0]["version"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"VS Code Marketplace has no result for {extension}") from exc
    statistics = {
        stat.get("statisticName", "").lower(): stat.get("value", 0)
        for stat in item.get("statistics", [])
    }
    installs = int(statistics.get("install", statistics.get("installdaily", 0)))
    return {
        "version": str(version),
        "installs": installs,
        "url": f"https://marketplace.visualstudio.com/items?itemName={extension}",
    }


def compact_number(value: int) -> str:
    if value >= 1_000_000:
        rendered = f"{value / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"{rendered}m"
    if value >= 1_000:
        rendered = f"{value / 1_000:.1f}".rstrip("0").rstrip(".")
        return f"{rendered}k"
    return str(value)


def svg_shell(width: int, height: int, content: str, *, dark: bool, title: str) -> str:
    background = "#0d1117" if dark else "#ffffff"
    border = "#30363d" if dark else "#d0d7de"
    text = "#e6edf3" if dark else "#1f2328"
    muted = "#8b949e" if dark else "#59636e"
    grid = "#21262d" if dark else "#eaeef2"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{html.escape(title)}</title>
  <desc id="desc">Package distribution metrics refreshed from public registries.</desc>
  <style>
    .title {{ font: 600 25px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; fill: {text}; }}
    .value {{ font: 600 24px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; fill: {text}; }}
    .label {{ font: 400 16px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; fill: {muted}; }}
    .small {{ font: 400 14px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; fill: {muted}; }}
    .grid {{ stroke: {grid}; stroke-width: 1; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" fill="{background}" stroke="{border}"/>
{content}
</svg>
"""


def render_distribution(snapshot: dict[str, Any], *, dark: bool) -> str:
    npm = snapshot["npm"]
    crates_io = snapshot["crates_io"]
    channels = snapshot["channels"]
    vscode = channels["vscode"]
    maven = channels["maven"]
    accent = "#58a6ff" if dark else "#0969da"
    content = f"""  <text x="28" y="42" class="title">Open-source footprint</text>
  <text x="28" y="98" class="value">{compact_number(npm['downloads_ytd'])}</text>
  <text x="28" y="124" class="small">npm downloads in {snapshot['as_of'][:4]}</text>
  <line x1="278" y1="68" x2="278" y2="142" class="grid"/>
  <text x="308" y="98" class="value">{compact_number(crates_io['downloads_ytd'])}</text>
  <text x="308" y="124" class="small">crates.io downloads in {snapshot['as_of'][:4]}</text>
  <line x1="528" y1="68" x2="528" y2="142" class="grid"/>
  <text x="558" y="98" class="value">{compact_number(vscode['installs'])}</text>
  <text x="558" y="124" class="small">VS Code installs</text>
  <line x1="28" y1="160" x2="762" y2="160" class="grid"/>
  <circle cx="38" cy="203" r="5" fill="{accent}"/>
  <text x="55" y="210" class="value">{npm['package_count']}</text>
  <text x="55" y="236" class="small">npm packages</text>
  <circle cx="288" cy="203" r="5" fill="{accent}"/>
  <text x="305" y="210" class="value">{crates_io['crate_count']}</text>
  <text x="305" y="236" class="small">crates.io crates</text>
  <circle cx="538" cy="203" r="5" fill="{accent}"/>
  <text x="555" y="210" class="value">{maven['artifact_count']}</text>
  <text x="555" y="236" class="small">Maven Central artifacts</text>
  <text x="28" y="270" class="small">Registry downloads are requests, not unique users.</text>
  <text x="28" y="301" class="small">Data through {snapshot['as_of']}</text>"""
    return svg_shell(790, 330, content, dark=dark, title="Open-source footprint")


def monthly_totals(daily: dict[str, int], end: dt.date) -> list[tuple[str, int]]:
    result = []
    end_month = end.year * 12 + end.month - 1
    for offset in range(11, -1, -1):
        month_index = end_month - offset
        year, zero_based_month = divmod(month_index, 12)
        key = f"{year:04d}-{zero_based_month + 1:02d}"
        total = sum(value for day, value in daily.items() if day.startswith(key))
        result.append((key, total))
    return result


def render_activity(snapshot: dict[str, Any], *, dark: bool) -> str:
    as_of = dt.date.fromisoformat(snapshot["as_of"])
    npm = snapshot["npm"]
    crates_io = snapshot["crates_io"]
    npm_months = monthly_totals(npm["daily_totals"], as_of)
    crate_months = monthly_totals(crates_io["daily_totals"], as_of)
    npm_accent = "#f05b5a" if dark else "#cb3837"
    crate_accent = "#f0883e" if dark else "#bc4c00"

    def bars(months: list[tuple[str, int]], baseline: int, color: str) -> str:
        maximum = max((value for _, value in months), default=0) or 1
        rectangles = []
        for index, (_, value) in enumerate(months):
            height = value * 62 / maximum
            rectangles.append(
                f'  <rect x="{252 + index * 42}" y="{baseline - height:.1f}" '
                f'width="28" height="{height:.1f}" rx="3" fill="{color}"/>'
            )
        return "\n".join(rectangles)

    month_names = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    labels = []
    for index in (0, 3, 6, 9, 11):
        key = npm_months[index][0]
        month = month_names[int(key[5:7]) - 1]
        labels.append(f'  <text x="{266 + index * 42}" y="276" text-anchor="middle" class="small">{month}</text>')

    content = f"""  <text x="28" y="42" class="title">Registry activity</text>
  <g transform="translate(28 74) scale(.75)" fill="{npm_accent}" aria-hidden="true">
    <path d="M1.763 0C.786 0 0 .786 0 1.763v20.474C0 23.214.786 24 1.763 24h20.474c.977 0 1.763-.786 1.763-1.763V1.763C24 .786 23.214 0 22.237 0zM5.13 5.323l13.837.019-.009 13.836h-3.464l.01-10.382h-3.456L12.04 19.17H5.113z"/>
  </g>
  <text x="54" y="91" class="label">npm</text>
  <text x="28" y="124" class="value">{compact_number(npm['downloads_30d'])}</text>
  <text x="28" y="145" class="small">last 30 days</text>
  <line x1="252" y1="142" x2="742" y2="142" class="grid"/>
{bars(npm_months, 142, npm_accent)}
  <g transform="translate(28 173) scale(.75)" fill="none" stroke="{crate_accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="m21 8-9-5-9 5 9 5 9-5Z"/>
    <path d="m3 8 9 5v9"/>
    <path d="m21 8-9 5"/>
  </g>
  <text x="54" y="190" class="label">crates.io</text>
  <text x="28" y="223" class="value">{compact_number(crates_io['downloads_30d'])}</text>
  <text x="28" y="244" class="small">last 30 days</text>
  <line x1="252" y1="241" x2="742" y2="241" class="grid"/>
{bars(crate_months, 241, crate_accent)}
{chr(10).join(labels)}
  <text x="28" y="304" class="small">Monthly downloads · independent scale per registry · through {snapshot['as_of']}</text>"""
    return svg_shell(790, 330, content, dark=dark, title="Monthly registry activity")


def validate_svg(text: str, expected_width: int, expected_height: int) -> None:
    if "Something went wrong" in text or "Resource not accessible" in text:
        raise RuntimeError("Generated SVG contains an error response")
    root = ET.fromstring(text)
    if not root.tag.endswith("svg"):
        raise RuntimeError("Generated asset is not an SVG")
    if root.get("width") != str(expected_width) or root.get("height") != str(expected_height):
        raise RuntimeError("Generated SVG has unexpected dimensions")
    if not root.findtext("{http://www.w3.org/2000/svg}title"):
        raise RuntimeError("Generated SVG has no accessible title")


def load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read previous metrics from {path}: {exc}") from exc


def collect(config: dict[str, Any], previous: dict[str, Any], today: dt.date) -> dict[str, Any]:
    history_days = int(config.get("history_days", 400))
    start = today - dt.timedelta(days=history_days - 1)
    cutoff = start.isoformat()
    previous_packages = previous.get("npm", {}).get("packages", {})
    packages: dict[str, Any] = {}

    npm_sources = [source for source in config["sources"] if source["type"] == "npm"]
    configured_npm = {source["package"] for source in npm_sources}
    discovered = discover_npm_packages(config["npm_maintainer"])
    unconfigured = sorted(discovered - configured_npm)
    if unconfigured:
        print("warning: unconfigured npm packages: " + ", ".join(unconfigured))

    for source in npm_sources:
        package = source["package"]
        release = fetch_npm_version(package)
        published_on = release.get("published_on")
        if published_on and published_on > today.isoformat():
            incoming = {}
        else:
            query_start = max(start, dt.date.fromisoformat(published_on)) if published_on else start
            incoming = fetch_npm_daily(package, query_start, today)
        old_daily = previous_packages.get(package, {}).get("daily", {})
        merged = {
            day: count
            for day, count in old_daily.items()
            if cutoff <= day <= today.isoformat()
        }
        merged.update(incoming)
        packages[package] = {
            "label": source["label"],
            "product": source["product"],
            "version": release["version"],
            "daily": dict(sorted(merged.items())),
        }

    previous_crates = previous.get("crates_io", {}).get("packages", {})
    crate_packages: dict[str, Any] = {}
    crate_sources = [source for source in config["sources"] if source["type"] == "crates_io"]
    configured_crates = {source["crate"] for source in crate_sources}
    owner_id = config.get("crates_io_owner_id")
    if owner_id is not None:
        discovered_crates = discover_crates(int(owner_id))
        unconfigured_crates = sorted(discovered_crates - configured_crates)
        if unconfigured_crates:
            print("warning: unconfigured crates.io packages: " + ", ".join(unconfigured_crates))
    else:
        unconfigured_crates = []

    for source in crate_sources:
        crate = source["crate"]
        metadata = fetch_crate(crate)
        published_on = metadata.get("published_on")
        if published_on and published_on > today.isoformat():
            incoming = {}
        else:
            query_start = max(start, dt.date.fromisoformat(published_on)) if published_on else start
            incoming = fetch_crate_daily(crate, query_start, today)
        old_daily = previous_crates.get(crate, {}).get("daily", {})
        merged = {
            day: count
            for day, count in old_daily.items()
            if cutoff <= day <= today.isoformat()
        }
        merged.update(incoming)
        crate_packages[crate] = {
            "label": source["label"],
            "product": source["product"],
            "version": metadata["version"],
            "downloads_total": metadata["downloads_total"],
            "daily": dict(sorted(merged.items())),
        }

    vscode_items = []
    maven_items = []
    for source in config["sources"]:
        if source["type"] == "vscode":
            item = fetch_vscode(source["extension"])
            vscode_items.append(item)
        elif source["type"] == "maven":
            item = fetch_maven(source)
            maven_items.append(item)

    all_days = sorted({day for package in packages.values() for day in package["daily"]})
    daily_totals = {
        day: sum(package["daily"].get(day, 0) for package in packages.values())
        for day in all_days
    }
    all_crate_days = sorted({day for package in crate_packages.values() for day in package["daily"]})
    crate_daily_totals = {
        day: sum(package["daily"].get(day, 0) for package in crate_packages.values())
        for day in all_crate_days
    }
    last_30_start = (today - dt.timedelta(days=29)).isoformat()
    previous_30_start = (today - dt.timedelta(days=59)).isoformat()
    previous_30_end = (today - dt.timedelta(days=30)).isoformat()
    year_start = dt.date(today.year, 1, 1).isoformat()

    def package_total(package: dict[str, Any], start_day: str, end_day: str) -> int:
        return sum(value for day, value in package["daily"].items() if start_day <= day <= end_day)

    top = sorted(
        (
            {
                "label": source.get("metrics_label", source["label"]),
                "package": source["package"],
                "downloads": package_total(packages[source["package"]], last_30_start, today.isoformat()),
            }
            for source in npm_sources
        ),
        key=lambda item: (-item["downloads"], item["package"]),
    )[:3]

    return {
        "as_of": today.isoformat(),
        "npm": {
            "maintainer": config["npm_maintainer"],
            "package_count": len(packages),
            "downloads_ytd": sum(value for day, value in daily_totals.items() if day >= year_start),
            "downloads_30d": sum(value for day, value in daily_totals.items() if day >= last_30_start),
            "downloads_previous_30d": sum(
                value for day, value in daily_totals.items() if previous_30_start <= day <= previous_30_end
            ),
            "daily_totals": daily_totals,
            "top_packages_30d": top,
            "packages": packages,
            "unconfigured_packages": unconfigured,
        },
        "crates_io": {
            "owner_id": owner_id,
            "crate_count": len(crate_packages),
            "downloads_total": sum(package["downloads_total"] for package in crate_packages.values()),
            "downloads_ytd": sum(value for day, value in crate_daily_totals.items() if day >= year_start),
            "downloads_30d": sum(value for day, value in crate_daily_totals.items() if day >= last_30_start),
            "daily_totals": crate_daily_totals,
            "packages": crate_packages,
            "unconfigured_packages": unconfigured_crates,
        },
        "channels": {
            "vscode": {
                "extension_count": len(vscode_items),
                "installs": sum(item["installs"] for item in vscode_items),
            },
            "maven": {"artifact_count": len(maven_items)},
        },
    }


def write_outputs(root: Path, snapshot: dict[str, Any]) -> None:
    output_dir = root / "profile"
    outputs = {
        "distribution-light.svg": render_distribution(snapshot, dark=False),
        "distribution-dark.svg": render_distribution(snapshot, dark=True),
        "registry-activity-light.svg": render_activity(snapshot, dark=False),
        "registry-activity-dark.svg": render_activity(snapshot, dark=True),
    }
    validate_svg(outputs["distribution-light.svg"], 790, 330)
    validate_svg(outputs["distribution-dark.svg"], 790, 330)
    validate_svg(outputs["registry-activity-light.svg"], 790, 330)
    validate_svg(outputs["registry-activity-dark.svg"], 790, 330)

    with tempfile.TemporaryDirectory(dir=root) as temporary:
        staging = Path(temporary)
        (staging / "package-metrics.json").write_text(
            json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        for name, content in outputs.items():
            (staging / name).write_text(content, encoding="utf-8")

        output_dir.mkdir(exist_ok=True)
        for name in ["package-metrics.json", *outputs]:
            os.replace(staging / name, output_dir / name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--date", type=dt.date.fromisoformat, help="Override the run date (YYYY-MM-DD)")
    parser.add_argument(
        "--lag-days",
        type=int,
        default=2,
        help="Ignore registry reporting days that may not be complete (default: 2)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    if args.lag_days < 0:
        raise SystemExit("--lag-days cannot be negative")
    config_path = root / ".github" / "package-sources.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    previous = load_previous(root / "profile" / "package-metrics.json")
    run_date = args.date or dt.date.today()
    data_date = run_date - dt.timedelta(days=args.lag_days)
    snapshot = collect(config, previous, data_date)
    snapshot["refreshed_on"] = run_date.isoformat()
    write_outputs(root, snapshot)
    print(
        f"Updated {snapshot['npm']['package_count']} npm packages through {snapshot['as_of']} "
        f"and {snapshot['crates_io']['crate_count']} crates "
        f"({snapshot['npm']['downloads_30d']} npm and "
        f"{snapshot['crates_io']['downloads_30d']} crates.io downloads in 30 days)."
    )


if __name__ == "__main__":
    main()
