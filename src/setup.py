import setuptools

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
    'arclia/kerblaxion/assets': [
      "**/*.png",
      "**/*.wav",
      "**/*.mp3",
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
