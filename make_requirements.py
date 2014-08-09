import optparse
from os.path import abspath, dirname, join #FIXME: bring in path.py
from shutil import rmtree
import subprocess
import sys
from tempfile import mkdtemp

PROJECT_ROOT = abspath(dirname(__file__)) #FIXME: move to same dir as manage.py
PROJECT = lambda *args: join(PROJECT_ROOT, *args)

def run(args):
    parser = optparse.OptionParser(usage="""
    # to bake requirements for dev:
      make_requirements.py freeze --env dev > ../requirements-dev.txt
    # to bake requirements for prod:
      make_requirements.py freeze --env prod > ../requirements.txt
    """)

    if len(args) == 1:
        print parser.usage
        return

    operation = args[1]
    args = args[2:]

    parser.add_options([optparse.make_option('--env',
                        action='store',
                        dest='env',
                        default='dev',
                        help="dev|prod, default dev")])
    opts, args = parser.parse_args(args)

    if operation == 'freeze':
        freeze(opts.env)
    else:
        raise ValueError("No {0} operation".format(operation))

def make_paths(env):
    unpinned = PROJECT("reqs", "{0}.txt".format(env))
    if env == 'prod':
        pinned = PROJECT("requirements.txt".format(env))
    else:
        pinned = PROJECT("requirements-{0}.txt".format(env))

    sandbox = mkdtemp()

    return unpinned, pinned, sandbox

def clean_sandbox(sandbox):
    rmtree(sandbox)

def output_if_failure(*args, **kwargs):
    try:
        return subprocess.check_output(*args, **kwargs)
    except subprocess.CalledProcessError as exc:
        print exc.output
        raise

def freeze(env):
    unpinned, pinned, sandbox = make_paths(env)

    output_if_failure(['virtualenv', '--no-site-packages', sandbox])

    pip_path = join(sandbox, 'bin', 'pip')
    output_if_failure([pip_path, 'install',
                           '--requirement', unpinned])
    print output_if_failure([pip_path, 'freeze',
                            '--requirement', unpinned])
    clean_sandbox(sandbox)

# TODO: Finish this; the update_checker package is crap.
# def check(env):
#     unpinned, pinned, sandbox = make_paths(env)

#     file_names = [basename(unpinned)]
#     file_relative = dirname(unpinned)

#     while file_names:
#         current_file = file_names.pop()
#         with open(join(file_relative, current_file)) as f:
#             contents = f.read().split('\n')

#         for line in contents:
#             if re.search(line, '^ *#'):
#                 continue
#             if line.strip().startswith('-r'):
#                 next_file = re.split('-r', line)[1].strip()
#                 file_names.append(next_file)
#                 continue
#             try:
#                 version, updated_at = requirements_update_checker.check(line)
#             except TypeError:
#                 print "Unable to check {0}".format(line)
#             else:
#                 if str(version) != V('0'):
#                     print "up to date: {0}".format(line)
#                 else:
#                     print "old: {0}, new: {1}, updated {2}".format(line, version, updated_at)

if __name__ == '__main__':
    run(sys.argv)