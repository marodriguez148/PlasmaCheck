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
import subprocess
import sys
 
 
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
    cmd.extend([f"--browser-type={args.browser}"])
    if args.headless:
        cmd.append("--headless")
 
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
 
    cmd = build_pytest_command(args)
 
    print(f"[plasma_checker] Running: {' '.join(cmd)}\n")
 
    result = subprocess.run(cmd)
    return result.returncode
 
 
if __name__ == "__main__":
    sys.exit(main())
