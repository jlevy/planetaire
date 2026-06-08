---
type: is
id: is-01ktjsvdrpvy38ma6e43vapstx
title: Confirm license/copyright notices are included in the distribution
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T05:03:57.205Z
updated_at: 2026-06-08T05:06:03.157Z
---
CONFIRMED: NOT fully OFL-compliant (pre-existing, not from this PR).

Findings:
1. Font name table carries ONLY Hack's notice (nameID 0 = 'Copyright (c) 2018 Source Foundry Authors / Bitstream'; nameID 13 = Hack MIT; nameID 14 = Hack LICENSE URL). It does NOT carry B612's copyright + OFL/EPL, nor the project's OFL-1.1 / Joshua Levy copyright. OFL requires the copyright + license notice to travel with the font.
2. Release archives (release-fonts.yml) bundle only ttf/, web/, README.txt -- no LICENSE file. The README.txt (docs/release/readme-*.txt) just says 'SIL Open Font License 1.1' + a URL; it does NOT include the OFL text or the constituent license texts (B612 OFL+EPL, Hack MIT, Nerd Fonts MIT) or their copyrights.

Fix:
- Build (ops/rename or a finalize step): set nameID 0 (combined copyright: Planetaire/Joshua Levy + B612/Intactile-Airbus + Hack/Source Foundry + Nerd Fonts/Ryan McIntyre), nameID 13 (OFL-1.1 description noting constituent licenses), nameID 14 (project OFL URL).
- Distribution: add a LICENSE/OFL.txt (+ constituent license texts) into dist/Extended and dist/Text and into the tar/zip in release-fonts.yml. Vendor the constituent license texts under docs/release/ or fonts/source/.
