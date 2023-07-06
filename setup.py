from setuptools import setup

setup(
    name='summarization',
    version='0.2',
    description='',
    url='',
    packages=['summarization'],
    license='',
    author='Dorina Lakatos, Botond Barta',
    python_requires='',
    install_requires=[
        'setuptools~=68.0.0',
        'datasets~=2.5.1',
        'dateparser~=1.1.1',
        'dotmap~=1.3.30',
        'evaluate~=0.3.0',
        'typing~=3.7.4.3',
        'numpy~=1.23.2',
        'click~=8.0.4',
        'transformers~=4.22.2',
        'tqdm~=4.64.0',
        'tldextract~=3.3.1',
        'beautifulsoup4~=4.11.1',
        'pandas~=2.0.3',
        'pypandoc~=1.8.1',
        'PyYAML~=6.0',
        'warc-knot>=0.2.5',
        'quntoken~=3.1.8',
        'Cython',
        'fasttext',
        'nltk',
        'sentencepiece',
        'protobuf==3.19.6'
    ]
)
