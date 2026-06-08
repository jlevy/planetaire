---
type: is
id: is-01ktk221p7qgw6q8m4epybsbhw
title: "Terminal examples: two separate images, each dark+light, consistent in README and specimen"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T07:27:22.822Z
updated_at: 2026-06-08T07:27:22.822Z
---
On the README the terminal images combine two examples into a single image (terminal-dark.png/terminal-light.png at README.md:86-88 pack the syntax-highlighted Python analyze_trajectory() function AND a terminal session into one image). That looks odd, the font sizes between the two are not quite consistent, and the code sample differs from the specimen's. The specimen 'Planetaire Terminal' page (planetaire-mono-specimen.typ:304, #terminal-mockup() at :310) shows the two examples separately.

DESIRED: keep the two examples as SEPARATE images, each presented as a dark/light pair, the SAME way in both README and specimen:
1. Python example (analyze_trajectory() function) -- dark + light
2. Terminal example (eza/git terminal session) -- dark + light
Four images total, matching font sizes and the same code sample in README and specimen.

WORK: split/regenerate the terminal images in the image-generation recipe (find where terminal-*.png are produced), update README terminal section to show the two pairs, and update the specimen terminal page to show both dark and light for each example (matching README). Ensure font-size + code-sample parity across both docs.
