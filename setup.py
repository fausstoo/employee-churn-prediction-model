from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT="-e ."
def get_requirements(file_path:str)->List[str]:
    "This function will return a list of requirements"
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
    return requirements

setup(
    name="Project Name",
    version="0.0.1",
    author="FaustoPF",
    author_email="faustopuchetafortin@gmail.com",
    description="Short project description here",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FaustoPF/project-name",  # (if applicable)
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=get_requirements("requirements.txt"),
)
