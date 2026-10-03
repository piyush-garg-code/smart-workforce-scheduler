# IP and License Audit

## Scope and method

This is a technical provenance audit, not legal advice. The repository was
searched for author names, reference URLs, old branding, copyright notices,
credentials, package metadata, documentation, tests, templates, and assets.
The reference named by the project owner was `Saykar/Duty-Scheduler`.

## Reference project and license

The reference repository was reachable for metadata inspection, but its GitHub
license endpoint returned `404 Not Found` and no license file was present in
this working copy. A missing license is not permission to reuse substantial
code. Human review is required before distributing any retained historical
material.

## Findings in the starting repository

- Python modules contained an original author marker and a legacy
  Duty Scheduler application label.
- The README described the old application and linked to dependencies.
- The implementation used Flask, SQLAlchemy, MySQL, and a holiday package.
- No image, frontend bundle, font, template, NOTICE, or LICENSE asset was
  present.
- Database strings were masked placeholders rather than usable credentials.
- Git history in this working directory contains a prior migration commit and
  must not be represented as the reference project's history.

## Rewrite performed

The runtime implementation was replaced rather than cosmetically renamed:

- New Flask application factory and route module.
- New SQLite schema and storage boundary.
- New business-day and rotation algorithm.
- New API contract under `/api`.
- New CLI, sample data, tests, requirements, and README.
- No legacy source modules, copied SQLAlchemy models, MySQL setup, or old
  Python 2 code remain in the runtime.

## Third-party components and assets

The rewritten project intentionally uses:

- Flask, under its upstream open-source license, for HTTP routing.
- pytest, under its upstream open-source license, for tests.
- Python standard library modules, under Python's PSF license.

No third-party images, icons, CSS, JavaScript bundles, fonts, or screenshots
were found or retained. Upstream license texts are not vendored; users should
consult the installed packages for their notices.

## Attribution that remains

The README keeps a concise acknowledgement that the repository originated
from work associated with `Saykar/Duty-Scheduler`, without claiming that work
as Piyush Garg's authorship. This is retained because provenance should not be
hidden and because the reference license status is unresolved.

## Independent contribution

The present schema, storage layer, API design, scheduling logic, analytics,
CLI, sample data, tests, and documentation are the new implementation in this
working tree. This does not establish exclusive copyright ownership of every
idea or eliminate obligations that may arise from the starting code.

## Manual legal review still required

1. Confirm whether any code copied before this rewrite was ever distributed
   under terms not visible in the current checkout.
2. Check the reference repository's commit history and any archived release
   for a license or contributor terms.
3. Decide whether to retain the acknowledgement or add a full notice if a
   license is later discovered.
4. Review any future assets and dependencies before redistribution.

Do not make a definitive claim that the repository is legally “100% mine”
without that review.
