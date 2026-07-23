# Releasing

OpenEA Graph is not yet published to a package index. A release is ready for
publication when all of the following are true:

1. Conceptual-model changes were accepted through RFCs before implementation.
2. The specification, schemas, validator and normative examples are synchronized.
3. `CHANGELOG.md` describes user-visible changes and breaking changes explicitly.
4. The version in `pyproject.toml` matches the intended release.
5. CI passes on every supported Python version.
6. CI builds both a source distribution and wheel, then validates a repository
   using the installed wheel outside the source checkout.
7. The release tag and package artifacts are created from the same reviewed
   commit.

Publishing should be added as a separate, manually authorized workflow only
after the package name and package-index account ownership have been confirmed.
CI must never publish merely because a branch or pull request was updated.
