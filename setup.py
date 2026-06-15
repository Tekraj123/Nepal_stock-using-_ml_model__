
from setuptools import setup, find_packages 


from typing import List


def get_requirements(file_path:str) -> List[str]:
    hypon_e_dot = "-e ."    
    requiresments = []

    with open(file_path) as file_obj:
        requiresment=file_obj.readlines()
        requiresments=[req.replace("\n","") for req in requiresment]

    if hypon_e_dot in requiresments:
        requiresments.remove(hypon_e_dot)

    return requiresments




setup(
    name='end to end ml project',
    version='0.0.1',
    author='TEKRAJ UPADHYAYA',
    author_email='tupadhyaya5@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)

