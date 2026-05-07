"""
plasma_checker — a CLI wrapper around pytest + Playwright.
 
Usage:
    python plasma_checker.py [OPTIONS] [TESTS...]
 
Examples:
    python plasma_checker.py                              # run all tests, chromium
    python plasma_checker.py tests/test_login.py          # run a specific file
    python plasma_checker.py -k "login" --browser firefox # filter by name, firefox
    python plasma_checker.py -m smoke --headless          # smoke suite, headless
    python plasma_checker.py --list                       # list collected tests
"""
 
import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from utils.logger import configure_logging, get_logger
 
logger = get_logger(__name__)

 
def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="plasma_checker",
        description="Plasma Checker — Playwright test runner built on pytest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
 
    # ── Test selection ────────────────────────────────────────────────────────
    parser.add_argument(
        "tests",
        nargs="*",
        help="Test files, directories, or node IDs to run (default: current directory)",
    )
    parser.add_argument(
        "-k",
        dest="keyword",
        metavar="EXPR",
        help="Only run tests matching the given substring expression (passed to pytest -k)",
    )
    parser.add_argument(
        "-m",
        dest="marker",
        metavar="MARKER",
        help="Only run tests with the given pytest marker (e.g. smoke, regression)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List collected tests without running them (pytest --collect-only)",
    )
 
    # ── Browser options ───────────────────────────────────────────────────────
    parser.add_argument(
        "--browser",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to use (default: chromium)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode",
    )

 
    # ── Output / reporting ────────────────────────────────────────────────────
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Minimal output",
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "STEP", "WARNING", "ERROR"],
        help="Plasma Checker log level (default: INFO)",
    )
    parser.add_argument(
        "--log-dir",
        default="plasma_checker_logs/",
        metavar="PATH",
        help="Directory to save log files (default: none)",
    )
    parser.add_argument(
        "--html-report",
        metavar="PATH",
        help="Write an HTML report to PATH (requires pytest-html)",
    )
    parser.add_argument(
        "--screenshot",
        choices=["on", "off", "only-on-failure"],
        default="only-on-failure",
        help="When to capture screenshots (default: only-on-failure)",
    )
 
    # ── Execution control ─────────────────────────────────────────────────────
    parser.add_argument(
        "-x", "--exitfirst",
        action="store_true",
        help="Stop after the first failure",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=0,
        metavar="N",
        help="Retry failed tests N times (requires pytest-rerunfailures)",
    )
    parser.add_argument(
        "-n", "--workers",
        type=int,
        default=1,
        metavar="N",
        help="Number of parallel workers (requires pytest-xdist)",
    )
 
    return parser
 
 
def build_pytest_command(args: argparse.Namespace) -> list[str]:
    """Translate plasma_checker args into a pytest argv list."""
    cmd = [sys.executable, "-m", "pytest"]
 
    # Test selection
    if args.tests:
        cmd.extend(args.tests)
    if args.keyword:
        cmd.extend(["-k", args.keyword])
    if args.marker:
        cmd.extend(["-m", args.marker])
    if args.list:
        cmd.append("--collect-only")
 
    # Pass plasma_checker-specific flags through to conftest fixtures
    cmd.extend([f"--browser={args.browser}"])
    if args.headless:
        cmd.append("--headed=false")
 
    # Output
    if args.verbose:
        cmd.append("-v")
    elif args.quiet:
        cmd.append("-q")
    if args.html_report:
        cmd.extend([f"--html={args.html_report}", "--self-contained-html"])
    if args.screenshot:
        cmd.extend([f"--screenshot={args.screenshot}"])
 
    # Execution control
    if args.exitfirst:
        cmd.append("-x")
    if args.retries > 0:
        cmd.extend([f"--reruns={args.retries}"])
    if args.workers > 1:
        cmd.extend(["-n", str(args.workers)])
 
    return cmd
 
 
def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
 
    configure_logging(level=args.log_level, log_dir=None)

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"plasma_{timestamp}.log"

    env = os.environ.copy()
    env["PLASMA_LOG_FILE"] = str(log_file)

    logger.info("plasma_checker starting")
    logger.debug("Parsed args: %s", args)

    cmd = build_pytest_command(args)
    logger.step("Handing off to pytest")
    logger.debug("pytest command: %s", " ".join(cmd))

    pytest_lines = []
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env) as proc:
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            pytest_lines.append(line)

    with open(log_file, "a", encoding="utf-8") as fh:
        fh.write("\n" + "=" * 60 + " PYTEST OUTPUT " + "=" * 60 + "\n")
        fh.writelines(pytest_lines)

    if proc.returncode == 0:
        logger.info("All tests passed ✓")
    else:
        logger.error("Test run finished with failures (exit code %d)", proc.returncode)

    return proc.returncode

 
if __name__ == "__main__":
    sys.exit(main())
