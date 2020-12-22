import os
from shutil import rmtree
import getpass

def upload_to_git(git_path, update_dir, username=None, password=None):
    cwd = os.getcwd()
    if username is not None and password is not None:
        git_path = git_path.replace('https://','')
        git_path = 'https://{}:{}@{}'.format(username, password, git_path)
    git_command = './commit_git.sh -m "commit" -l "{}"'.format(git_path)

    os.chdir(update_dir)
    print(os.getcwd())
    os.system(git_command)
    print('{} completed'.format('+' * 5))
    os.chdir(cwd)

def upload_to_gits_auth(git_paths, update_dirs):
    username = input('Git ID?')
    password = getpass.getpass(prompt='Git password?')

    num_git = len(git_paths)
    for j, git_path, update_dir in zip(range(num_git), git_paths, update_dirs):
        print('{} [{}/{}] Giting push from {} to {}'.format('+' * 10, j, num_git, update_dir, git_path))
        upload_to_git(git_path, update_dir, username=username, password=password)


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

    upload_to_gits_auth(git_paths, update_dirs)



