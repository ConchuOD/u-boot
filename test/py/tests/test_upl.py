# SPDX-License-Identifier: GPL-2.0+
# Copyright 2024 Google LLC
#
# Test addition of Universal Payload

import os

import pytest
import u_boot_utils

@pytest.mark.boardspec('sandbox_vpl')
def test_upl_handoff(u_boot_console):
    """Test of UPL handoff

    This works by starting up U-Boot VPL, which gets to SPL and then sets up a
    UPL handoff using the FIT containing U-Boot proper. It then jumps to U-Boot
    proper and runs a test to check that the parameters are correct.

    The entire FIT is loaded into memory in SPL (in upl_load_from_image()) so
    that it can be inpected in upl_test_info_norun
    """
    cons = u_boot_console
    ram = os.path.join(cons.config.build_dir, 'ram.bin')
    fdt = os.path.join(cons.config.build_dir, 'u-boot.dtb')

    # Remove any existing RAM file, so we don't have old data present
    if os.path.exists(ram):
        os.remove(ram)
    flags = ['-m', ram, '-d', fdt, '--upl']
    cons.restart_uboot_with_flags(flags, use_dtb=False)

    # Make sure that Universal Payload is detected in U-Boot proper
    output = cons.run_command('upl info')
    assert 'UPL state: active' == output

    # Check the FIT offsets look correct
    output = cons.run_command('ut upl -f upl_test_info_norun')
    assert 'Failures: 0' in output