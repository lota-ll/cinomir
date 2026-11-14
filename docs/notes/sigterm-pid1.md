# docker stop чекав 10 с (SIGTERM і PID 1)

**Симптом:** `docker stop` одразу після `docker run` — 10.7 с, exit 137; через 3 с після старту — 1 с, exit 0.

**Гіпотеза:** SIGTERM приходить, поки Python імпортує модулі, а uvicorn ще не встановив обробник.
Ядро не застосовує дію за замовчуванням до сигналів PID 1 → сигнал губиться → SIGKILL через 10 с.

**Експеримент:**
| запуск | час | exit |
|---|---|---|
| без init, stop одразу | 10.7 с | 137, у логах немає "Shutting down", застосунок стартував ПІСЛЯ stop |
| `--init`, stop одразу | 0.6 с | 143 |

**Рішення:** tini в образі (`ENTRYPOINT ["/usr/bin/tini", "--"]`), а не `init: true` у Compose,
бо в Kubernetes прапорця `--init` немає. Після виправлення: 0.7 с, exit 143.

**Чому це важливо:** у crash loop і rolling deploy под зупиняють саме під час старту;
без виправлення кожен такий под — +10 с (Docker) / +30 с (Kubernetes, terminationGracePeriodSeconds).
