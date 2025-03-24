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
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/display',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'libAsusMotorDriverHAL',
        'libAsusRGBSensorHAL',
        'libmpbase',
        'libxditk_DIT_Manager',
        'libxditk_ISP',
        'libxditk_arch',
        'libxditk_ditArchLIB',
        'libxditk_ditBSP',
        'libxditk_ditBSP_JNI',
        'libxditk_DIT_MSMv1',
    ): lib_fixup_vendor_suffix,
    (
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('system/lib64/libxditk_ISP.so',
     'system/lib64/libxditk_ditArchLIB.so'): blob_fixup()
        .replace_needed('libOpenCL.so', 'libOpenCL_system.so'),
     'system_ext/lib64/libqti-iopd-client_system.so': blob_fixup()
        .replace_needed('vendor.qti.hardware.iop@2.0.so', 'vendor.qti.hardware.iop@2.0_system.so'),
    'vendor/bin/hw/android.hardware.power-service': blob_fixup()
        .replace_needed('android.hardware.power-V1-ndk_platform.so', 'android.hardware.power-V1-ndk.so'),
    'vendor/etc/msm_irqbalance.conf': blob_fixup()
        .regex_replace('IGNORED_IRQ=27,23,38$', 'IGNORED_IRQ=27,23,38,115,332'),
    'vendor/etc/seccomp_policy/qspm.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
    'vendor/bin/hw/android.hardware.camera.provider@2.4-service_64': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    ('vendor/lib/libqti-perfd.so',
     'vendor/lib64/libqti-perfd.so'): blob_fixup()
        .binary_regex_replace(b'sys.asus.dongletype', b'vendor.sys.asus.dongletype'),
    'vendor/lib64/libvendor.goodix.hardware.biometrics.fingerprint@2.1.so': blob_fixup()
        .replace_needed('libhidltransport.so', 'libhidlbase_shim.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .patchelf_version('0_17_2')
        .add_needed('libcrypto_shim.so'),
    'vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .sig_replace('13 0A 00 94', '1F 20 03 D5'),
}  # fmt: skip

module = ExtractUtilsModule(
    'zenfone7',
    'asus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

module.add_proprietary_file('proprietary-files-product.txt')
module.add_proprietary_file('proprietary-files-vendor.txt')

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
