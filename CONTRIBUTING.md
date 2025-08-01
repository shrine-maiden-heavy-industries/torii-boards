<!-- markdownlint-disable MD014 -->
# Contribution Guidelines

Hey! Thanks for your interest in contributing to Torii Boards!

A few important things to note up front:

* Contributions to the Torii Boards source code are licensed under the [BSD-2-Clause], the full text of which can be found in the [`LICENSE`] file in the root of the [git repository].
* Contributions to the Torii Boards documentation are licensed under the [CC-BY-SA 4.0], the full text of which can be found in the [`LICENSE.docs`] file in the root of the [git repository].
* When contributing to Torii Boards and interacting with people in/around the project be sure to keep in mind the [Code Of Conduct].
* We have a strict [AI usage policy], so be sure to read that.

Now that we've got that out of the way, there are a few ways to contribute. The first two are by either [reporting issues] or [suggesting a board], which we actively encourage users and developers alike to do -
we can't fix what we don't know about and we can't implement what we don't realise users want, making this a fantastic way to contribute. The next two are working on [development and testing] or on the [documentation].

No matter what it is you are looking to contribute, we would love to get you involved! The detailed instructions for each of them are outlined in their own sections below.

We look forward to your involvement!

## Reporting Issues

The goal for Torii is to be able to be as friendly and powerful as possible, allowing for anyone of any skill level to get into hardware design, as such it is extremely important that we get feedback from users so we know what snags, sharp corners, unclear information, and unexpected behavior they encounter.

It is asked that you please report any and all problems you encounter when using Torii, this can be from small things such as typos or weird wording, and unclear/confusing messages and diagnostics, to larger things such as general useability and tool integration.

Reporting an issue with Torii Boards is done through the [issue tracker], the issue templates should guide you through most of the needed information. A quick summary of what would be needed is as follows:

* The version of Torii Boards being used, this can be done by running `python -c "import torii_boards;print(torii_boards.__version__)"`
* Which version of Python being used, and if it's CPython or PyPy, as we don't support any other Python interpreters at the moment.
* Which operating system and it's version this happened on, this can help narrow down platform-specific issues.
* A Minimal, Complete, and Verifiable Example that reproduces the issue if possible.

Any other information you can provide will be a huge help in getting your problem solved, be it technical, or if it's a general useability issue with the tooling or language.

## Suggesting A Board

We would like to make Torii Boards as comprehensive as possible, so we encourage people to suggest boards for us to add, or even add them themselves if possible.

When suggesting a new board, the following information is needed:

* The board vendor, for example `Digilent`, `Avnet`, etc.
* The board name and part number.
* The device vendor, for example `Lattice`, `Altera`, etc.
* The device part number.

In addition to that, any extra details such as links to the store page for the board, schematic or pinout references, documentation, etc.

Once all of that is collected, you can [open a new issue] with the board suggestion template, it'll ask you for all the information, and give you a spot for any extra information.

## Development and Testing

> [!NOTE]
> It is recommended that before you make a large change or contribution, to discuss it with
> the maintainers to see if there are any potential snags or foreseeable difficulties with it.
> This will save you and the maintainers a large amount of potential frustration and time.

The guidelines and instructions below are a best-effort attempt at describing the least-friction way of getting started with doing development and testing for Torii Boards. If you notice any problems then please do [report an issue], and if you need any help then feel free to use the [discussion forum] or join the [IRC channel] and ask there.

### Required Tools

When working with the Torii code base, we require the following tools:

