from setuptools import setup

setup(
    name='beets-syncpl',
    version='0.1.0-beta',
    description='beets plugin to sync certain music files to a folder',
    author='Laurent De Marez',
    author_email='laurent@demarez.org',
    license='MIT',
    platforms='ALL',

    packages=['beetsplug'],

    install_requires=['beets>=1.3.0'],

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
