import threading


class Tile_Benchmark_Coordinator:
    def __init__(self, candidate_sizes):
        self.lock = threading.Lock()
        self.results: dict[int, float] = {}
        self.expected_sizes = set(candidate_sizes)
        self.condition = threading.Condition(self.lock)
        self.winning_size: int | None = None

    def report(self, size: int, elapsed: float) -> None:
        with self.condition:
            self.results[size] = elapsed
            self.condition.notify_all()

    def wait_and_get_winner(
        self,
        fallback_size: int = 192,
    ) -> int:
        with self.condition:
            self.condition.wait_for(
                lambda: self.expected_sizes.issubset(self.results),
                timeout=300,
            )

            if self.winning_size is None:
                if self.results:
                    self.winning_size = min(
                        self.results,
                        key=lambda size: self.results[size],
                    )
                else:
                    self.winning_size = fallback_size

            return self.winning_size
