# Contribution Guidelines

Thank you for your interest in contributing to `geolysis.core`!
We welcome contributions from the community to help make this
project better. Before you get started, please take a moment
to read and understand these contribution guidelines.
Following these guidelines helps maintain a productive and a
welcoming community for everyone involved.

Not a coder? Not a problem! `geolysis.core` is multi-faceted, and
we can use a lot of help. These are all activities we would
like to get help with:

- Code development
- Developing educational content
- Website design and development
- Writing technical documentation
- Branding (logo design etc.)

This project has a [code of conduct](code_of_conduct) that we
expect all contributors to adhere to. Please read and follow
it when participating in this project.

## Table of Contents

1. [Getting Started](#getting-started)
1. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Enhancements](#suggesting-enhancements)
   - [Pull Requests](#development-process---summary)
1. [Testing](#testing)
1. [Documentation](#documentation)
1. [Community](#community)
1. [License](#license)

## Getting Started

Before you start contributing, please make sure you have:

- Familiarized yourself with the project by visiting the
  [Project Repository](https://github.com/patrickboateng/geolysis).
- Create a [GitHub](https://github.com/join) account if you
  don't have one already.
- Review the project's issues and pull requests to see if
  the issue you want to work on or the feature you want to
  add is already being discussed.

## How to Contribute

### Reporting Bugs

If you encounter a bug or issue with the project, please follow
these steps:

1. Check the [existing issues](https://github.com/patrickboateng/geolysis/issues)
   to see if the issue has already been reported.
1. If not, create a new issue, describing the problem in detail.
   Include steps to reproduce if possible and any relevant error
   messages.

### Suggesting Enhancements

If you have an idea for an enhancement or a new feature, please
follow these steps:

1. Check the [existing issues](https://github.com/patrickboateng/geolysis/issues)
   to see if the enhancement has already been suggested.
1. If not, create a new issue, describing the enhancement in detail.
   Be clear about why it's valuable and how it should work.

### Development process - summary

If you want to contribute code to the project, please follow
these steps:

1. If you are a first time contributor:

   - Go to <https://github.com/patrickboateng/geolysis> and
     fork the repository to your own GitHub account.

   - Clone the project to your local computer:

     ```sh
     git clone https://github.com/your-username/geolysis.git
     ```

   - Move into the `geolysis` directory:

     ```sh
     cd geolysis
     ```

   - Add the upstream repository:

     ```sh
     git remote add upstream https://github.com/patrickboateng/geolysis.git
     ```

   - Now, `git remote -v` will show two remote repositories named:

     - `upstream`, which refers to the `geolysis` repository
     - `origin`, which refers to your personal fork

   - Pull the latest changes from upstream, including tags:

     ```sh
     git checkout main
     git pull upstream main --tags
     ```

1. Develop your contribution:

   - Create a branch for your contribution. Kindly use a
     descriptive name since the branch name will appear
     in the merge message.

     ```sh
     git checkout -b your-branch-name
     ```

   - Make your changes, following the [style guide](./style_guide.rst).
     _Make sure to read the style guide before contributing code to the
     `geolysis` project_.

   - Commit locally as you progress (`git add` and `git commit`).
     Use a [properly formatted](https://cbea.ms/git-commit/)
     commit message, write tests that fail before your change and
     pass afterward (both new and existing tests), run all
     [tests locally](#testing). Be sure to document any changed
     behavior in docstrings, keeping to the
     [style guide](style_guide.rst#code-documentation).

1. To submit your contribution:

   - Push your changes back to your fork on `GitHub`.

     ```sh
     git push origin your-branch-name
     ```

   - Go to GitHub, the new branch will show up with a green
     Pull request button. Make sure the title and message
     are clear, concise, and self-explanatory. Click the button
     to submit it.

1. Review process:

   - Respond to any feedback or questions from reviewers.
   - To update your Pull Request (PR), make your changes on your
     local repository, commit, run tests, and only if they pass
     should you push to your fork on GitHub. As soon as those
     changes are pushed up (to the same branch as before) the
     PR will update automatically. If you have no idea how to fix
     the test failures, you may push your changes any way and ask
     for help in a PR comment.
   - A PR must be approved by at least one core member before
     merging. Approval means the core team member has carefully
     reviewed the changes, and the PR is ready for merging.

## Testing

Running geolysis test suite locally requires some additional
packages, such as [pytest](https://pytest.org/) and
[coverage.py](https://coverage.readthedocs.io/en/7.3.2/)

- To run the tests, run the pytest command with no arguments as
  follows:

  ```sh
  pytest
  ```

- To measure the test coverage, run:

  ```sh
  coverage run --rcfile=pyproject.toml -m pytest
  ```

- Use `coverage report` to view report on the results:

  ```sh
  coverage report -m
  ```

- For a nicer presentation, use `coverage html` to get
  annotated HTML listings detailing missed lines:

  ```sh
  coverage html
  ```

  Then open **htmlcov/index.html** in your browser, to see a
  [report like this](https://nedbatchelder.com/files/sample_coverage_html/index.html)

## Documentation

Improvements to documentation are always appreciated. If you
make changes to the code, please update the documentation as
needed. See [style guide](style_guide.rst) for more information.

## Community

Join our community to discuss the project, ask questions, and
collaborate with other contributors:

- [GitHub Discussions](https://github.com/patrickboateng/geolysis/discussions)

## License

By contributing to this project, you agree that your contributions
will be licensed under the project's
[LICENSE](https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt).

## Thank You

Thank you for your interest in contributing to `geolysis.core`! We appreciate
your help in making this project a success.
