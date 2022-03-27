from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='Yappy3',
    packages=['Yappy3'],  # this must be the same as the name above
    version='0.2',
    description='Biblioteca yappy convertida a python3. Yappy proporciona un analizador léxico y un generador parser LR para aplicaciones en python.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Álvaro Rodríguez Carpintero',
    author_email='alvaro9rocar@gmail.com',
    # use the URL to the github repo
    url='https://github.com/Alvaro9rc/Yappy3',
    download_url='https://github.com/Alvaro9rc/Yappy3/releases/tag/0.2',
    keywords=['parser', 'yappy'],
    classifiers=[ ],
    license='GNU',
    include_package_data=True
)