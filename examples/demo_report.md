# video-engine demo report

Synthetic 60.0s episode planned from voice durations 9.57s, 8.48s, 9.40s, 9.76s.

```json
{
 "title": 5.0,
 "prologue": 5.0,
 "voice_dur": [
  9.57,
  8.48,
  9.4,
  9.76
 ],
 "scene_dur": [
  11.47,
  10.38,
  11.3,
  11.66
 ],
 "scene_starts": [
  10.0,
  21.47,
  31.85,
  43.15
 ],
 "voice_starts": [
  11.0,
  22.47,
  32.85,
  44.15
 ],
 "end_dur": 5.19,
 "total": 60.0
}
```

First scene zoom filter:

```
[0:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0009,1.15)':d=344:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30,format=yuv420p[v]
```

Captions kept: 4/4 segments.

```srt
1
00:00:11,000 --> 00:00:15,200
Barsik runs the house and sleeps sixteen hours.

2
00:00:22,500 --> 00:00:26,900
Murzik hunts at night and ignores every rule.

3
00:00:32,800 --> 00:00:37,100
Pushok is white, round and permanently surprised.

4
00:00:44,100 --> 00:00:49,000
Together they are a gang with zero discipline.

```
