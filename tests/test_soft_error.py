# SPDX-FileCopyrightText: 2023 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import os

import pytest

from ocrmypdf.exceptions import ExitCode

from .conftest import run_ocrmypdf


def test_raster_continue_on_soft_error(resources, outpdf):
    p = run_ocrmypdf(
        resources / 'francais.pdf',
        outpdf,
        '--continue-on-soft-render-error',
        '--plugin',
        'tests/plugins/tesseract_noop.py',
        '--plugin',
        'tests/plugins/gs_raster_soft_error.py',
    )
    assert p.returncode == ExitCode.ok


def test_raster_stop_on_soft_error(resources, outpdf):
    p = run_ocrmypdf(
        resources / 'francais.pdf',
        outpdf,
        '--plugin',
        'tests/plugins/tesseract_noop.py',
        '--plugin',
        'tests/plugins/gs_raster_soft_error.py',
    )
    assert p.returncode == ExitCode.child_process_error


def test_render_continue_on_soft_error(resources, outpdf):
    p = run_ocrmypdf(
        resources / 'francais.pdf',
        outpdf,
        '--continue-on-soft-render-error',
        '--plugin',
        'tests/plugins/tesseract_noop.py',
        '--plugin',
        'tests/plugins/gs_render_soft_error.py',
    )
    assert p.returncode == ExitCode.ok


@pytest.mark.skipif(os.name == 'nt', reason='Ghostscript on Windows errors out')
def test_render_stop_on_soft_error(resources, outpdf):
    p = run_ocrmypdf(
        resources / 'francais.pdf',
        outpdf,
        '--plugin',
        'tests/plugins/tesseract_noop.py',
        '--plugin',
        'tests/plugins/gs_render_soft_error.py',
    )
    assert p.returncode == ExitCode.child_process_error
