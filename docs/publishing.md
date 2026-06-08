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

In this repo the tag drives `release-fonts.yml`, which builds the fonts, creates the
GitHub Release, and attaches the font archives — this is the active release path. PyPI
publishing (`publish.yml`) is **currently manual-only** (run it from the Actions tab when
trusted publishing is configured); the tag does **not** publish to PyPI yet. See
[fonts-build-and-release.md](fonts-build-and-release.md) for the font side and the
release-notes workflow.

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

4. **Create a version tag:**

   - Commit code and make sure it’s running correctly.

   - Confirm all tests are passing in the last CI workflow (Actions tab).

   - Tag a version (it’s wise to start with a `v`; a good first one is `v0.1.0`). Prefer
     `gh`, which also works from web sessions where `git push <tag>` is blocked:

     ```shell
     gh api repos/OWNER/PROJECT/git/refs \
       -f ref=refs/tags/v0.1.0 \
       -f sha="$(git rev-parse origin/main)"
     # or, from a local checkout: git tag v0.1.0 && git push origin v0.1.0
     ```

   - The tag triggers the workflows; the GitHub Release is created automatically by
     `release-fonts.yml`.

5. **Confirm it publishes to PyPI**

   - Watch for the release workflow in the GitHub Actions tab.

   - If it succeeds, you should see it appear at `https://pypi.org/project/PROJECT`.

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

6. **Write the release notes, then create the tag:**

   Add `docs/release/notes/vX.Y.Z.md` using the [Release Notes Format](#release-notes-format)
   below, and commit it to `main` so the tagged commit contains it. Then cut the tag with
   `gh` (this works from web sessions too, where `git push <tag>` is blocked — see
   [fonts-build-and-release.md](fonts-build-and-release.md#2-cut-the-tag) for details):

   ```shell
   gh api repos/OWNER/PROJECT/git/refs \
     -f ref=refs/tags/vX.Y.Z \
     -f sha="$(git rev-parse origin/main)"
   # or, from a local checkout: git tag vX.Y.Z && git push origin vX.Y.Z
   ```

   The tag triggers `release-fonts.yml`, which builds the fonts, creates the GitHub
   Release using your `docs/release/notes/vX.Y.Z.md` (falling back to auto-generated
   notes if none exists), and attaches the font archives. PyPI publishing (`publish.yml`)
   is manual-only for now, so the tag does not upload to PyPI.

7. **Verify the release published successfully:**

   ```shell
   # Check the release workflow:
   gh run list --workflow=release-fonts.yml --limit 1

   # Confirm the GitHub Release and its attached archives:
   gh release view vX.Y.Z
   ```

### Release Notes Format

Use this structure for release notes:

```markdown
## What's Changed

### Bug Fixes

**Short title of fix**

Description of what was fixed and why it matters.

### New Features

**Short title of feature**

Description of the new capability.

### Breaking Changes

**Short title of breaking change**

Description of what changed and how to migrate.

### Full Changelog

https://github.com/OWNER/PROJECT/compare/vPREVIOUS...vNEW
```

Guidelines:

- Use `## What's Changed` as the top-level heading.

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
