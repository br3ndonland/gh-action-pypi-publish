import os
import pathlib

import yaml

EVENT = os.environ["EVENT"]
REF = os.environ["REF"]
REPO = os.environ["REPO"]


def set_image(event: str, ref: str, repo: str) -> str:
    """Set Docker image name and tag.

    If action run was triggered by a pull request to this repo,
    build image from Dockerfile because it has not been pushed to GHCR,
    else pull image from GHCR
    """
    if event == "pull_request" and "gh-action-pypi-publish" in repo:
        return "../../../Dockerfile"
    else:
        return f"docker://ghcr.io/{repo}:{ref.replace('/', '-')}"


image = set_image(EVENT, REF, REPO)

action = {
    "name": "🏃",
    "description": (
        "Run Docker container to upload Python distribution packages to PyPI"
    ),
    "inputs": {
        "user": {"description": "PyPI user", "required": False},
        "password": {
            "description": "Password for your PyPI user or an access token",
            "required": False,
        },
        "repository-url": {
            "description": "The repository URL to use",
            "required": False,
        },
        "packages-dir": {
            "description": "The target directory for distribution",
            "required": False,
        },
        "verify-metadata": {
            "description": "Check metadata before uploading",
            "required": False,
        },
        "skip-existing": {
            "description": (
                "Do not fail if a Python package distribution"
                " exists in the target package index"
            ),
            "required": False,
        },
        "verbose": {"description": "Show verbose output.", "required": False},
        "print-hash": {
            "description": "Show hash values of files to be uploaded",
            "required": False,
        },
    },
    "runs": {
        "using": "docker",
        "image": image,
        "args": [
            "${{ inputs.user }}",
            "${{ inputs.password }}",
            "${{ inputs.repository-url }}",
            "${{ inputs.packages-dir }}",
            "${{ inputs.verify-metadata }}",
            "${{ inputs.skip-existing }}",
            "${{ inputs.verbose }}",
            "${{ inputs.print-hash }}",
        ],
    },
}

action_path = pathlib.Path(".github/actions/run-docker-container/action.yml")
action_path.parent.mkdir(parents=True, exist_ok=True)

with action_path.open(mode="w", encoding="utf-8") as file:
    yaml.dump(action, file, allow_unicode=True, sort_keys=False)
