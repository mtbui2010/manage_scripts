import os
from shutil import rmtree
import getpass

def download_update_from_git(git_path, update_dir, git_dir='tmp', select_dirs=None, username=None, password=None):
    print('{} Giting {} and updating {}'.format('+'*10, git_path, update_dir))

    if os.path.exists(git_dir): rmtree(git_dir)
    os.makedirs(git_dir, exist_ok=True)

    if username is None or password is None:
        git_command = 'git clone --recursive {} {}'.format(git_path, git_dir)
    else:
        git_path = git_path.replace('https://', '')
        git_command = 'git clone --recursive https://{}:{}@{} {}'.format(username, password, git_path, git_dir)
    os.system(git_command)
    print('{} downloaded into {}'.format(git_path, git_dir))

    if select_dirs is None:
        cp_source = os.path.join(git_dir, '*')
        os.system('cp -r {} {}'.format(cp_source,update_dir))
        print('{} copied to {}'.format(cp_source, update_dir))
    else:
        for fold in select_dirs:
            cp_source = os.path.join(git_dir, fold, '*')
            cp_dest = os.path.join(update_dir, fold)
            os.makedirs(cp_dest, exist_ok=True)
            os.system('cp -r {} {}'.format(cp_source, cp_dest))
            print('{} copied to {}'.format(cp_source, cp_dest))

    rmtree(git_dir)
    print('{} completed'.format('+' * 5))

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
    select_dirss = [
                    None,
                    None,#['ikeacv',],
                    None,
                    None,#['ttdet',],
                    None,#['ttcv',],
                    None,#['detectron2',],
                    ]

    username=input('Git ID?')
    password = getpass.getpass(prompt = 'Git password?')

    for git_path, update_dir, select_dirs in zip(git_paths, update_dirs, select_dirss):
        download_update_from_git(git_path, update_dir, select_dirs=select_dirs, username=username, password=password)


