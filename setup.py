from setuptools import setup
from setuptools_rust import Binding, RustExtension


if __name__ == "__main__":
    setup(
        name="bgpry",
        version="3.0.0",
        rust_extensions=[
            RustExtension("bgpry.bgpr", "bgpr/Cargo.toml", binding=Binding.PyO3)],
        packages=["bgpry"],
        zip_safe=False,
    )
