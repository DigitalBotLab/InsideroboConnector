import omni.ext
import omni.ui as ui


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[insiderobo.license] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class InsideroboLicenseExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[insiderobo.license] insiderobo license startup")

        self._count = 0

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                with ui.HStack():
                    ui.Button("Add", clicked_fn=self.debug)
    
    def debug(self):
        print("[insiderobo.license] insiderobo license debug: ")

    def on_shutdown(self):
        print("[insiderobo.license] insiderobo license shutdown")
