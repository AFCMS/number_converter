import math
import re

import click
import rich.console
import rich.table

superscript_number_map = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}


def subscript_number(number: int) -> str:
    return "".join([superscript_number_map[c] for c in str(number)])


def print_decimal_to_base(console: rich.console.Console, number: int, target_base: int):
    table = rich.table.Table(show_header=True, header_style="bold magenta")
    table.add_column("Result", style="dim", width=12)
    table.add_column("Remaining")

    o = []
    while number > 0:
        o.append(number % target_base)
        table.add_row(str(number % target_base), str(number // target_base))
        number = number // target_base

    console.log(o)
    console.log(table)


def print_binary_to_decimal(console: rich.console.Console, binary: str):
    table = rich.table.Table(show_header=True, header_style="bold blue")

    # Validate binary string
    for c in binary:
        assert c in ["0", "1"]

    for i in range(len(binary)):
        table.add_column(binary[i], style="dim")

    # table.add_row(*list(binary))

    table.add_row(
        # "[red]Multiplication[/red]",
        *[
            binary[k] + f"×[red]2" + subscript_number(len(binary) - k - 1)
            for k in range(len(binary))
        ],
        style="bold blue",
        # end_section=True,
    )

    table.add_row(
        *[
            binary[k] + f"×[red]" + str(2 ** (len(binary) - k - 1))
            for k in range(len(binary))
        ],
        style="bold blue",
    )

    table.add_row(
        *[
            str(2 ** (len(binary) - k - 1)) if binary[k] == "1" else "0"
            for k in range(len(binary))
        ],
        style="bold blue",
    )

    console.log("[green]Source Binary:[/green]", f"[blue bold]{binary}[blue]")
    console.log(table)
    console.log(
        "[green]Calculation:[/green]",
        f"[blue bold]{'[green]+[/green]'.join(filter(lambda v: v is not None, [str(2 ** (len(binary) - k - 1)) if binary[k] == '1' else None for k in range(len(binary))]))}",
    )

    console.log(
        "[green]Result:[/green]",
        f"[blue bold]{sum([2 ** (len(binary) - k - 1) if binary[k] == '1' else 0 for k in range(len(binary))])}[blue]",
    )


def print_decimal_to_binary(console: rich.console.Console, number: int):
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Remaining", style="dim", width=12)
    table.add_column("Result", style="dim", width=12)

    console.log("[green]Source Decimal:[/green]", f"[blue bold]{number}[blue]")

    table.add_row(str(number), "")

    result = []
    while number > 0:
        table.add_row(str(number // 2), str(number % 2))
        result.append(number % 2)
        number = number // 2
    result.reverse()
    lr = len(result)
    console.log(table)
    console.log("[green]Result:[/green]", f"[blue bold]{''.join(map(str, result))}")
    console.log("[green]Bits:[/green]", f"[blue bold]{lr}")
    console.log(
        "[green]Bytes:",
        f"ceil({lr}/8) = [blue bold]{math.ceil(lr / 8)}",
    )
    console.log(
        "[green]Result (Bytes):[/green]",
        f"[blue bold]{' '.join(re.findall(r'.'*8,''.join(map(str, [0 for _ in range((math.ceil(lr / 8) * 8) - lr)] + result))))}",
    )
    # '-'.join(re.findall('..', s))


if __name__ == "__main__":
    main_console = rich.console.Console()

    @click.group()
    def cmd():
        pass

    @cmd.command()
    @click.argument("dec", type=str)
    def dec_to_bin(dec: str):
        print_decimal_to_binary(main_console, int(dec))

    @cmd.command()
    @click.argument("b", type=str)
    def bin_to_dec(b: str):
        print_binary_to_decimal(main_console, b)

    cmd()
