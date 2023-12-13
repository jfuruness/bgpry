from setuptools import setup
from setuptools_rust import Binding, RustExtension


if __name__ == "__main__":
    setup(
        name="bgpry",
        version="3.0.0",
        rust_extensions=[
            RustExtension(
                "bgpry.bgpr",
                "bgpr/Cargo.toml",
                binding=Binding.PyO3,
                # Set to True for a debug build
                debug=False
            )],
        packages=["bgpry"],
        zip_safe=False,
        include_package_data=True,
    )
