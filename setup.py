import os
import setuptools.command.build_py
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

#custom post-installation steps go here:
class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        #nothing else to do
        print("Running setup")
        try:
            os.system("cp pymail/pymail /usr/local/bin")
        except:
            print("Unable to copy to /usr/local/bin -- recommended that you copy the script to this location")


setup(
    cmdclass={
        'install': Install,
    },
    name='PyMail',
    description='PyMail',
    url='https://github.com/genomeorganizer/pymail.git',
    # git+https://github.com/sequencecentral/twitter-bot.git@main#egg=twitterbot
    author='Steve Ayers, Ph.D.',
    author_email='steve@sequencecentral.com',
    # install_requires=[],
    version='1.0.0',
    license='MIT',
    packages=['pymail'],
    # packages = find_packages(),
    # install_requires=[''],
    long_description="PyMail package", #open('README.md').read(),
    # install_requires=[]
)

#to make an egg:
#python setup.py bdist_egg
#egg-info added