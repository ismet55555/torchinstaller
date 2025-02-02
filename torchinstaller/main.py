from pathlib import Path
from rich import print
import argparse

from .utils import (
    loadConfig,
    availableCudaVersions,
    getPythonVersion,
    getSystemPlatform,
    getCudaVersion,
    getCommandForPlatform,
    handlePyGCommand,
    handleTorchCommand,
    handleLightningCommand,
)


def main():
    configPath = Path(__file__).parent / "config" / "commands.toml"
    config = loadConfig(configPath)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pytorch",
        "-pt",
        help=(
            "Flag to install pytorch, can optionally specify a desired version."
            " Must be full semantic version, e.g. 1.13.1, not 1.13, defaults to `latest`"
        ),
        nargs="?",
        const="latest",
    )
    parser.add_argument
    parser.add_argument(
        "--pyg",
        "-pyg",
        help="Flag to install pytorch-geometric",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--pyg-lib-source",
        "-pyg-src",
        help=(
            "Flag to install PyG from source. i.e. PyG doesn't support wheels for M1/M2 macs."
            " They recommend installing from source"
        ),
        default=False,
        action="store_true",
        dest="pyg_lib_source",
    )
    parser.add_argument(
        "--compute-platform",
        "-c",
        type=str,
        default=None,
        dest="compute_platform",
        choices=availableCudaVersions(config),
        help=(
            "Manually specify platform version (cuda or rocm) instead of"
            "auto-detect (useful for cluster installations)."
        ),
    )
    parser.add_argument(
        "--lightning",
        "-l",
        action="store_true",
        help="Flag to install lightning (lightning.ai)",
        default=False,
    )
    parser.add_argument(
        "--use",
        "-u",
        default="pip",
        choices=["pip", "conda", "mamba"],
        help="set command to install with.",
    )
    parser.add_argument(
        "-install",
        "-i",
        default=False,
        action="store_true",
        help="Run installation (default is to dry run commands)",
    )

    parser.add_argument(
        "--sync",
        "-s",
        help="update installation commands by parsing the pytorch website",
        default=False,
        action="store_true",
    )

    try:
        args, unk = parser.parse_known_args()
    except Exception as e:
        print("-" * 80)
        print("[red bold]Argument Error")
        print(e)
        print("-" * 80)
        exit(0)

    installer = args.use

    # LATEST_VERSION = "2.2.0"

    if args.sync:
        print("[bold red]Syncing commands")
        from ._parse import parse_commands
        parse_commands()
        print("[bold green]Sync complete")
        config = loadConfig(configPath)
        exit(0)

    if installer in ["conda", "mamba"]:
        command_key = "conda"
    elif installer in ["pip", "poetry"]:
        command_key = "pip"
    else:
        raise NotImplementedError("Unsupported installer")

    getPythonVersion()
    system_platform = getSystemPlatform()

    platform, detected = getCudaVersion(availableCudaVersions(config))

    print("-" * 100)
    if system_platform == "darwin":
        detected = "macos"
        
    if args.compute_platform is None:
        print(f"System platform: [blue bold]{detected}[/blue bold]\nUsing platform: [red bold]{platform}")
        platform = detected
    else:
        platform = args.compute_platform
        print(f"User specified platform: [yellow bold]{platform}")
        print(f"System platform: [blue bold]{detected}[/blue bold]\nUsing platform: [blue bold]{platform}")

    if platform in ["cpu"]:
        print("[yellow bold]CPU ONLY")
    elif platform in ["macos"]:
        print("\n[yellow bold]macOS (pytorch 2.0 supports apple silicon)\n")

    print("-" * 100)

    try:
        if args.pytorch is not None:
            command = getCommandForPlatform(config, command_key, args.pytorch, platform)
            handleTorchCommand(installer, command, args.install)

        if args.lightning:
            handleLightningCommand(installer, args.install)

        if args.pyg:
            handlePyGCommand(installer, args.pytorch, platform, args.pyg_lib_source, args.install)

        if not any([args.pytorch, args.lightning, args.pyg]):
            print("[red bold]NO COMMANDS Selected")
            print("[green bold]Run torchinstall -h to see flags for installing")

    except Exception as err:
        print("Install failed")
        print(f"{err}")
        raise err
    print("-" * 100)


if __name__ == "__main__":
    main()
