from distutils.core import setup


setup(
    name='beautifullogger',
    packages=['beautifullogger'],
    version='4.7',
    license='MIT',
    description = 'A very simple log formatter for the logging module that can be used as is',
    description_file = "README.md",
    author="Julien Braine",
    author_email='julienbraine@yahoo.fr',
    url='https://github.com/JulienBrn/BeautifulLogger',
    download_url = 'https://github.com/JulienBrn/BeautifulLogger.git',
    package_dir={'': 'src'},
    keywords=['python',  'logging'],
    install_requires=['colorama', 'requests'],
)