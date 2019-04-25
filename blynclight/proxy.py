"""
"""

import requests
import json


class Proxy(object):
    """
    """

    def __init__(self, blynclight_url=None):
        """
        """
        self.baseurl = blynclight_url or "http://localhost:8000/blynclight"

    def _call(self, cmd, light_id=None, value=None):
        """
        """
        args = [self.baseurl]

        if light_id or light_id == 0:
            args.append(light_id)

        args.append(cmd)

        if value:
            args.append(value)

        r = requests.get("/".join(map(str, args)))

        return json.loads(r.content.decode("utf-8"))

    @property
    def lights(self):
        """Returns list of available BlyncLights.
        """
        return self._call("status")

    @property
    def status(self, light_id=None):
        """Returns a dictionary of BlyncLight status.
        """
        return self._call("status", light_id)

    def on(self, light_id):
        """:param light_id: integer

        Turns the light associated with light_id on.
        """
        return self._call("on", light_id)

    def off(self, light_id):
        """:param light_id: integer

        Turns the light associated with light_id off.
        """
        return self._call("off", light_id)

    def color(self, light_id, value):
        """:param light_id: integer
        :param value: color specifier ( tuple of ints or int )

        Changes the color of the light associated with light_id.

        """
        if isinstance(value, tuple):
            # convert tuple to string
            value = "0x" + "".join(["{02x}".format(v) for v in value])

        if isinstance(value, int):
            # convert int to hex string
            value = hex(value)

        return self._call("color", light_id, value)

    def red(self, light_id, value):
        """
        """
        return self._call("red", light_id, value)

    def green(self, light_id, value):
        """
        """
        return self._call("green", light_id, value)

    def blue(self, light_id, value):
        """
        """
        return self._call("blue", light_id, value)

    def flash_on(self, light_id):
        raise NotImplementedError("flash_on")

    def flash_off(self, light_id):
        raise NotImplementedError("flash_on")

    def flash_speed(self, light_id, value):
        """
        """
        raise NotImplementedError("flash_speed")
