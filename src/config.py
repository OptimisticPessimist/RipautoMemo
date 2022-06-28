from dataclasses import dataclass


@dataclass
class Config:
    db: str = "sqlite:///ripauto_memo.sqlite3"
    root: str = "/html/memo.html"
    monitor_size: tuple[int, int] = (850, 650)
    port: int = 8080
    debug: bool = False


@dataclass
class TestConfig:
    db: str = "sqlite:///test.sqlite3"
    root: str = "/html/memo.html"
    monitor_size: tuple[int, int] = (850, 650)
    port: int = 8050
    debug: bool = True
