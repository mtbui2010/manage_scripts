import shutil, os
from glob import glob
from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy as np


# +++++++++++++++++++++++++++++++++ CONFIGURATIONS
package_dir = '/mnt/workspace/001_grasp_detection_package'
rebinarize = True
upload_to_git = True
git_msg = 'commit'
git_link = 'https://github.com/mtbui2010/kpick_binary.git'

binary_package_dir = '{}_binary'.format(package_dir)
if rebinarize: remove_git = 'remove_git'
else: remove_git = 'keep_git'

if rebinarize:
    # +++++++++++++++++++++++++++++++++ convert .py to binary
    if os.path.exists(binary_package_dir): shutil.rmtree(binary_package_dir, ignore_errors=True)
    shutil.copytree(package_dir, binary_package_dir)

    py_module_paths = glob(os.path.join(binary_package_dir, '**/*.py'), recursive=True)
    py_dirs = np.unique([os.path.split(path)[0] for path in py_module_paths]).tolist()
    py_dirs.remove(binary_package_dir)


    for py_dir in py_dirs:          # cythonize .py files
        # os.chdir(binary_package_dir)
        os.chdir(py_dir)
        if os.path.exists('__init__.py'): os.remove('__init__.py')
        py_module_paths_ = [p for p in glob('*.py', recursive=True)]
        if len(py_module_paths_)==0: continue

        setup_path = 'setup.py'  # make setup file
        if os.path.exists(setup_path): os.remove(setup_path)
        with open(setup_path, 'w') as f:
            f.write('from setuptools import setup\n')
            f.write('from Cython.Build import cythonize\n')
            f.write('setup(ext_modules = cythonize({}))'.format(py_module_paths_))

        os.system('python3 {} build_ext --inplace'.format(setup_path))
        # os.remove(setup_path)  # remmove setup file
        if os.path.exists('build'): shutil.rmtree('build')
        [os.remove(p) for p in py_module_paths_]



if upload_to_git:
    # +++++++++++++++++++++++++++++++++ updload to git
    os.chdir(binary_package_dir)
    git_command = './commit_git.sh -m "{}" -l "{}" -r "{}"'.format(git_msg, git_link, remove_git)
    print(git_command)
    os.system(git_command)


# # +++++++++++++++++++++++++++++++++ updload to pypi
# os.chdir(pkg_dir)
# os.system('python3 setup.py sdist bdist_wheel')
# os.system('python3 -m twine upload dist/*')


















