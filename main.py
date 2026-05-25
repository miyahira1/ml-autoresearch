import random
import signal
import time

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live

from src.api import analyze_niche
from src.constants import NICHES_PER_RUN, NICHES_SEED, REQUEST_DELAY_SECS
from src.display import build_layout, build_results_table

load_dotenv()

console = Console()


def main() -> None:
    client = Anthropic()

    results: list[dict] = []
    logs: list[dict] = []
    stats = {"analyzed": 0, "excellent": 0, "good": 0}
    abort = [False]

    def add_log(msg: str, log_type: str = "info") -> None:
        logs.append({"msg": msg, "type": log_type})

    def handle_interrupt(sig, frame) -> None:
        abort[0] = True
        add_log("Análisis interrumpido por el usuario", "warn")

    signal.signal(signal.SIGINT, handle_interrupt)

    selected = random.sample(NICHES_SEED, NICHES_PER_RUN)
    add_log("Iniciando NicheHunter ML Argentina...", "info")
    add_log(f"Seleccionados {NICHES_PER_RUN} nichos para analizar", "info")

    with Live(
        build_layout(results, logs, stats, "running"),
        console=console,
        refresh_per_second=4,
        screen=True,
    ) as live:
        for i, nicho in enumerate(selected):
            if abort[0]:
                break

            add_log(f'Analizando "{nicho}"...', "agent")
            live.update(build_layout(results, logs, stats, "running"))

            result = analyze_niche(client, nicho)

            if result:
                results.append(result)
                results.sort(key=lambda x: x.get("score", 0), reverse=True)

                stats["analyzed"] += 1
                verdict = result.get("veredicto", "")
                if verdict == "EXCELENTE":
                    stats["excellent"] += 1
                elif verdict == "BUENO":
                    stats["good"] += 1

                score = result.get("score", 0)
                add_log(f'"{nicho}" → score {score} [{verdict}]', "success")
            else:
                add_log(f'Error al analizar "{nicho}"', "warn")

            live.update(build_layout(results, logs, stats, "running"))

            if i < len(selected) - 1 and not abort[0]:
                time.sleep(REQUEST_DELAY_SECS)

        add_log("✓ Análisis completado", "success")
        live.update(build_layout(results, logs, stats, "done"))
        time.sleep(2)

    console.print("\n[bold white]RESULTADOS FINALES[/bold white]\n")
    console.print(build_results_table(results))


if __name__ == "__main__":
    main()
