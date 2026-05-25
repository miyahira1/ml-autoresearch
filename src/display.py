from rich import box
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .constants import (
    COMPETITION_COLORS,
    DEMAND_COLORS,
    NICHES_PER_RUN,
    TREND_COLORS,
    VERDICT_COLORS,
)


def _score_style(score: int) -> str:
    if score >= 8:
        return "bold green"
    if score >= 6:
        return "bold yellow"
    if score >= 4:
        return "bold orange1"
    return "bold red"


def build_results_table(results: list[dict]) -> Table:
    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style="dim",
        header_style="bold white",
        show_lines=True,
        expand=True,
        padding=(0, 1),
    )
    table.add_column("#", style="dim", width=3, no_wrap=True)
    table.add_column("Nicho", min_width=20)
    table.add_column("Score", width=7, no_wrap=True)
    table.add_column("Demanda", width=8, no_wrap=True)
    table.add_column("Compet.", width=8, no_wrap=True)
    table.add_column("Tendencia", width=10, no_wrap=True)
    table.add_column("Margen", width=10, no_wrap=True)
    table.add_column("Veredicto", width=12, no_wrap=True)

    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        verdict = r.get("veredicto", "")
        table.add_row(
            str(i),
            r.get("nicho", ""),
            Text(str(score), style=_score_style(score)),
            Text(r.get("demanda", ""), style=DEMAND_COLORS.get(r.get("demanda", ""), "white")),
            Text(r.get("competencia", ""), style=COMPETITION_COLORS.get(r.get("competencia", ""), "white")),
            Text(r.get("tendencia", ""), style=TREND_COLORS.get(r.get("tendencia", ""), "white")),
            r.get("margen_estimado", ""),
            Text(verdict, style=VERDICT_COLORS.get(verdict, "white")),
        )

    return table


def build_log_panel(logs: list[dict]) -> Panel:
    lines = []
    for log in logs[-24:]:
        t = log.get("type", "info")
        msg = log.get("msg", "")
        if t == "agent":
            lines.append(f"[cyan]🤖 {msg}[/cyan]")
        elif t == "success":
            lines.append(f"[green]✅ {msg}[/green]")
        elif t == "warn":
            lines.append(f"[yellow]⚡ {msg}[/yellow]")
        else:
            lines.append(f"[dim]{msg}[/dim]")

    content = "\n".join(lines) if lines else "[dim]Esperando...[/dim]"
    return Panel(content, title="[bold]Agent Logs[/bold]", border_style="dim", padding=(0, 1))


def build_stats_text(stats: dict) -> str:
    analyzed = stats.get("analyzed", 0)
    excellent = stats.get("excellent", 0)
    good = stats.get("good", 0)
    return (
        f"  Analizados [bold white]{analyzed}[/bold white] / {NICHES_PER_RUN}"
        f"   •   Excelentes [bold green]{excellent}[/bold green]"
        f"   •   Buenos [bold cyan]{good}[/bold cyan]"
    )


def build_layout(results: list[dict], logs: list[dict], stats: dict, status: str) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="stats", size=3),
        Layout(name="body"),
    )

    indicator = "[bold green]● Analizando...[/bold green]" if status == "running" else "[dim]○ Completado[/dim]"
    layout["header"].update(
        Panel(
            f"[bold white]NICHEHUNTER ML ARGENTINA[/bold white]   {indicator}",
            box=box.HEAVY,
            border_style="bright_black",
            padding=(0, 2),
        )
    )

    layout["stats"].update(
        Panel(build_stats_text(stats), box=box.SIMPLE, border_style="dim", padding=(0, 2))
    )

    layout["body"].split_row(
        Layout(name="results", ratio=2),
        Layout(name="logs", ratio=1),
    )

    results_content = (
        build_results_table(results)
        if results
        else Text("\n  Iniciando análisis...", style="dim")
    )
    layout["body"]["results"].update(
        Panel(results_content, title="[bold]Resultados[/bold]", border_style="dim")
    )
    layout["body"]["logs"].update(build_log_panel(logs))

    return layout
