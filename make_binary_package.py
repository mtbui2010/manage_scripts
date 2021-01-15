import os
import shutil
from glob import glob
from distutils.dir_util import copy_tree


rebinarize = False
make_pyi = False

def iter_make_pyi(dir_path=''):
    os.system(f'stubgen {os.path.join(dir_path,"*.py")} -o .')

    items = os.listdir(dir_path)
    sub_dirs = [os.path.join(dir_path, p)  for p in items if os.path.isdir(os.path.join(dir_path, p)) and 'cache' not in p]
    if len(sub_dirs)==0: return

    for p in sub_dirs:
        iter_make_pyi(p)


def make_binary_package(pkg_dir, pkg_name='', rebinarize=True, make_pyi=True):
    if not os.path.isdir(pkg_dir):
        print(f'{"+"*10} {pkg_dir} is not a dir >> return')
        return

    bn_pkg_dir = f'{pkg_dir}_binary'
    if rebinarize or make_pyi:
        # if os.path.exists(bn_pkg_dir):
        #     #shutil.rmtree(bn_pkg_dir, ignore_errors=True)
        #     os.system(f'sudo rm -rf {bn_pkg_dir}')
        # shutil.copytree(pkg_dir, bn_pkg_dir)
        os.makedirs(bn_pkg_dir, exist_ok=True)
        copy_tree(pkg_dir, bn_pkg_dir)
        print(f'{"+"*10} {pkg_dir} coppied to {bn_pkg_dir}')

    cwd = os.getcwd()
    os.chdir(bn_pkg_dir)
    print(f'{"+" * 10} change workdir to {bn_pkg_dir}')

    if make_pyi:
        iter_make_pyi(pkg_name)
        print(f'{"+" * 10} .pyi files made for {bn_pkg_dir}')

    if rebinarize:
        os.system('python3 setup.py build_ext --inplace')
        print(f'{"+" * 10} binary files built')

    lib_dir = [p for p in os.listdir('build') if p.startswith('lib.linux')][0]
    lib_dir = os.path.join('build', lib_dir)
    pyifiles = glob(os.path.join(pkg_name, '**/*.pyi'), recursive=True)
    for src in pyifiles: shutil.copyfile(src,os.path.join(lib_dir, src))
    print(f'{"+" * 10} pyi files copied to built lib')

    if os.path.exists('dist'):
        os.system('rm -rf dist/*')
    os.system('python3 setup.py bdist_wheel')
    print(f'{"+" * 10} distribute wheel made')

    wheelfile = glob(os.path.join('dist', '*.whl'))[0]
    os.rename(wheelfile, wheelfile.replace('-linux_', '-manylinux2014_'))
    if os.path.exists(wheelfile): os.remove(wheelfile)
    print(f'{"+" * 10} rename wheel file to support manylinux')

    os.chdir(cwd)
    print(f'{"+" * 10} change workdir to {cwd}')

if __name__=='__main__':
    make_binary_package(pkg_dir='/mnt/workspace/001_kpick', pkg_name='kpick',
                        rebinarize=rebinarize, make_pyi=make_pyi)




















