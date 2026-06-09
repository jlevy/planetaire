## Publishing Releases

This is how to publish a Python package to [**PyPI**](https://pypi.org/) from GitHub
Actions, when using the
[**simple-modern-uv**](https://github.com/jlevy/simple-modern-uv) template.

Thanks to
[the dynamic versioning plugin](https://github.com/ninoseki/uv-dynamic-versioning/) and
the
[`publish.yml` workflow](https://github.com/jlevy/simple-modern-uv/blob/main/template/.github/workflows/publish.yml),
releases are tag-driven: push a version tag (standard format, e.g. `v0.1.0`) and the tag
triggers the build, which uploads the package to PyPI.

In this repo the active release path is font-specific: follow
[fonts-build-and-release.md](fonts-build-and-release.md). The tag drives
`release-fonts.yml`, which builds the fonts, creates the GitHub Release, and attaches
the font archives. PyPI publishing (`publish.yml`) is **manual-only** for now; the tag
does **not** publish to PyPI.

### First-Time Setup

This part is a little confusing the first time. Here is the simplest way to do it. For
the purposes of this example replace OWNER and PROJECT with the right values.

**Note:** These steps assume you already have a GitHub repo with your code pushed. If
you used [`uvx uvtemplate`](https://github.com/jlevy/uvtemplate), it handles repo
creation for you. If you're setting up manually, create an **empty** GitHub repo (no
README, no .gitignore, no license; the template already provides these) and push your
code to it. See the
[README](https://github.com/jlevy/simple-modern-uv#option-2-use-copier-and-git-yourself)
for details.

1. **Get a PyPI account** at [pypi.org](https://pypi.org/) and sign in.

2. **Pick a name for the project** that isn’t already taken.

   - Go to `https://pypi.org/project/PROJECT` to see if another project with that name
     already exits.

   - If needed, update your `pyproject.toml` with the correct name.

3. **Authorize** your repository to publish to PyPI:

   - Go to [the publishing settings page](https://pypi.org/manage/account/publishing/).

   - Find “Trusted Publisher Management” and register your GitHub repo as a new
     “pending” trusted publisher.

   - Enter the project name, repo owner, repo name, and `publish.yml` as the workflow
     name. (You can leave the “environment name” field blank.)

4. **Prepare and publish the font release:**

   - Commit code and make sure it’s running correctly.

   - Confirm all tests are passing in the last CI workflow (Actions tab).

   - Add curated notes at `docs/release/notes/vX.Y.Z.md` using
     [`docs/release/notes/TEMPLATE.md`](release/notes/TEMPLATE.md).

   - Use the font release script; it prepares the version-stamped specimen and README,
     then creates the release commit and annotated tag after review:

     ```shell
     make release VERSION=X.Y.Z
     make release-finalize VERSION=X.Y.Z
     ```

   - Push `main` and the tag as described in
     [fonts-build-and-release.md](fonts-build-and-release.md#4-push-the-commit-and-tag).
     The tag triggers `release-fonts.yml`.

5. **Confirm the GitHub font release publishes**

   - Watch for the release workflow in the GitHub Actions tab.

   - If it succeeds, you should see the GitHub Release and attached font archives.

   - Run the manual PyPI workflow separately only when you are intentionally publishing
     the build tooling package.

### Publishing Subsequent Releases

Follow this checklist for each new release.

#### Pre-Release Checklist

1. **Verify all changes are committed and pushed:**

   ```shell
   git status
   git log origin/main..HEAD  # should be empty if pushed
   ```

2. **Run linting and tests locally:**

   ```shell
   make lint
   make test
   ```

3. **Confirm CI is passing:**

   ```shell
   gh run list --limit 3
   ```

   Or check the Actions tab on GitHub.

4. **Determine the new version number:**

   ```shell
   # Check current/latest version:
   gh release list --limit 1
   ```

   Use [semantic versioning](https://semver.org/):

   - **Patch** (e.g., `v0.5.8` → `v0.5.9`): Bug fixes, minor changes

   - **Minor** (e.g., `v0.5.9` → `v0.6.0`): New features, backward-compatible

   - **Major** (e.g., `v0.6.0` → `v1.0.0`): Breaking changes

#### Create the Release

5. **Review changes since the last release:**

   ```shell
   # Get the last release tag:
   LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')

   # View commits since last release:
   git log ${LAST_TAG}..HEAD --oneline

   # View full diff:
   git diff ${LAST_TAG}..HEAD
   ```

6. **Write the release notes, then prepare and tag the release:**

   Add `docs/release/notes/vX.Y.Z.md` by copying
   [`docs/release/notes/TEMPLATE.md`](release/notes/TEMPLATE.md), and commit it to
   `main` so the tagged commit contains the release page text. Then use the font release
   script so the README CDN links and specimen PDF are pinned to the same tag:

   ```shell
   make release VERSION=X.Y.Z
   make release-finalize VERSION=X.Y.Z
   ```

   Then push `main` and the tag as described in
   [fonts-build-and-release.md](fonts-build-and-release.md#4-push-the-commit-and-tag).
   The tag triggers `release-fonts.yml`, which builds the fonts, creates the GitHub
   Release using your curated notes, and attaches the font archives. The workflow fails
   if the notes file is missing. PyPI publishing (`publish.yml`) is manual-only for now,
   so the tag does not upload to PyPI.

7. **Verify the release published successfully:**

   ```shell
   # Check the release workflow:
   gh run list --workflow=release-fonts.yml --limit 1

   # Confirm the GitHub Release and its attached archives:
   gh release view vX.Y.Z
   ```

### Release Notes Format

Start from [`docs/release/notes/TEMPLATE.md`](release/notes/TEMPLATE.md). The GitHub
Release page is also the downloads page, so notes must explain the packages before the
changelog.

Guidelines:

- Start with the product intro and links to the repo, README, install instructions, and
  web-font instructions.

- Keep the **Which package?** section so users can choose Text vs. Extended without
  reading the whole README.

- Describe archive contents and point users at `SHA256SUMS`.

- Use `## What's Changed` for release-specific changes.

- Group changes under `### Bug Fixes`, `### New Features`, `### Breaking Changes`, etc.
  as appropriate.

- Use `**bold**` for short titles of individual changes.

- Include technical details only when helpful for users.

- Always include the Full Changelog compare link at the end.

- For small releases, a simple bullet list is acceptable instead of full sections.

* * *

*This file was built with
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
