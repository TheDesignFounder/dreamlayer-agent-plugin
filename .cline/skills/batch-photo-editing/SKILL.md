---
name: batch-photo-editing
description: "Apply a specified edit, background removal or upscaling task to a list of local images with DreamLayer. Use for a bounded batch with per-file results and a total credit budget."
---

# batch photo editing

Read [the workflow contract](references/workflow-contract.md) for setup, billing, recovery and output checks.

Enumerate input files and assign unique new outputs before uploading. Estimate total operations from current capabilities; an edit plus cutout is two paid operations per image. Maintain a per-item ledger of input, asset ID, saved request, idempotency key, execution ID, status and output. Process sequentially initially; stop new submissions on insufficient credits or exhausted budget. Resume existing executions after interruption. Skip already completed outputs rather than changing paths and charging again. Inspect a sample first and all outputs for tasks where fidelity matters. The batch is orchestration over individual operations, not a separate DreamLayer batch endpoint.

