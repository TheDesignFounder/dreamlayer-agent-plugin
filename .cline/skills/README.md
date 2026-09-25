# Generated skills

Do not edit these files. They are copied byte for byte from
`plugins/dreamlayer/skills/`, the canonical source, so that Cline load the same
workflows as every other host.

Change a workflow in the canonical source, then regenerate:

```sh
python3 scripts/sync_skills.py
```

`python3 scripts/sync_skills.py --check` fails when any copy has drifted, and
`python3 scripts/validate.py` runs that check.
