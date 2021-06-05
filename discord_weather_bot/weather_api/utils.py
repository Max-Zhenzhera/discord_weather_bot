"""
Contains some helper functions.

.. function:: fetch_json_response(session: aiohttp.ClientSession, url: str, params: dict) -> dict
    Return json response parsed in ``dict``
"""

from __future__ import annotations

import aiohttp


async def fetch_json_response(session: aiohttp.ClientSession, url: str, params: dict) -> dict:
    """
    Return json response parsed in ``dict`` by url and GET params.

    :param session: session (to send http requests)
    :type session: aiohttp.ClientSession
    :param url: http url
    :type url: str
    :param params: GET params
    :type params: dict

    :return: response result in ``dict`` representation
    :rtype: dict
    """

    async with session.get(url, params=params) as response:
        json_response = await response.json()

    return json_response
