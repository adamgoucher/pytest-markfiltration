from setuptools import setup

setup(
    name="pytest-markfiltration",
    packages = ["markfiltration"],
    version = "0.5",
    author = "adam goucher",
    author_email = "adam@element34.ca",
    install_requires = ['pytest>2.0.2'],
    long_description=open('README.txt').read(),
    url='https://github.com/adamgoucher/pytest-markfiltration',
    # the following makes a plugin available to py.test
    entry_points = {
        'pytest11': [
            'markfiltration = markfiltration.markfiltration',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Utilities',
        'Programming Language :: Python',
    ]
)