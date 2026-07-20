import pygame, sys
from crafting_app import CraftingApp

__version__ = "0.1.0"


def _get_initial_resolution():
    pygame.init()
    try:
        info = pygame.display.Info()
        dw, dh = info.current_w, info.current_h
        if dw > 0 and dh > 0:
            return dw, dh
    except Exception:
        pass
    return 1280, 800


def _maximize_window():
    try:
        import ctypes
        hwnd = pygame.display.get_wm_info()['window']
        SW_MAXIMIZE = 3
        ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
    except Exception:
        pass


def main():
    try:
        iw, ih = _get_initial_resolution()
        pygame.display.set_caption(f"PoE2 Mirror Crafter v{__version__}")
        import renderer
        renderer.update_layout(iw, ih)
        app = CraftingApp(iw, ih)
        _maximize_window()
        sw, sh = pygame.display.get_surface().get_size()
        renderer.update_layout(sw, sh)
        app.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
