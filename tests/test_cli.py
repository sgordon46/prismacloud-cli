import subprocess
import os
import pytest

commands = [
    ["-o", "csv", "policy"],
    ["stats", "vulnerabilities", "--cve", "CVE-2022-0847"],
    ["-o", "json", "policy", "list"],
    ["tags"],
    ["stats", "dashboard"],
    ["-o", "json", "stats", "dashboard"],
    ["cloud", "names"],
    ["cloud", "type"],
    ["--columns", "defendersSummary.host", "stats", "dashboard"]
]


@pytest.mark.parametrize("command", commands, ids=[str(command) for command in commands])
def test_cli_commands(command, benchmark):
    """Test various CLI commands and check if they run successfully."""

    def run_command():
        try:
            result = subprocess.run(["python3", "bin/pc"] + command, capture_output=True, text=True, check=True)
            assert result.returncode == 0
        except subprocess.CalledProcessError as test_error:
            pytest.fail(
                f"Command {' '.join(command)} failed with return code {test_error.returncode} "
                f"and output:\\n{test_error.output}"
            )

    if os.environ.get("SKIP_BENCHMARK") == "1":
        run_command()
    else:
        benchmark(run_command)