* Python (that's a given)
* [nox] - Our developer automation and testing tooling uses Nox
* [Yosys] - Yosys is our primary synthesis backend, even if working on a different toolchain

Optionally the following tools would be beneficial:

* [sby], [Yices2], and [Bitwuzla] - Some of our core tests use [formal verification] and so these tools are needed to support that.

Other than that, your code editor and everything else is up to personal taste, so go ham. If you are having a hard time finding things like [Yosys], [sby], [Yices2], and [Bitwuzla], those, along with a whole lot of other tools are in the [OSS CAD Suite] builds. Instructions in that repository should help you get those set up so you can use them with Torii.

### Setting Up

1. [Fork] the repository to your GitHub account and clone it locally if you've not done so already previously.
1. Within the local repository, add this repo as a remote: `git remote add upstream https://github.com/shrine-maiden-heavy-industries/torii-boards`
1. If you already have an existing clone, make sure it's up to date:
   1. Fetch all pending changes: `git fetch --all --prune`
   1. Switch back to the `main` branch: `git switch main`
   1. Pull the changes locally: `git pull upstream`
   1. Finally make sure your remote is up to date: `git push`
1. Create a new branch for your contribution: `git switch -c type/branch-name` (see the [Branch Naming] section for details on how to name it)

You're now ready to make your changes! Make sure see the [Formatting Code] and [Commit Guidelines] sections, and when you're ready to submit your changes for review, follow the steps in the [Submitting a Pull Request] section.

### Formatting Code

The overall style guidelines for Torii Boards are not super fixed or well defined at the moment, but the following things are required:

* All strings use single-quotes where possible, this includes doc comments.
* Indentation is done using hard-tabs, the general tab-stop used is 4, but use what you are happy with.
* The general gap between things should be a single line, unless it is at the top of the file after the imports block, then it should be 2.

The `nox -s lint` command can be used to check that any new code conforms to the current style for the codebase.

### Testing

To run the Torii Boards test suite, you can simply invoke `nox -s test`, this will do everything needed to set up Torii, Torii Boards, and then invoke it's test suite on the current state of the code base as it is locally.

If you are working in one specific part of the code base and don't want to wait for the full test suite to run you can specify a filter to use by passing extra arguments to [`unittest`] via nox like so:

```shell
$ nox -s test -- <unittest args here>
```

See the [`unittest` CLI] documentation for more information on any possible arguments.

### Commit Guidelines

It is beneficial for everyone involved in the project for commits to be reasonably small and atomic as possible, along with the messages being detailed.

The contents of a commit should be as tight in scope as possible, regardless if the overall change set is much broader. This helps with doing the review, as well as things such as aiding in `git bisect`, `git revert`, and `git rebase`.

When writing a commit message, the general recommendation is to have the first line, also known as the "short" description of the commit, be a tag which denotes what the commit touched followed by a brief summary. This is then followed by a blank line, and then followed by a more detailed description giving context and rational behind the change where appropriate.

The rules for tag at the front of the message are as follows:

* If the commit touches part of the core Torii package, try to use the full dotted path to the module. (e.g. `torii_boards.lattice`, `torii_boards.xilinx.arty_s7`, etc. )
* If the commit modifies anything to do with the documentation, then use `docs`.
* If the commit modifies anything to do with the CI or workflows, then use `ci`.
* If it's something not covered here, make a best-effort guess based on the rules above.
* Suffix the tag with `:` before the description.

Some examples of good commit messages are as follows:

```text
docs: Fixed a pile of typos in the board descriptions
```

```text
torii.xilinx: Added Kria SoM

This adds board definitions for the Xilinx Kria SoMs and also the
evaluation platforms for them.
```

Finally, it is ***highly*** recommended for you to sign all your commits, if you need help with setting this up, see the GitHub documentation on [signing commits] and [setting up your signing key] with git.

We do suggestion you run `git config --global commit.gpgsign true` to ensure git will always sign your commits when you make them.

### Branch Naming

In general, when naming a branch they should follow the `$type/[$function]/$name` pattern.

First the `$type` section of the branch name is what this branch is trying to do, for example, if it's to add a feature then `$type` should be `feature`, for a bug fix then `fix` should be used, `docs` if it's for Documentation, and `board` if you're adding a new board.

Next, the `$function` section can be thought of something like a filesystem path segment that describes where this branch is focused, for instance, `lattice/ecp5` if it's related to Lattice Semiconductor ECP5 chips. If the changes are more wide-reaching than a specific sub-section, then this part can be omitted.

Finally, the `$name` section should be a short, but descriptive name for what this branch is doing, it doesn't need to be super detailed, that's what commit messages are for, but something that gives a general idea, like `butterstick-fpga`.

So, to put it all together, the following are good examples of how your branch should be named:

* `fix/xilinx`
* `board/lattice/versa-nx`
* `docs/grammar-fixes`

### Submitting a Pull Request

> [!IMPORTANT]
> Torii Boards uses a [git rebase] based workflow to maintain a linear history and avoid merge commits.

Once your changes are done, tested, and you're happy with them, then now to open a pull request against the Torii Boards repository.

The first step is to ensure your changes are based on-top of the latest changes in the `main` branch. This can be done two ways, the first is to pull the changes to your local clone and then rebase on top of that, or directly rebase against `upstream/main`. The former is recommended as that way you can keep your local repo in-sync with upstream.

For example:

1. Switch from your working branch to `main`: `git switch main`
2. Update the remotes: `git fetch --all --prune`
3. Pull the changes into your local `main`: `git pull upstream`
4. Push the changes back up to your fork so it is updated as well: `git push`
5. Switch back to your working branch: `git switch <branch-name>`
6. Rebase the changes from `main` onto your feature branch: `git rebase -i main`
7. Go through the steps of running the rebase and resolving any conflicts that arise.
8. Once rebased and you've re-tested and are happy with the changes again, push them up to your fork: `git push -f`

After this, run `nox -s lint` in the root of the repository, this will run the code linter and alert you if anything is amiss. This is also run in the CI workflow, and will prevent your pull request from getting merged if it's not happy.

Once your changes are all up to date, make sure that all the tests pass (see the [Testing] section for more info), and then you can then open a [new pull request] against the Torii Boards repository.

Once you've filled out the details about the PR, it will then be reviewed to ensure that it's in line with the various project standards, sometimes you'll nail it the first try, other times there will be feedback and requested changes.

If changes are requested, then go back and address them, where possible use `git commit --fixup=<sha>` to attach the updates back to the commit which they were associated with (this is why having smaller atomic commits is important), once all the feedback items have been addressed, then run a `git rebase -i main --autosquash` to apply the fixups to the commits in question and resolve any merge issues.

Once that is done, then re-push to your fork with a force push and the pull request will automatically re-trigger CI, you can then re-request review on the pull request.

This cycle will continue until all items have been addressed and we're ready to merge it into `main` if it has been approved.

As noted above, we use a `git rebase` based workflow, as such we require that your change branch is always based on the tip of `main`, so we might ask you to rebase it onto `main` prior to merging. This might result in things breaking that were not broken before, and they must be fixed as appropriate.

And with that, you're done! You've contributed to Torii Boards!

## Documentation

> [!IMPORTANT]
> The Torii Boards documentation *used* to be licensed under the same [BSD-2-Clause] license as the source
> code, this has been changed to the [CC-BY-SA 4.0] going forward, however, all the **old**
> contributions are still licensed under the [BSD-2-Clause] until they are re-written or superseded.

The documentation for Torii Boards uses [sphinx] with a few plugins, most notably [MyST], which allows us to use Markdown with some extensions to do the documentation rather than reStructuredText.

When contributing to the Torii Boards documentation there are 2 key places it can be found, the "free text" documentation is located in the [`docs`] directory in the root of the repository and contains all the main markup for the overall layout and contents of the documentation site, where as the API and most library documentation is done via Python doc comments in the relevant source code itself.

The reason it's done this way is to ensure that the docs for the APIs and modules are as close and consistent to the code as possible. When having detached documentation it's much easier for drift to occur.

The general overall guidelines in [development and testing] also apply to any and all documentation changes as well, with the extra details that the final documentation should build and not be broken with any dead links.

To generate a local version of the documentation, run `nox -s build-docs`. This will set up everything needed to build the documentation, and then produce a rendered output result in `build/docs`.

When working on the documentation, having to re-build after every change can be rough. That's where the `nox -s watch-docs` comes in. When run, it will build the initial current version of the docs, then start a local web-server up on `http://127.0.0.1:8000` to view the docs. Whenever you then make a change to any of the files in `docs/`, it will automatically re-build the documentation and then re-load the page opened in the browser.

To check to make sure all links are live, the `nox -s linkcheck-docs` command can be used. This will build the documentation and then check each and every hyperlink found within it to make sure it is reachable. This is also done in CI and is a hard-requirement for the documentation to be deployed, so if any of the links are dead, the documentation will not be updated on the live site.

## AI Usage Policy

Torii USB explicitly does not allow any contributions that were in either whole or in part made using a Generative AI system or agent, such as large language models (LLMs), chatbots, or image generation systems. This ban includes, but is not limited to Copilot, BARD/Gemini, ChatGPT, Claude, llama, DeepSeek, Stable Diffusion, DALL-E, Midjourney, or Devin AI.

This policy covers ***ALL*** parts of this project, including but not limited to code, tests, documentation, metadata, artworks, issues, comments, suggestions, feature requests, discussions, pull requests, and any other possible contributions that can be made to Torii USB.

If you are found to be using such tools when contributing to Torii USB, all of you contributions will be removed if viable, outstanding contributions closed without recourse or review, all future collaboration efforts denied, and you will be banned from contributing to Torii USB and related projects.

No exceptions to this policy will be made.

> [!NOTE]
> It is also recommended to avoid any and all AI tools when asking questions about Torii USB,
> prefer the documentation when available, as well as things such as the discussion forum, or IRC channel.
> These tools often fabricate plausible sounding information that is entirely incorrect, or often subtly
> incorrect and pass it off with confidence, and are thus misleading.

### TL;DR

The use of Generative AI when contributing or interacting with this project is ***EXPLICITLY FORBIDDEN*** with ***NO EXCEPTIONS*** and if you are found to be using it, you will be banned from the project and your contributions removed.

[BSD-2-Clause]: https://spdx.org/licenses/BSD-2-Clause.html
[`LICENSE`]: https://github.com/shrine-maiden-heavy-industries/torii-boards/blob/main/LICENSE
[CC-BY-SA 4.0]: https://creativecommons.org/licenses/by-sa/4.0/
[`LICENSE.docs`]: https://github.com/shrine-maiden-heavy-industries/torii-boards/blob/main/LICENSE.docs
[git repository]: https://github.com/shrine-maiden-heavy-industries/torii-boards
[Code Of Conduct]: https://github.com/shrine-maiden-heavy-industries/torii-boards/blob/main/CODE_OF_CONDUCT.md
[AI Usage Policy]: #ai-usage-policy
[Reporting Issues]: #reporting-issues
[Suggesting A Board]: #suggesting-a-board
[Development and Testing]: #development-and-testing
[Branch Naming]: #branch-naming
[Commit Guidelines]: #commit-guidelines
[Formatting Code]: #formatting-code
[Submitting a Pull Request]: #submitting-a-pull-request
[Documentation]: #documentation
[issue tracker]: https://github.com/shrine-maiden-heavy-industries/torii-boards/issues
[report an issue]: https://github.com/shrine-maiden-heavy-industries/torii-boards/issues
[discussion forum]: https://github.com/shrine-maiden-heavy-industries/torii-boards/discussions
[IRC channel]: https://web.libera.chat/#torii
[`unittest`]: https://docs.python.org/3/library/unittest.html
[`unittest` CLI]: https://docs.python.org/3/library/unittest.html#command-line-interface
[Yosys]: https://github.com/YosysHQ/yosys
[sby]: https://github.com/YosysHQ/sby
[Yices2]: https://yices.csl.sri.com/
[Bitwuzla]: https://bitwuzla.github.io/
[formal verification]: https://en.wikipedia.org/wiki/Formal_verification
[OSS CAD Suite]: https://github.com/YosysHQ/oss-cad-suite-build/tree/main
[nox]: https://nox.thea.codes/
[fork]: https://github.com/shrine-maiden-heavy-industries/torii-boards/fork
[signing commits]: https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits
[setting up your signing key]: https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key
[git rebase]: https://git-scm.com/book/en/v2/Git-Branching-Rebasing
[`docs`]: https://github.com/shrine-maiden-heavy-industries/torii-boards/blob/main/docs
[testing]: #testing
[new pull request]: https://github.com/shrine-maiden-heavy-industries/torii-boards/compare
[sphinx]: https://www.sphinx-doc.org/en/master/
[myst]: https://myst-parser.readthedocs.io/en/latest/
[open a new issue]: https://github.com/shrine-maiden-heavy-industries/torii-boards/issues/new?template=2-board-request.yml
