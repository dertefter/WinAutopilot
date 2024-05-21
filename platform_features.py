import ctypes

import win32con


class WindowsFeature:
    def get_wallpaper_path(self):
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
        return ubuf.value

    def rgba_to_hex(rgba):
        r, g, b, a = rgba
        return (int(r * 255) << 16) + (int(g * 255) << 8) + int(b * 255)

    def get_screen_resolution(self):
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
