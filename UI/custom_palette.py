class CustomPalette:
    active_palette = None
    passive_palette = None

    @staticmethod
    def setActivePalette(active_palette):
        CustomPalette.active_palette = active_palette

    @staticmethod
    def setPassivePalette(passive_palette):
        CustomPalette.passive_palette = passive_palette