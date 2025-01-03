#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/asus/zenfone7',
    'vendor/asus/zenfone7',
    'hardware/qcom-caf/sm8250',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
    ): lib_fixup_vendor_suffix,
    (
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('system_ext/etc/permissions/vendor.qti.hardware.data.connection-V1.0-java.xml',
     'system_ext/etc/permissions/vendor.qti.hardware.data.connection-V1.1-java.xml'): blob_fixup()
        .regex_replace('system/product', 'system_ext')
        .regex_replace('xml version="2.0"', 'xml version="1.0"'),
    'vendor/etc/seccomp_policy/qspm.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
    'vendor/lib64/libvendor.goodix.hardware.biometrics.fingerprint@2.1.so': blob_fixup()
        .replace_needed('libhidltransport.so', 'libhidlbase_shim.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .patchelf_version('0_17_2')
        .add_needed('libgui_shim.so'),
    'vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .sig_replace('13 0A 00 94', '1F 20 03 D5'),
}  # fmt: skip

module = ExtractUtilsModule(
    'zenfone7',
    'asus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=False,
)

module.add_proprietary_file('proprietary-files-product.txt')
module.add_proprietary_file('proprietary-files-vendor.txt')

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
