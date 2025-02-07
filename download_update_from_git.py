import os
from shutil import rmtree
import getpass

def download_update_from_git(git_path, update_dir, git_dir='tmp', ignores=None, username=None, password=None):

    if os.path.exists(git_dir): rmtree(git_dir)
    os.makedirs(git_dir, exist_ok=True)

    if username is None or password is None:
        git_command = 'git clone --recursive {} {}'.format(git_path, git_dir)
    else:
        git_path = git_path.replace('https://', '')
        git_command = 'git clone --recursive https://{}:{}@{} {}'.format(username, password, git_path, git_dir)
    os.system(git_command)
    print('{} downloaded into {}'.format(git_path, git_dir))

    if ignores is None: ignores = ['.git', '.idea']
    else: ignores += ['.git', '.idea']
    for item in os.listdir(git_dir):
        if item in ignores: continue
        cp_source = os.path.join(git_dir, item)
        cp_dest = update_dir
        os.system('cp -r {} {}'.format(cp_source, cp_dest))
        print('{} copied to {}'.format(cp_source, cp_dest))

    rmtree(git_dir)
    print('{} completed'.format('+' * 5))

def download_update_from_gits_auth(git_paths, update_dirs, ignoress=None):
    if ignoress is None: ignoress = [None]*len(git_paths)

    username = input('Git ID?')
    password = getpass.getpass(prompt='Git password?')

    num_git = len(git_paths)
    for j, git_path, update_dir, ignores in zip(range(num_git), git_paths, update_dirs, ignoress):
        print('{} [{}/{}] Giting {} and updating {}'.format('+' * 10, j, num_git, git_path, update_dir))
        download_update_from_git(git_path, update_dir, ignores=ignores, username=username, password=password)


if __name__=='__main__':
    git_paths = [
                 'https://github.com/mtbui2010/ikea',
                 'https://github.com/KETI-AN/ikeacv',
                 'https://github.com/mtbui2010/ttdet_demo',
                 'https://github.com/mtbui2010/ttdet',
                 'https://github.com/mtbui2010/ttcv',
                 'https://github.com/mtbui2010/detectron2',
                 ]
    update_dirs = [
                   '/mnt/workspace/001_ikea',
                   '/mnt/workspace/001_ikeacv',
                   '/mnt/workspace/000_ttdet_demo',
                   '/mnt/workspace/000_ttdet',
                   '/mnt/workspace/000_ttcv_simple',
                   '/mnt/workspace/000_detectron2',
                   ]


    download_update_from_gits_auth(git_paths, update_dirs)



