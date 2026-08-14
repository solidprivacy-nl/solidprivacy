# SolidPrivacy website

This directory contains the source baseline for `solidprivacy.nl` and future website development.

## Imported baseline

Source supplied by the principal on 2026-08-15 as `solidprivacy_v8.zip`.

- ZIP SHA-256: `d52d87d967e2fe723dfd3da2ee9f8273ce95de4dd02e8bb98d7388e01be93c58`
- Baseline label: `v8`
- Baseline purpose: preserve the then-current production website before the positioning/website redesign workstream.
- Import policy: do not silently rewrite the baseline while importing it; substantive redesign starts in later commits/PRs.

## Current structure

`website/site/` contains the editable static website source copied from the v8 production package. The original package also contained legacy/self-hosted font assets that are not referenced by the supplied HTML; those are intentionally not treated as part of the future design system unless a later audited migration requires them.

The two PNG media assets (`apple-touch-icon.png` and `og-image.png`) remain part of the v8 provenance package and must be carried into the deployable website before production cutover. Website redesign/deployment is a separate workstream from the current SolidPrivacy product PR stack.

## Source-of-truth intent

Once the website deployment workflow is approved, changes should follow:

`GitHub branch/PR -> preview/build checks -> approved merge -> Wrangler/Cloudflare deployment -> post-deploy verification`.

The public website is a projection of approved SolidPrivacy service/capability/positioning state; it must not make production or performance claims that are not supported by product/service evidence.
