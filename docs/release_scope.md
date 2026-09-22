# What this public release contains

This repository provides a small, independently runnable portion of the project:

- Statistical evaluation utilities, including Wilson intervals and exact paired tests.
- The reported aggregate counts used by those utilities.
- A typed policy-interface contract and dimension checks.
- Evaluation protocols and illustrated project documentation.

The metrics utility is adapted from the experiment aggregation code, with local paths removed and input validation added. The interface specification documents the manuscript; it contains no learned model. Aggregate counts are distinguished from raw rollout records throughout.

## Withheld components

The following are not part of this release:

- The shared backbone implementation, sparse expert/router implementation, learned feedback modules, embodiment adapters, task-specific residual modules, and action codecs.
- Training recipes, fine-tuning pipelines, checkpoint selection tools, weights, and optimizer states.
- Raw demonstrations, physical recordings, intermediate caches, and unpublished per-trial logs.
- Hardware drivers, calibration, serial-port mappings, network configuration, deployment credentials, and live control scripts.
- Internal notes, historical repositories, paper editing backups, local paths, identities, affiliations, and commit history from the research workspace.

Consequently, this package can reproduce calculations from reported counts, but cannot independently reproduce learned-policy results. No download link for withheld components is implied.

## Anonymous review distribution

Anonymizing file contents and commit metadata does not anonymize a GitHub account. A review copy must use an anonymous hosting address or an anonymized supplementary ZIP. Check relative links, image metadata, archive contents, and any hosting redirects before linking the review copy in the manuscript.

The README uses local SVG assets and does not embed analytics, visitor counters, external badges, author profiles, or institution logos.
