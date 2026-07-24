# CloudBuildBastionHost

A machine enrolled to dispatch to [[SuperpowersCloudBuild]]. Both Mac and jeff-ubuntu are bastion hosts — the box authenticates the **shared cloud-build SSH key**, not the machine, so the same key on both machines makes both valid dispatch hosts.

## Enrollment artifacts (all 3 required)
1. `~/.ssh/cloud-build/{id_ed25519, id_ed25519.pub, known_hosts}` — the keypair + host pin
2. `~/.config/cloud-build/state.json` — enrollment record (`enrolled_fp_hash`, `identity_file` path, `host`, `port`). Fix `identity_file`/`public_key_file` paths to the new machine's home when copying.
3. `~/superpowers-cloud-build-main/skills/cloud-build/scripts/` — the lib-client.sh + dispatch helpers

## Verify enrollment
```bash
cd ~/superpowers-cloud-build-main/skills/cloud-build
bash scripts/preflight-local.sh "$PROJECT" <plan_rel>   # → preflight OK
ssh -i ~/.ssh/cloud-build/id_ed25519 cloud-bastion@cloud.superpowers.build  # → "interactive shell is not permitted" = key accepted
```

## Why both (not Mac-only)
Originally jeff-ubuntu was unenrolled "by design" and `/super` fell through to local subagents — a bug. Fixed 2026-07-20: enrolled jeff-ubuntu by copying Mac artifacts; `/super` now dispatches to the box from either machine. See [[SuperCommand]].
