import setuptools

from glob import glob
from pathlib import Path

root_path = Path(__file__).parent
assets_path = root_path.joinpath("arclia", "kerblaxion", "assets")

def find_assets(pattern: str):
  return glob(pattern, root_dir = assets_path, recursive = True)

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="kerblaxion",
  version="0.1.0",
  description="Space Invaders + Galaxian Clone",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_namespace_packages(
    include=["arclia.*"],
  ),
  package_data = {
    'arclia.kerblaxion.assets': [
      *find_assets("**/*.png"),
      *find_assets("**/*.wav"),
      *find_assets("**/*.mp3"),
    ],
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.10',
  install_requires=[
    'pygame>=2.1.2'
  ],
  entry_points={
    "console_scripts": [
      "kerblaxion = arclia.kerblaxion.__main__:main",
    ],
  },
)
