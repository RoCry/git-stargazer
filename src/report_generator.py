from typing import List, Dict, Optional
import os
from litellm import acompletion, validate_environment
from log import logger


class ReportGenerator:
    def __init__(self, model: str = None, api_key: str = None):
        self.model = model or os.getenv("LLM_MODEL", "deepseek/deepseek-chat")
        check = validate_environment(self.model)
        if not check["keys_in_environment"]:
            raise ValueError(f"Missing keys in environment: {check['missing_keys']}")

    async def generate_repo_summary(self, repo_data: Dict, commits: List[Dict]) -> str:
        """Generate a minimalistic summary for a single repository and its recent commits"""
        if not commits:
            return ""
        # if there's only one commit, just return the message
        if len(commits) == 1:
            return commits[0]["commit"]["message"]

        commits_str = self._format_commits(commits)

        prompt = f"""
Repository: {repo_data['full_name']}
Description: {repo_data.get('description', 'No description')}
Recent commits: {len(commits)}

Commit details:
{commits_str}

Please provide <ONE LINE minimalistic title with ONE emoji> to summarize the recent commit messages above.
If nothing meaningful, just return `NONE`.
        """

        logger.info(
            f"Generating summary for {repo_data['full_name']}, commits:\n{commits_str}"
        )
        response = await acompletion(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content
        if summary == "NONE":
            return ""
        summary = summary.strip()
        # remove start and end quotes/backticks
        summary = summary.strip("`")
        summary = summary.strip('"')
        return summary

    def _format_commits(self, commits: List[Dict]) -> str:
        """Format commits for the prompt"""

        def __simplify_commit(commit: Dict) -> Optional[str]:
            m = commit["commit"]["message"]
            if m.startswith("Merge pull request"):
                return None
            if "\n" in m:
                m = m.split("\n")[0]
            return f"- {m}"

        # only using top 20 commits for now
        return "\n".join(filter(None, map(__simplify_commit, commits[:20])))

    async def generate_full_report(
        self, repos_with_commits: List[tuple[Dict, List[Dict]]]
    ) -> str:
        """Generate a full report for all repositories"""
        sections = []
        total_repos = len(repos_with_commits)
        total_commits = 0
        active_repos = 0

        for repo, commits in repos_with_commits:
            if not commits:
                continue

            total_commits += len(commits)
            active_repos += 1
            summary = await self.generate_repo_summary(repo, commits)
            if not summary:
                logger.info(
                    f"Skipping {repo['full_name']} because the summary is empty"
                )
                continue
            # Add repository metadata
            repo_info = (
                f"## [{repo['full_name']}]({repo['html_url']})\n"
                f"> 🔄 {len(commits)} | 📅 {commits[0]['commit']['committer']['date'] if commits else 'N/A'}\n\n"
                f"{summary}\n"
            )
            sections.append(repo_info)

        return (
            "# Recent Activity in Starred Repositories\n"
            f"_Tracking {active_repos}/{total_repos} repos with {total_commits} new commits_\n\n"
            + (
                "\n".join(sections)
                if sections
                else "No recent activity found in starred repositories."
            )
        )
