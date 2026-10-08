import pytest

@pytest.fixture(scope="session")
def api_base_url():
    return "https://verzel-store.qa-test-verzel-store.workers.dev/api"

@pytest.fixture(scope="session")
def ui_base_url():
    return "https://verzel-store.qa-test-verzel-store.workers.dev"