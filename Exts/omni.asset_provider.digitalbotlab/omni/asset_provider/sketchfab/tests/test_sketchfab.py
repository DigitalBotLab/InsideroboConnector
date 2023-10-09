# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import os
from typing import Any
import omni.kit.test
import aiohttp

from unittest.mock import patch
from typing import Dict
from omni.services.browser.asset import SearchCriteria, AssetModel
from ..sketchfab import SketchFabAssetProvider


class MockHeader:
    def __init__(self):
        pass

    def get(self, attr: str, default: Any):
        return default


class MockResponse:
    def __init__(self, json: Dict = {}, data: str = ""):
        self._json = json
        self._data = data
        self.headers = MockHeader()

    @property
    def ok(self):
        return True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def json(self) -> Dict:
        return self._json

    async def read(self) -> str:
        return self._data


class SketchfabTestCase(omni.kit.test.AsyncTestCaseFailOnLogError):
    VALID_USERNAME = "username"
    VALID_PASSWORD = "password"
    VALID_ACCESS_TOKEN = "access_token"
    DOWNLOADED_CONTENT = "abc def"

    def _mock_aiohttp_post_impl(self, url: str, params: Dict = None):
        import carb.settings
        from ..constants import SETTING_ROOT

        settings = carb.settings.get_settings()
        if url == settings.get_as_string(SETTING_ROOT + "accessTokenUrl"):
            # Auth endpoint
            if params["username"] == self.VALID_USERNAME and params["password"] == self.VALID_PASSWORD:
                return MockResponse(json={"access_token": self.VALID_ACCESS_TOKEN})
            else:
                return MockResponse(json={"error": "invalid_grant", "error_description": "Invalid credentials given."})
        return MockResponse(json={})

    def _mock_aiohttp_get_impl(self, url: str, headers: Dict = None):
        if headers is not None:
            self.assertTrue(self.VALID_ACCESS_TOKEN in headers["Authorization"])
        if url.endswith("download"):
            return MockResponse(json={"usdz": {"url": url.split("?")[0]}})
        else:
            return MockResponse(data=self.DOWNLOADED_CONTENT)

    async def _mock_write_file_impl(self, url: str, buffer):
        return omni.client.Result.OK

    # NOTE: this test is disabled by default to avoid reaching out to Turbosquid continiously during our tests.
    async def notest_search_no_criteria(self):
        """Test listing first page assets."""
        store = SketchFabAssetProvider()

        RESULTS_COUNT = 50

        (result, *_) = await store.search(search_criteria=SearchCriteria(), search_timeout=60)
        self.assertEqual(len(result), RESULTS_COUNT)

    async def test_authentication_succeeds(self):
        """Test listing first page assets."""
        under_test = SketchFabAssetProvider()
        username = self.VALID_USERNAME
        password = self.VALID_PASSWORD
        with patch.object(aiohttp.ClientSession, "post", side_effect=self._mock_aiohttp_post_impl):
            await under_test.authenticate(username, password)

        self.assertTrue(under_test.authorized())

    async def test_authentication_fails(self):
        """Test listing first page assets."""
        under_test = SketchFabAssetProvider()
        username = self.VALID_USERNAME
        password = "invalid_password"
        with patch.object(aiohttp.ClientSession, "post", side_effect=self._mock_aiohttp_post_impl):
            await under_test.authenticate(username, password)

        self.assertFalse(under_test.authorized())

    async def test_download_succeeds(self):
        """Test listing first page assets."""
        under_test = SketchFabAssetProvider()
        username = self.VALID_USERNAME
        password = self.VALID_PASSWORD
        with patch.object(aiohttp.ClientSession, "post", side_effect=self._mock_aiohttp_post_impl):
            await under_test.authenticate(username, password)

        with patch.object(aiohttp.ClientSession, "get", side_effect=self._mock_aiohttp_get_impl):
            with patch("omni.client.write_file_async", side_effect=self._mock_write_file_impl) as mock_write_file:
                asset = AssetModel(
                    identifier="1c54053d-49dd-4e18-ba46-abbe49a905b0",
                    name="car-suv-1",
                    version="1.0.1-beta",
                    published_at="2020-12-15T17:49:22+00:00",
                    categories=["/vehicles/cars/suv"],
                    tags=["vehicle", "cars", "suv"],
                    vendor="NVIDIA",
                    download_url="https://acme.org/downloads/vehicles/cars/suv/car-suv-1.usdz?download",
                    product_url="https://acme.org/products/purchase/car-suv-1",
                    price=10.99,
                    thumbnail="https://images.com/thumbnails/256x256/car-suv-1.png",
                )
                dest_url = "C:/Users/user/Downloads"
                results = await under_test.download(asset, dest_url)

                expected_filename = os.path.basename(asset.download_url.split("?")[0])
                expected_url = f"{dest_url}/{expected_filename}"
                mock_write_file.assert_called_once_with(expected_url, self.DOWNLOADED_CONTENT)

                self.assertEqual(results["status"], omni.client.Result.OK)
                self.assertEqual(results["url"], expected_url)
