import asyncio
import os
from datetime import date, datetime, timezone

from commit_feed import CommitFeed
from config import Config
from dotenv import load_dotenv
from github_client import GitHubClient
from log import configure_logging
from pipeline import run_daily
from summarizer import build_summarizer


async def run(config: Config) -> None:
    now = datetime.now(timezone.utc)
    async with GitHubClient(config.github_token) as transport:
        await run_daily(
            config,
            transport=transport,
            commit_feed=CommitFeed(transport, now=lambda: now),
            summarizer=build_summarizer(config.summarizer_model),
            published_at=now,
        )


def main() -> None:
    load_dotenv()
    configure_logging()
    config = Config.from_environment(os.environ, default_date=date.today())
    asyncio.run(run(config))


if __name__ == "__main__":
    main()
