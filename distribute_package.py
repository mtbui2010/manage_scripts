from make_binary_package import make_binary_package
import getopt, sys, os

PKG_DIR = '/mnt/workspace/000_demo_packaging'
PKG_NAME = 'ketitestlib'
REBINARY = True
MAKE_PYI = True
CHANGE = 'bug'

def distribute_protect_package_pypi(pkg_dir, pkg_name='', rebinarize=True, make_pyi=True, change='Bug'):
    cwd = os.getcwd()
    os.chdir(pkg_dir)
    # check version
    version_file = 'VERSION'
    if not os.path.exists(version_file): version='1.0.0'
    else: f = open(version_file, 'r'); version=f.read().replace('\n', ''); f.close(); os.remove(version_file)
    print(f'{"+" * 10} package {pkg_name}: current version {version}')

    # upgrade version
    major, minor, bug = [int(p) for p in version.split('.')]
    if change.lower()=='major': major+=1
    if change.lower()=='minor': minor+=1
    if change.lower()=='bug': bug+=1
    version = f'{major}.{minor}.{bug}'
    f = open(version_file, 'w'); f.write(version); f.close()
    print(f'{"+" * 10} change to version {version}')

    make_binary_package(pkg_dir=pkg_dir,pkg_name=pkg_name, rebinarize=rebinarize, make_pyi=make_pyi)

    os.chdir(f'{pkg_dir}_binary')
    os.system('python3 -m twine upload dist/*')
    print(f'{"+" * 10} package {pkg_name}_v{version} uploaded to pypi >> "pip install {pkg_name}" to install')


    os.chdir(cwd)

def get_args(argv):
    options = ['p', 'n', 'b', 'i', 'c']
    describes = ['package_path[str]', 'package_name[str]', 'rebinarize[True/False]',
                 'make_pyi[True/False]', 'change[Major/Minor/Bug]']
    default_values = [None, '', True, True, 'Bug']
    requires = ['p']

    #
    opt_str = 'h'
    for p in options: opt_str += f'{p}:'
    usage_guide = 'python3 distribute_package.py'
    for o,d in zip(options, describes): usage_guide += f' -{o} <{d}>'
    args=dict()
    for o,v in zip(options, default_values): args.update({o: v})

    try: opts, _ = getopt.getopt(argv, opt_str)
    except getopt.GetoptError:
        print(usage_guide)
        exit()

    opts1 = [opt[1:] for opt, v in opts]
    for r in requires:
        if r not in opts1:
            print(usage_guide)
            exit()

    for opt, v in opts: args[opt[1:]] = v

    return args

if __name__ == "__main__":
    # args = get_args(sys.argv[1:])
    # distribute_package_pypi(pkg_dir=args['p'], pkg_name=args['n'],rebinarize=args['b'],
    #                         make_pyi=args['i'], change=args['c'])

    distribute_protect_package_pypi(pkg_dir=PKG_DIR, pkg_name=PKG_NAME, rebinarize=REBINARY,
                            make_pyi=MAKE_PYI, change=CHANGE)

