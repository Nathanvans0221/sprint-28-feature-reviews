export const meta = {
  name: 'verify-feature-videos',
  description: 'Frame-verify each recorded feature video against its deep-dive demo script',
  phases: [{ title: 'Verify', detail: 'one agent per video: extract frames, read them, judge vs expected steps' }],
}

const SCHEMA = {
  type: 'object',
  required: ['pr', 'pass', 'severity', 'issues', 'evidence'],
  properties: {
    pr: { type: 'number' },
    pass: { type: 'boolean', description: 'true only if the video credibly demonstrates the feature with no visible mistakes' },
    severity: { type: 'string', enum: ['ok', 'minor', 'broken'], description: 'ok = ship it; minor = cosmetic wart but feature shown; broken = wrong/empty/error state filmed' },
    issues: { type: 'array', items: { type: 'string' }, description: 'specific problems seen in frames (empty grids, disabled buttons clicked, overlays, dialogs left open, error toasts, feature never shown)' },
    evidence: { type: 'array', items: { type: 'string' }, description: 'what each inspected frame showed, briefly' },
  },
}

const PRS = [9182, 7920, 9111, 7901]

phase('Verify')
const verdicts = await parallel(PRS.map(pr => () => agent(`You are verifying a screen-recorded feature demo video for PR #${pr} of worksuite-pwa, recorded against the live app. Judge STRICTLY — this video will be reviewed by the Director of Product, and the previous batch was rejected for mistakes.

DO THIS:
1. Find the video: run  V=$(find /home/natha/projects/ado-playwright-tests/reviews-output -name "*.webm" -path "*${pr}*" | head -1); echo $V  — if none exists, return pass=false severity=broken with issue "no video produced".
2. Get its duration:  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$V"
3. Extract 6 frames spread across the video into /tmp/verify-frames/ (create the dir):  for pct in 5 25 45 65 85 99; do ... done  — compute timestamps as duration*pct/100 (use ffmpeg -ss <t> -i "$V" -frames:v 1 /tmp/verify-frames/${pr}_<pct>.png). For the 99% frame use ffmpeg -sseof -2.
4. Read the expected demo script: run  python3 -c "import json; d=json.load(open('/tmp/demo_scripts.json')); s=d['${pr}']; print(json.dumps({'steps': s['demo_steps'], 'pitfalls': s['pitfalls']}, indent=1))"
5. Read EACH extracted frame with the Read tool and compare what you see against the expected steps, especially the FINAL frame vs the expected proof end-state.

JUDGING CRITERIA:
- broken: the feature is never actually shown (empty grid where data was expected, a disabled button clicked with no effect, an error toast, the wrong screen, a leftover overlay/dialog covering the end state, the demo stuck on a loading state).
- minor: feature clearly demonstrated but with a cosmetic wart (brief stray menu, slightly early cutoff, an extra dialog that was closed).
- ok: the demo shows the feature working and ends on a credible proof state.
Known acceptable: an orange version banner across the top of every frame; the app being SFG greenhouse data; for 8510 specifically, the final state 'No inventory recorded for this material item at the selected site.' IS the correct proof (no bin data on SFG).

Return ONLY the structured output.`, { label: `verify-${pr}`, phase: 'Verify', schema: SCHEMA })))

const out = verdicts.filter(Boolean)
return {
  passed: out.filter(v => v.pass).map(v => v.pr),
  minor: out.filter(v => v.severity === 'minor').map(v => v.pr),
  broken: out.filter(v => v.severity === 'broken'),
  all: out,
}
