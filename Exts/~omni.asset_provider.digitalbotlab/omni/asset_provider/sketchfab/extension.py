# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import omni.ext
import carb.settings
import omni.ui as ui
from omni.services.browser.asset import get_instance as get_asset_services
from .sketchfab import SketchFabAssetProvider
from .constants import SETTING_STORE_ENABLE

import asyncio
import aiohttp

class DigitalBotLabAssetProviderExtension(omni.ext.IExt):
    """ Sketchfab Asset Provider extension.
    """

    def on_startup(self, ext_id):
        self._asset_provider = SketchFabAssetProvider()
        self._asset_service = get_asset_services()
        self._asset_service.register_store(self._asset_provider)
        carb.settings.get_settings().set(SETTING_STORE_ENABLE, True)

        self._window = ui.Window("DBL Debug", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                #ui.Label("Prim Path:", width = 100)
                ui.Button("Debug", height = 20, clicked_fn = self.debug)
                ui.Button("Debug", height = 20, clicked_fn = self.debug_token)
                    

    def on_shutdown(self):
        self._asset_service.unregister_store(self._asset_provider)
        carb.settings.get_settings().set(SETTING_STORE_ENABLE, False)
        self._asset_provider = None
        self._asset_service = None

    def debug(self):
        
        async def authenticate():
            params = {"email": "10@qq.com", "password": "97654321abc"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:8000/api/auth/signin", json=params) as response:
                    self._auth_params = await response.json()
                    print("auth_params", self._auth_params)
                    self.token = self._auth_params["token"]

        asyncio.ensure_future(authenticate())
    
    def debug_token(self):
        async def verify_token():
            params = {"token": self.token, "asset": "test"}
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:8000/api/omniverse/download", json=params) as response:
                    response = await response.json()
                    print("response", response)
        
        asyncio.ensure_future(verify_token())