# Copyright (C) 2010 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This file is the build configuration for a full Android
# build for grouper hardware. This cleanly combines a set of
# device-specific aspects (drivers) with a device-agnostic
# product configuration (apps).
#

# Inherit from asus sm8250-common
-include device/asus/sm8250-common/BoardConfigCommon.mk

DEVICE_PATH := device/asus/zenfone7

# Bluetooth
BOARD_BLUETOOTH_BDROID_BUILDCFG_INCLUDE_DIR := $(DEVICE_PATH)/bluetooth

# Extra Folders
BOARD_ROOT_EXTRA_FOLDERS += motor_fw1 motor_fw2

# Lineage Health
TARGET_HEALTH_CHARGING_CONTROL_CHARGING_PATH := /sys/class/power_supply/battery/device/smartchg_stop_charging
TARGET_HEALTH_CHARGING_CONTROL_CHARGING_ENABLED := 0
TARGET_HEALTH_CHARGING_CONTROL_CHARGING_DISABLED := 1

#HIDL
DEVICE_FRAMEWORK_COMPATIBILITY_MATRIX_FILE += $(DEVICE_PATH)/manifest/vendor_framework_compatibility_matrix.xml
DEVICE_MANIFEST_FILE += $(DEVICE_PATH)/manifest/manifest.xml
DEVICE_MATRIX_FILE += $(DEVICE_PATH)/manifest/compatibility_matrix.xml

# Kernel
TARGET_KERNEL_SOURCE := kernel/asus/sm8250
TARGET_KERNEL_CONFIG := vendor/zf7_defconfig

# Kernel Audio Modules
TARGET_MODULE_ALIASES := \
    adsp_loader_dlkm.ko:audio_adsp_loader.ko \
    apr_dlkm.ko:audio_apr.ko \
    bolero_cdc_dlkm.ko:audio_bolero_cdc.ko \
    hdmi_dlkm.ko:audio_hdmi.ko \
    machine_dlkm.ko:audio_machine_kona.ko \
    mbhc_dlkm.ko:audio_mbhc.ko \
    native_dlkm.ko:audio_native.ko \
    pinctrl_lpi_dlkm.ko:audio_pinctrl_lpi.ko \
    pinctrl_wcd_dlkm.ko:audio_pinctrl_wcd.ko \
    platform_dlkm.ko:audio_platform.ko \
    q6_dlkm.ko:audio_q6.ko \
    q6_notifier_dlkm.ko:audio_q6_notifier.ko \
    q6_pdr_dlkm.ko:audio_q6_pdr.ko \
    rx_macro_dlkm.ko:audio_rx_macro.ko \
    snd_event_dlkm.ko:audio_snd_event.ko \
    stub_dlkm.ko:audio_stub.ko \
    swr_ctrl_dlkm.ko:audio_swr_ctrl.ko \
    swr_dlkm.ko:audio_swr.ko \
    tfa9874_dlkm.ko:audio_tfa9874.ko \
    tx_macro_dlkm.ko:audio_tx_macro.ko \
    usf_dlkm.ko:audio_usf.ko \
    va_macro_dlkm.ko:audio_va_macro.ko \
    wcd938x_dlkm.ko:audio_wcd938x.ko \
    wcd938x_slave_dlkm.ko:audio_wcd938x_slave.ko \
    wcd9xxx_dlkm.ko:audio_wcd9xxx.ko \
    wcd_core_dlkm.ko:audio_wcd_core.ko \
    wsa_macro_dlkm.ko:audio_wsa_macro.ko

# Kernel Wlan Module
TARGET_MODULE_ALIASES += \
    wlan.ko:qca_cld3_qca6390.ko

# Properties
TARGET_PRODUCT_PROP += $(DEVICE_PATH)/product.prop
TARGET_SYSTEM_PROP += $(DEVICE_PATH)/system.prop
TARGET_VENDOR_PROP += $(DEVICE_PATH)/vendor.prop

# Security patch level
VENDOR_SECURITY_PATCH := 2023-05-01

# Sepolicy
BOARD_VENDOR_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/vendor

# inherit from the proprietary version
-include vendor/asus/zenfone7/BoardConfigVendor.mk
