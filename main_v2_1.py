from __future__ import annotations

import argparse
from pathlib import Path

from app_v2_1.assembler.configuration_assembler_v2_1 import ConfigurationAssemblerV2_1
from app_v2_1.models import NamingPolicy
from app_v2_1.utils.config_dump import config_dump_payload, write_config_dump


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ActiveThermo configuration assembler v2.1")
    parser.add_argument("--base-path", default=str(Path(__file__).parent), help="Project base path")
    parser.add_argument("--system-file", default="config/00_system/00_system.yaml", help="System YAML path")
    parser.add_argument(
        "--naming-mode",
        default="keep_local_id",
        choices=["keep_local_id", "prefix_parent"],
        help="Entity exported id naming strategy",
    )
    parser.add_argument("--separator", default="_", help="Separator used by naming policy")
    parser.add_argument("--format", default="json", choices=["json", "yaml"], help="Output format")
    parser.add_argument("--output", default="", help="Optional output file path")
    parser.add_argument("--log-mode", default="verbose", choices=["silent", "normal", "verbose"])
    return parser


def main() -> None:
    args = build_parser().parse_args()
    assembled = ConfigurationAssemblerV2_1(
        base_path=Path(args.base_path),
        system_file=args.system_file,
        naming_policy=NamingPolicy(mode=args.naming_mode, separator=args.separator),
        log_mode=args.log_mode,
    ).assemble()

    if args.output:
        output_path = write_config_dump(assembled, Path(args.output), fmt=args.format)
        print(f"\n✅ Configuration dump written to: {output_path}")
    else:
        print(config_dump_payload(assembled, fmt=args.format))


if __name__ == "__main__":
    main()
