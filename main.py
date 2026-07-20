import pygame, sys
from crafting_app import CraftingApp

def main():
    try:
        pygame.init()
        pygame.display.set_caption("PoE2 Mirror Crafter")
        app = CraftingApp()
        app.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
