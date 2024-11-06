# Pull Request Template

## Description
<!-- Provide a clear and concise description of your changes. All changes should happen in the API first if applicable -->

## Type of Change
<!-- Add the appropriate label to your PR ('major', 'minor', or 'patch') based on the type of version bump needed -->

- [ ] Major version bump (incompatible API changes)
- [ ] Minor version bump (backwards-compatible functionality)
- [ ] Patch version bump (backwards-compatible bug fixes)
- [ ] Documentation only
- [ ] Other (please describe)

## Version Bump Label
<!-- 
IMPORTANT: This SDK follows semantic versioning (https://semver.org/). 
Please ensure you add ONE of the following labels to your PR:

- 'major' - for incompatible API changes (e.g., 1.0.0 -> 2.0.0)
- 'minor' - for new backwards-compatible functionality (e.g., 1.1.0 -> 1.2.0)
- 'patch' - for backwards-compatible bug fixes (e.g., 1.1.1 -> 1.1.2)

If no label is added, it will default to a patch bump.
-->

## Checklist
- [ ] I have added appropriate label for version bump ('major', 'minor', or 'patch')
- [ ] I have added tests for my changes (if applicable)
- [ ] I have updated documentation (if applicable)
- [ ] My code follows the project's coding standards
- [ ] All tests are passing

## Release Process
<!-- Information about the automated release process -->
When this PR is merged:
1. A new release will be automatically created based on the PR label
2. The version in `pyproject.toml` will be automatically updated
3. A new GitHub release will be created with a changelog
4. The package will be automatically published to PyPI
