import datetime as dt
from email.message import Message
import json
from pathlib import Path
import sys
import unittest
from unittest import mock
import urllib.error


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import update_package_metrics as metrics


class FormattingTests(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).parent / "fixtures" / "sample-snapshot.json"
        self.snapshot = json.loads(fixture.read_text(encoding="utf-8"))

    def test_compact_number(self):
        self.assertEqual(metrics.compact_number(999), "999")
        self.assertEqual(metrics.compact_number(4729), "4.7k")
        self.assertEqual(metrics.compact_number(1_000_000), "1m")

    def test_monthly_totals_includes_empty_months(self):
        totals = metrics.monthly_totals(
            {"2026-07-01": 2, "2026-08-02": 4, "2026-08-19": 3},
            dt.date(2026, 8, 19),
        )

        self.assertEqual(len(totals), 12)
        self.assertEqual(totals[-2:], [("2026-07", 2), ("2026-08", 7)])

    def test_new_npm_package_can_lack_download_history(self):
        response_error = urllib.error.HTTPError(
            "https://example.test",
            404,
            "Not Found",
            hdrs=Message(),
            fp=None,
        )
        request_error = RuntimeError("request failed")
        request_error.__cause__ = response_error

        with (
            mock.patch.object(metrics, "request_json", side_effect=request_error),
            mock.patch("builtins.print"),
        ):
            daily = metrics.fetch_npm_daily(
                "@scope/new",
                dt.date(2026, 8, 20),
                dt.date(2026, 8, 20),
            )

        self.assertEqual(daily, {})

    def test_cards_are_valid_accessible_svgs(self):
        distribution = metrics.render_distribution(self.snapshot, dark=False)
        activity = metrics.render_activity(self.snapshot, dark=True)
        metrics.validate_svg(distribution, 790, 330)
        metrics.validate_svg(activity, 790, 330)
        self.assertIn("crates.io downloads", distribution)
        labels = [
            "npm downloads",
            "crates.io downloads",
            "VS Code installs",
            "npm packages",
            "crates.io crates",
            "Maven Central artifacts",
        ]
        self.assertEqual(sorted(labels, key=distribution.index), labels)
        self.assertEqual(activity.count('aria-hidden="true"'), 2)
        self.assertIn("independent scale per registry", activity)

    def test_crate_downloads_aggregate_versions_and_filter_dates(self):
        payload = {
            "version_downloads": [
                {"version": 1, "downloads": 2, "date": "2026-08-18"},
                {"version": 2, "downloads": 3, "date": "2026-08-18"},
                {"version": 2, "downloads": 4, "date": "2026-08-19"},
                {"version": 2, "downloads": 99, "date": "2026-08-20"},
            ]
        }

        with mock.patch.object(metrics, "request_json", return_value=payload):
            daily = metrics.fetch_crate_daily(
                "example",
                dt.date(2026, 8, 18),
                dt.date(2026, 8, 19),
            )

        self.assertEqual(daily, {"2026-08-18": 5, "2026-08-19": 4})


class CollectionTests(unittest.TestCase):
    @mock.patch.object(metrics, "fetch_npm_daily")
    @mock.patch.object(metrics, "fetch_npm_version")
    @mock.patch.object(metrics, "discover_npm_packages")
    def test_collection_preserves_missing_historical_days(
        self,
        discover,
        npm_version,
        npm_daily,
    ):
        discover.return_value = {"@scope/example"}
        npm_version.return_value = {"version": "1.2.3", "url": "https://example.test"}
        npm_daily.return_value = {"2026-08-18": 4, "2026-08-19": 5}
        config = {
            "npm_maintainer": "owner",
            "history_days": 3,
            "sources": [
                {
                    "id": "example",
                    "product": "example",
                    "label": "npm",
                    "metrics_label": "Example",
                    "type": "npm",
                    "package": "@scope/example",
                }
            ],
        }
        previous = {
            "npm": {
                "packages": {
                    "@scope/example": {
                        "daily": {
                            "2026-08-17": 3,
                            "2026-08-18": 2,
                            "2026-08-20": 99
                        }
                    }
                }
            },
        }

        snapshot = metrics.collect(config, previous, dt.date(2026, 8, 19))

        daily = snapshot["npm"]["packages"]["@scope/example"]["daily"]
        self.assertEqual(daily, {"2026-08-17": 3, "2026-08-18": 4, "2026-08-19": 5})
        self.assertEqual(snapshot["npm"]["downloads_30d"], 12)
        self.assertEqual(snapshot["npm"]["top_packages_30d"][0]["label"], "Example")

    def test_collection_skips_history_before_package_was_published(self):
        config = {
            "npm_maintainer": "owner",
            "history_days": 3,
            "sources": [
                {
                    "id": "new",
                    "product": "new",
                    "label": "npm",
                    "type": "npm",
                    "package": "@scope/new",
                }
            ],
        }
        with (
            mock.patch.object(metrics, "discover_npm_packages", return_value={"@scope/new"}),
            mock.patch.object(
                metrics,
                "fetch_npm_version",
                return_value={
                    "version": "0.1.0",
                    "url": "https://example.test",
                    "published_on": "2026-08-20",
                },
            ),
            mock.patch.object(metrics, "fetch_npm_daily") as npm_daily,
        ):
            snapshot = metrics.collect(config, {}, dt.date(2026, 8, 19))

        npm_daily.assert_not_called()
        self.assertEqual(snapshot["npm"]["package_count"], 1)
        self.assertEqual(snapshot["npm"]["packages"]["@scope/new"]["daily"], {})

    def test_collection_keeps_crates_separate_from_npm(self):
        config = {
            "npm_maintainer": "owner",
            "crates_io_owner_id": 42,
            "history_days": 3,
            "sources": [
                {
                    "id": "tool",
                    "product": "tool",
                    "label": "crates.io",
                    "type": "crates_io",
                    "crate": "tool",
                }
            ],
        }
        with (
            mock.patch.object(metrics, "discover_npm_packages", return_value=set()),
            mock.patch.object(metrics, "discover_crates", return_value={"tool"}),
            mock.patch.object(
                metrics,
                "fetch_crate",
                return_value={
                    "version": "1.0.0",
                    "url": "https://crates.io/crates/tool",
                    "downloads_total": 20,
                    "published_on": "2026-08-17",
                },
            ),
            mock.patch.object(
                metrics,
                "fetch_crate_daily",
                return_value={"2026-08-18": 3, "2026-08-19": 4},
            ),
        ):
            snapshot = metrics.collect(config, {}, dt.date(2026, 8, 19))

        self.assertEqual(snapshot["npm"]["downloads_30d"], 0)
        self.assertEqual(snapshot["crates_io"]["downloads_30d"], 7)
        self.assertEqual(snapshot["crates_io"]["downloads_total"], 20)
        self.assertEqual(snapshot["crates_io"]["crate_count"], 1)


if __name__ == "__main__":
    unittest.main()
