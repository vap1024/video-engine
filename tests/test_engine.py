import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from video_engine.plan import plan_scenes, zoom_expression, zoom_filter, lower_third_filter  # noqa: E402
from video_engine.timing import fmt_srt, render_srt, filter_window  # noqa: E402


class TestFmtSrt(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(fmt_srt(0), "00:00:00,000")

    def test_minutes_and_ms(self):
        self.assertEqual(fmt_srt(65.25), "00:01:05,250")

    def test_hours(self):
        self.assertEqual(fmt_srt(3661.5), "01:01:01,500")

    def test_rounding_carry(self):
        self.assertEqual(fmt_srt(59.9996), "00:01:00,000")

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            fmt_srt(-1)


class TestRenderSrt(unittest.TestCase):
    def test_two_segments(self):
        out = render_srt([
            {"start": 1.0, "end": 2.5, "text": " hello "},
            {"start": 3.0, "end": 4.0, "text": "world"},
        ])
        self.assertIn("00:00:01,000 --> 00:00:02,500", out)
        self.assertIn("hello", out)
        self.assertTrue(out.startswith("1\n"))

    def test_end_before_start_rejected(self):
        with self.assertRaises(ValueError):
            render_srt([{"start": 5, "end": 4, "text": "x"}])


class TestFilterWindow(unittest.TestCase):
    def test_keeps_overlapping_only(self):
        segs = [
            {"start": 0, "end": 5, "text": "a"},
            {"start": 10, "end": 12, "text": "b"},
            {"start": 55, "end": 59, "text": "c"},
        ]
        kept = filter_window(segs, 10.2, 54.8)
        self.assertEqual([s["text"] for s in kept], ["b"])


class TestPlan(unittest.TestCase):
    def test_demo_plan_totals_60(self):
        plan = plan_scenes([9.57, 8.48, 9.40, 9.76], total=60.0)
        total = plan["title"] + plan["prologue"] + sum(plan["scene_dur"]) + plan["end_dur"]
        self.assertAlmostEqual(total, 60.0, places=2)
        self.assertEqual(len(plan["scene_starts"]), 4)
        self.assertAlmostEqual(plan["voice_starts"][0], 11.0)

    def test_end_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            plan_scenes([25.0, 25.0], total=60.0)

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            plan_scenes([])

    def test_nonpositive_rejected(self):
        with self.assertRaises(ValueError):
            plan_scenes([0.0])


class TestFilters(unittest.TestCase):
    def test_zoom_in_caps_at_115(self):
        self.assertIn("1.15", zoom_expression(True))

    def test_zoom_out_starts_at_115(self):
        self.assertIn("if(eq(on,0),1.15", zoom_expression(False))

    def test_zoom_filter_frames(self):
        f = zoom_filter(10.0, zoom_in=True)
        self.assertIn("d=300", f)
        self.assertIn("s=1280x720", f)

    def test_zoom_filter_rejects_zero(self):
        with self.assertRaises(ValueError):
            zoom_filter(0)

    def test_lower_third_per_scene(self):
        f = lower_third_filter(11.0)
        self.assertIn("shortest=1", f)
        with self.assertRaises(ValueError):
            lower_third_filter(0)


if __name__ == "__main__":
    unittest.main()
