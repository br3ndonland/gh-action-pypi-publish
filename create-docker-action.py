import os
import pathlib

import yaml

DESCRIPTION = 'description'
REQUIRED = 'required'

EVENT = os.environ['EVENT']
REF = os.environ['REF']
REPO = os.environ['REPO']


def set_image(event: str, ref: str, repo: str) -> str:
    if event == 'pull_request' and 'gh-action-pypi-publish' in repo:
        return '../../../Dockerfile'
    docker_ref = ref.replace('/', '-')
    return f'docker://ghcr.io/{repo}:{docker_ref}'


image = set_image(EVENT, REF, REPO)

action = {
    'name': '🏃',
    DESCRIPTION: (
        'Run Docker container to upload Python distribution packages to PyPI'
    ),
    'inputs': {
        'user': {DESCRIPTION: 'PyPI user', REQUIRED: False},
        'password': {
            DESCRIPTION: 'Password for your PyPI user or an access token',
            REQUIRED: False,
        },
        'repository-url': {
            DESCRIPTION: 'The repository URL to use',
            REQUIRED: False,
        },
        'packages-dir': {
            DESCRIPTION: 'The target directory for distribution',
            REQUIRED: False,
        },
        'verify-metadata': {
            DESCRIPTION: 'Check metadata before uploading',
            REQUIRED: False,
        },
        'skip-existing': {
            DESCRIPTION: (
                'Do not fail if a Python package distribution'
                ' exists in the target package index'
            ),
            REQUIRED: False,
        },
        'verbose': {DESCRIPTION: 'Show verbose output.', REQUIRED: False},
        'print-hash': {
            DESCRIPTION: 'Show hash values of files to be uploaded',
            REQUIRED: False,
        },
        'attestations': {
            DESCRIPTION: (
                '[EXPERIMENTAL]'
                ' Enable experimental support for PEP 740 attestations.'
                ' Only works with PyPI and TestPyPI via Trusted Publishing.'
            ),
            REQUIRED: False,
        }
    },
    'runs': {
        'using': 'docker',
        'image': image,
        'args': [
            '${{ inputs.user }}',
            '${{ inputs.password }}',
            '${{ inputs.repository-url }}',
            '${{ inputs.packages-dir }}',
            '${{ inputs.verify-metadata }}',
            '${{ inputs.skip-existing }}',
            '${{ inputs.verbose }}',
            '${{ inputs.print-hash }}',
            '${{ inputs.attestations }}',
        ],
    },
}

action_path = pathlib.Path('.github/actions/run-docker-container/action.yml')
action_path.parent.mkdir(parents=True, exist_ok=True)

with action_path.open(mode='w', encoding='utf-8') as file:
    yaml.dump(action, file, allow_unicode=True, sort_keys=False)
