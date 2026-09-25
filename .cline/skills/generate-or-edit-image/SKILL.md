---
name: generate-or-edit-image
description: "Generate an original image, edit a local reference, remove a background, or upscale an image with DreamLayer. Use for visual assets in an app, website or creative project when the user wants image files."
---

# generate or edit image

Read [the workflow contract](references/workflow-contract.md) for setup, billing, recovery and output checks.

Establish the visual brief, output count, aspect ratio, destination and authorized credits. Select the operation by the requested change; an edit needs a reference, a new image does not. Use background_remove for transparency rather than assuming a prompt creates alpha. Upscale doubles both dimensions; input longest side must be <=2048 and output is capped at 4096. Supported aspect ratios: 1:1, 16:9, 9:16, 4:3, 3:4. Save files into the project, inspect, and report dimensions and remaining limitations. For logos, product photos, marketing and print artwork, read the matching installed task skill if present.

