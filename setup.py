from setuptools import setup

setup(name='b3_investor_auth',
      version='1.0',
      description='B3 Authentication',
      url='',
      author='Leonardo Pache',
      license='MIT',
      packages=['b3_investor_auth'],
      zip_safe=False)


# How to compile and install the package
# from home of project, generate the compiled structure. build/, dist/ and xxx.egg.info
# python3 setup.py bdist_wheel
# if everything ok, install the .whl file in dist/
# python3 -m pip install dist/xxx-0.1-py3-none-any.whl


