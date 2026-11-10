from cinomir.config import Settings


def test_defaults(monkeypatch):
    for name in ("LOG_LEVEL", "ALLOWED_USER_IDS"):
        monkeypatch.delenv(name, raising=False)
    s = Settings.from_env()
    assert s.log_level == "INFO"
    assert s.allowed_user_ids == frozenset()


def test_allowed_user_ids_parsing(monkeypatch):
    monkeypatch.setenv("ALLOWED_USER_IDS", " 42, 7 ,")
    assert Settings.from_env().allowed_user_ids == frozenset({42, 7})
