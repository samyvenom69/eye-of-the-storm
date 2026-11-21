"""Shared HTTP helpers — session factory with retry/backoff."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def make_session(config, retries: int = 2, backoff: float = 0.4,
                 pool_size: int = 32) -> requests.Session:
    """Return a requests.Session preconfigured with:
    - automatic retries on 429/5xx with exponential backoff,
    - connection pooling sized for concurrent workers,
    - the default EOTS headers.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        connect=retries,
        read=retries,
        backoff_factor=backoff,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "HEAD"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=pool_size,
        pool_maxsize=pool_size,
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(config.REQUEST_HEADERS)
    return session
