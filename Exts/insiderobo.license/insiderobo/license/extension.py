import omni.ext
import omni.ui as ui
import omni.usd

from pxr import Sdf
import os
# import omni.kit.window.file

from .params import LICENSE2PATH


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

        self._window = ui.Window("Insiderobo License", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                with ui.HStack(height = 20):
                    ui.Label("Prim Path:", width = 100)
                    self.prim_path_ui = ui.StringField()
                with ui.HStack(height = 20):
                    ui.Label("License Name:", width = 100)
                    self.license_name_ui = ui.StringField()
                    self.license_name_ui.model.set_value("kinova")

                with ui.HStack(height = 20):
                    ui.Label("License Path:", width = 100)
                    # self.license_path_ui = ui.StringField()
                    # self.license_name = self.license_name_ui.model.get_value_as_string()
                    # self.license_path_ui.model.set_value(LICENSE2PATH[self.license_name])  
                
                ui.Button("Add License to Prim", height = 20, clicked_fn=self.add_license)
                
    
    def add_license(self):
        print("adding license")
        stage = omni.usd.get_context().get_stage()
        prim_path = self.prim_path_ui.model.get_value_as_string()
        
        # if the prim path is empty, use the default prim path
        if prim_path == "":
            prim_path = stage.GetDefaultPrim().GetPath().pathString

        self.license_name = self.license_name_ui.model.get_value_as_string()
        license_path = LICENSE2PATH[self.license_name] #self.license_path_ui.model.get_value_as_string()
        prim = stage.GetPrimAtPath(prim_path)

        # load the license file into string
        license_file = open(license_path, "r")
        license_text = license_file.read()

        print("license text: ", license_text)
        
        attribute_name = f"{self.license_name}_license"
        if not prim.HasAttribute(attribute_name):
            # create a new attribute on the prim
            prim.CreateAttribute(attribute_name, Sdf.ValueTypeNames.String, False).Set(license_text)
        
        # save the stage
        omni.usd.get_context().get_stage().Save()

        license_file.close()
        

                    
    def debug(self):
        print("[insiderobo.license] insiderobo license debug: ")

    def on_shutdown(self):
        print("[insiderobo.license] insiderobo license shutdown")
