from conans import tools, ConanFile
from conans.errors import ConanException
import os
from shutil import copy, rmtree
from tempfile import mkdtemp

class NxConanFile(ConanFile):

    extra_options = {"system":[True, False], "root":"ANY"}
    extra_default_options = "system=False", "root="
    extra_exports = "conanfile.py", "nxtools/__init__.py", "nxtools/nx_conan_file.py"
    exports = extra_exports
    staging_dir = "staging"
    retrieved_files = ()

    def retrieve(self, sha256, locations, saveas):
        vendor_dir = os.getenv("VENDOR_DIR", "~/.vendor")
        for location in locations:
            try:
                if location[:4] == "http":
                    tools.download(location, saveas)
                elif location[:9] == "vendor://":
                    location = '{vendor_dir}/{location}'.format(location=location[9:],
                                                                vendor_dir=vendor_dir)
                    copy(location, saveas)
                else:
                    copy(location, saveas)
                tools.check_sha256(saveas, sha256)
                self.retrieved_files = (self.retrieved_files, saveas)
                break
            except:
                self.output.warn("Failed to retrieve " + location)
                continue
        if not self.retrieved_files:
            raise ConanException("Error retrieving file. All sources failed.")

    def __init__(self, output, runner, settings, conanfile_directory, user=None, channel=None):
        self.options.update(self.extra_options)

        if isinstance(self.default_options, (list, tuple)):
            self.default_options = self.extra_default_options + self.default_options
        elif isinstance(self.default_options, str):
            self.default_options = self.extra_default_options + (self.default_options, )

        self.staging_dir = mkdtemp()

        if isinstance(self.exports, (list, tuple)):
            self.exports = self.extra_exports + self.exports
        elif isinstance(self.exports, str):
            self.exports = self.extra_exports + (self.exports, )

        super(NxConanFile, self).__init__(output, runner, settings, conanfile_directory, user, channel)


    def do_package(self):
        pass

    def package(self):
        if self.options.system:
            self.output.warn("Using system, skipping package()")
            return
        staging_include = "{staging_dir}/include".format(staging_dir=self.staging_dir)
        staging_lib = "{staging_dir}/lib".format(staging_dir=self.staging_dir)
        self.copy(pattern="*",        dst="include", src=staging_include)
        self.copy(pattern="*.la",     dst="lib", src=staging_lib)
        self.copy(pattern="*.a",      dst="lib", src=staging_lib)
        self.copy(pattern="*.so",     dst="lib", src=staging_lib)
        self.copy(pattern="*.so.*",   dst="lib", src=staging_lib)
        self.copy(pattern="*.dll"  ,  dst="lib", src=staging_lib)
        self.copy(pattern="*.dylib*", dst="lib", src=staging_lib)
        self.copy(pattern="*.lib",    dst="lib", src=staging_lib)
        self.do_package()
        rmtree(self.staging_dir)


    def do_imports(self):
        pass

    def imports(self):
        if self.options.system:
            self.output.warn("Using system, skipping imports()")
            return
        self.copy(pattern="*.dll"   , dst="bin", src="bin")
        self.copy(pattern="*.dylib*", dst="bin", src="lib")
        self.copy(pattern="*.so*"  , dst="lib", src="lib")
        self.do_imports()


    def do_package_info(self):
        pass

    def package_info(self):
        self.do_package_info()
        if self.options.system:
            self.cpp_info.includedirs = []
            self.cpp_info.libdirs = []
            if len(str(self.options.root)) != 0:
                self.cpp_info.includedirs.append(str(self.options.root) + "/include")
                self.cpp_info.libdirs.append(str(self.options.root) + "/lib")


    def do_build(self):
        pass

    def build(self):
        if self.options.system:
            self.output.warn("Using system, skipping build()")
            return
        self.do_build()


    def do_source(self):
        pass

    def source(self):
        if self.options.system:
            self.output.warn("Using system, skipping source()")
            return
        self.do_source()


