from conans import tools, ConanFile
import os
from shutil import copy

class NxConanFile(ConanFile):

    settings = "os", "compiler", "build_type", "arch"
    extra_options = {"system":[True, False], "root":"ANY"}
    extra_default_options = "system=False", "root="
    exports = "conanfile.py", "nxtools/__init__.py", "nxtools/nx_conan_file.py", "nxtools/retrieve.py"

    def __init__(self, output, runner, settings, conanfile_directory, user=None, channel=None):
        self.options.update(self.extra_options)
        if isinstance(self.default_options, (list, tuple)):
            self.default_options = self.extra_default_options + self.default_options
        elif isinstance(self.default_options, str):
            self.default_options = self.extra_default_options + (self.default_options, )
        super(NxConanFile, self).__init__(output, runner, settings, conanfile_directory, user, channel)


    def package(self):
        if self.options.system:
            return
        self.copy("tools")
        self.copy("*.h", dst="include", src="distr/include")
        self.copy("*.la"   , dst="lib", src="distr/lib")
        self.copy("*.a"    , dst="lib", src="distr/lib")
        self.copy("*.so"   , dst="lib", src="distr/lib")
        self.copy("*.dll"  , dst="lib", src="distr/lib")
        self.copy("*.dylib", dst="lib", src="distr/lib")


    def imports(self):
        if self.options.system:
            return
        self.copy("*.dll"   , dst="bin", src="lib")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so"    , dst="lib", src="lib")


    def package_info(self):
        self.do_package_info()
        self.env_info.PYTHONPATH.append(self.package_folder)
        if self.options.system:
            self.cpp_info.includedirs = []
            self.cpp_info.libdirs = []
            if len(str(self.options.root)) != 0:
                self.cpp_info.includedirs.append(str(self.options.root) + "/include")
                self.cpp_info.libdirs.append(str(self.options.root) + "/lib")


    def build(self):
        if self.options.system:
            return
        self.do_build()


    def source(self):
        if self.options.system:
            return
        self.do_source()


