from setuptools import setup, find_packages

setup(
    name = "cn-treasury-curve",
    version = "0.5",
    packages = find_packages(),
    install_requires=[
        'requests',
        'xlrd',
        'pandas',
        'click'
    ],

    # metadata for upload to PyPI
    author="rainx",
    author_email="i@rainx.cn",
    description="Collection Treasury Curve data from China Bond",
    license="MIT",
    keywords="china bond Treasury curve stock",
    url="https://github.com/rainx/cn_treasury_curve.git",  # project home page, if any

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.xlsx'],
    },
    entry_points={
        'console_scripts': [
            'cn-treasury-curve=cn_treasury_curve.data:save_zipline_file'
        ]
    }
)
