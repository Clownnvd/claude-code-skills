# Workflow 01: Capture App UI from PageFlows

## Tool

```bash
python scripts/pageflows_capture.py --app [app-name]
python scripts/pageflows_capture.py --app [app-name] --flows "onboarding,settings,login"
python scripts/pageflows_capture.py --app [app-name] --wait 3000
```

## Auth Setup (first time)

```bash
agent-browser --headed open https://pageflows.com
# Login manually, then:
agent-browser state save pageflows-auth.json
```

Saved session: `pageflows-auth.json` (root of project). Pro account: `magicduy56@gmail.com`.

## Steps

1. **Verify** `pageflows-auth.json` exists in project root
2. **Run**: `python scripts/pageflows_capture.py --app [app-name]`
3. Tool auto-discovers flows → extracts screen URLs via `eval + data-url` → screenshots each
4. **Verify**: open a few screenshots with the Read tool to confirm they look correct

## Output

```
screenshots/[app]/
  [flow-1]/
    01-[screen].png
    02-[screen].png
.tmp/[app]/
  manifest.json           ← Flows + screen metadata (input to next step)
```

## Edge Cases

| Problem | Fix |
|---------|-----|
| Screenshots look like login page | Re-auth: delete `pageflows-auth.json`, re-login |
| 0 flows discovered | Pass `--flows "flow1,flow2"` with manual slugs |
| App not found | Check exact slug: `pageflows.com/search/?q=[name]` |
| Blank/loading screenshots | Add `--wait 3000` flag |
| Some screens timeout | Tool continues — check manifest for gaps |

## Lessons

- PageFlows click interactions reliably timeout → `eval + data-url` is the correct pattern
- Keep browser session alive during entire capture — never close between flows
- Auth expires after ~1 day — re-authenticate if screenshots look wrong
- Screen images are 1920×1080 JPG — full resolution

## Next

```bash
python scripts/find_shared_components.py --manifest .tmp/[app]/manifest.json
# Then: references/build.md
```
