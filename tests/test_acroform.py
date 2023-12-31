# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import logging

import pytest

import ocrmypdf

from .conftest import check_ocrmypdf

# pylint: disable=redefined-outer-name


@pytest.fixture
def acroform(resources):
    return resources / 'acroform.pdf'


def test_acroform_and_redo(acroform, caplog, no_outpdf):
    with pytest.raises(ocrmypdf.exceptions.InputFileError):
        check_ocrmypdf(acroform, no_outpdf, '--redo-ocr')
    assert '--redo-ocr is not currently possible' in caplog.text


def test_acroform_message(acroform, caplog, outpdf):
    caplog.set_level(logging.INFO)
    check_ocrmypdf(acroform, outpdf, '--plugin', 'tests/plugins/tesseract_noop.py')
    assert 'fillable form' in caplog.text
    assert '--force-ocr' in caplog.text
