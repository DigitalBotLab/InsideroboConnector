# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import omni.ext
import carb.settings
from omni.services.browser.asset import get_instance as get_asset_services
from .digitalbotalab import DigitalBotLabAssetProvider
from .constants import SETTING_STORE_ENABLE


class DigitalBotLabAssetProviderExtension(omni.ext.IExt):
    """ Sketchfab Asset Provider extension.
    """

    def on_startup(self, ext_id):
        self._asset_provider = DigitalBotLabAssetProvider()
        self._asset_service = get_asset_services()
        self._asset_service.register_store(self._asset_provider)
        carb.settings.get_settings().set(SETTING_STORE_ENABLE, True)

    def on_shutdown(self):
        self._asset_service.unregister_store(self._asset_provider)
        carb.settings.get_settings().set(SETTING_STORE_ENABLE, False)
        self._asset_provider = None
        self._asset_service = None
