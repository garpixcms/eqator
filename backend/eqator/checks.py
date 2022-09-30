from importlib.util import find_spec
from .helpers import shell_run
from .helpers import print_error
from .helpers import print_ok
from .helpers import print_warning
from .helpers import run_unit_tests
from django.conf import settings
from .helpers import print_default
from .helpers import check_needed
import re


def check_flake(directory: str, verbose: bool, config_file: str, flake: bool, variables_passed: bool) -> int:
    if check_needed(flake, variables_passed):
        print_default(f'Checking style guide with flake8 (see "{config_file}")')
        backend_dir = directory
        cmd = f'flake8 {backend_dir}'
        lines = shell_run(cmd)
        if lines == '':
            print_ok(lines, verbose)
            return 0
        print_error(lines)
        return len(lines.strip().split('\n'))
    return 0


def check_radon(directory: str, verbose: bool, config_file: str, radon: bool, variables_passed: bool) -> int:
    if check_needed(radon, variables_passed):
        print_default(f'Cyclomatic complexity with radon (see "{config_file}")')
        cmd = f'radon cc {directory}'
        lines = shell_run(cmd)
        if lines == '':
            print_ok(lines, verbose)
            return 0
        print_error(lines)
        return len(re.findall(' {4}.*?\n', lines))
    return 0


def check_security_linter(directory: str, verbose: bool, config_file: str, linter: bool,
                          variables_passed: bool) -> int:
    if check_needed(linter, variables_passed):
        print_default(f'Security lint with bandit (only high-severity issues, see "{config_file}")')
        lines = shell_run(f'bandit -r {directory} -lll')  # TODO проверить корректность -lll
        if 'No issues identified' in lines:
            print_ok(lines, verbose)
            return 0
        print_error(lines)
        return lines.count('>> Issue:')
    return 0


def check_migrations(directory: str, verbose: bool, migrations: bool, variables_passed: bool) -> int:
    if check_needed(migrations, variables_passed):
        print_default('Project migrations')
        cmd = f'python3 {directory}/manage.py makemigrations --check --dry-run'
        lines = shell_run(cmd)
        if 'No changes detected' in lines:
            print_ok(lines, verbose)
            return 0
        print_error(lines)
        return 1
    return 0


def check_unit_tests(directory: str, verbose: bool, tests: bool, variables_passed: bool, test_coverage: bool) -> int:
    if check_needed(tests, variables_passed):
        command_pref = 'coverage run ' if check_needed(test_coverage, variables_passed) else ''

        if find_spec('pytest') is not None:
            print_default('Django pytest')
            cmd = 'coverage run -m pytest' if check_needed(test_coverage, variables_passed) else 'pytest'
            lines = shell_run(cmd)
            tests_count: list = re.findall(r'collected (\d+) item', lines)
            passed_count: list = re.findall(r'(\d+) passed', lines)
            skipped_count: list = re.findall(r'(\d+) skipped', lines)

            int_tests_count = int(tests_count[0])
            int_passed = sum(list(map(int, skipped_count)) + list(map(int, passed_count)))
            if int_tests_count == int_passed:
                print_ok(lines, verbose)
                return 0

            print_error(lines)
            return int_tests_count - int_passed
        else:
            print_default('Django unit tests')

            if check_needed(test_coverage, variables_passed):
                shell_run(f'{command_pref}{directory}/manage.py test')

            failures, output = run_unit_tests(())

            if failures:
                print_error(output)
                return int(failures)
            print_ok('', verbose)
            return 0
    return 0


def check_garpix_page_tests(verbose: bool, garpix_page: bool, variables_passed: bool) -> int:
    if 'garpix_page' in settings.INSTALLED_APPS and check_needed(garpix_page, variables_passed):
        print_default('Django unit tests garpix_page')
        failures, output = run_unit_tests(('garpix_page',))

        if failures:
            print_error(output)
            return int(failures)
        print_ok('', verbose)
    return 0


def check_test_coverage(verbose: bool, coverage: bool, variables_passed: bool, test_coverage_report: bool) -> (int, int):
    coverage_result = -1

    if check_needed(coverage, variables_passed):

        print_default('Test coverage')

        cmd = 'coverage report'
        lines = shell_run(cmd)

        result_line: list = re.findall(r'TOTAL[ \d]+ (\d+)%', lines)

        coverage_result = int(result_line[0])

        if coverage_result < getattr(settings, 'TEST_COVERAGE_RATE', 70):
            print_error(lines)
            return 1, coverage_result
        print_ok('', verbose)
        if test_coverage_report:
            print_default(lines)

    return 0, coverage_result


def check_lighthouse(verbose: bool, lighthouse: bool, clear_reports: bool, variables_passed: bool) -> int:
    if check_needed(lighthouse, variables_passed):
        print_default('Lighthouse CI')

        lines = shell_run('lhci collect')

        if 'command not found' in lines:
            if getattr(settings, 'LIGHTHOUSE_CHECK_METHOD', 'warning') == 'error':
                print_error(
                    'You need to install Lighthouse CI to run Lighthouse CI check (look at `Readme.md` for more info)',
                    short_error=True)
                return 1
            print_warning(
                'You need to install Lighthouse CI to run Lighthouse CI check (look at `Readme.md` for more info)')
            return 0
        lines = shell_run('lhci assert')
        if clear_reports:
            shell_run('rm -rf .lighthouseci')
        if 'Assertion failed' in lines:
            print_error(lines)
            return 1
        print_ok(lines, verbose)

    return 0


def check_sentry() -> int:
    print_default('Sentry SDK')
    if find_spec('sentry_sdk') is not None:
        print_ok()
        return 0
    if getattr(settings, 'SENTRY_CHECK_METHOD', 'error') == 'error':
        print_error("Sentry SDK isn't installed", short_error=True)
        return 1
    print_warning("Sentry SDK isn't installed")
    return 0
