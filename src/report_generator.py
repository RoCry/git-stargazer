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

        lines_of_commits = self._format_commits(commits)

        # if there's only one commit, just return the message
        if len(lines_of_commits) == 1:
            return lines_of_commits[0]

        bullet_commits_str = "\n".join([f"- {c}" for c in lines_of_commits])

        prompt = f"""
Repository: {repo_data["full_name"]}
Description: {repo_data.get("description", "No description")}
Recent commits: {len(commits)}

Commit details:
{bullet_commits_str}

Please generate `<EXACTLY ONE emoji> <minimalistic title with no more than 80 characters>` to summarize the recent commit messages above.
If nothing meaningful, just return `NONE`.
        """

        commits_compact_str = (
            "\n".join(lines_of_commits)
            if len(lines_of_commits) < 5
            else "\n".join(lines_of_commits[:2])
            + f"\n... and {len(lines_of_commits) - 2} more commits ..."
        )
        logger.info(
            f"Generating summary for {repo_data['full_name']}, commits:\n{commits_compact_str}"
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

    def _format_commits(self, commits: List[Dict]) -> List[str]:
        """Format commits for the prompt"""

        def __simplify_commit(commit: Dict) -> Optional[str]:
            m = commit["commit"]["message"]
            if m.startswith("Merge pull request"):
                return None
            if "\n" in m:
                m = m.split("\n")[0]
            return m

        # only using top 20 commits for now
        return list(filter(None, map(__simplify_commit, commits[:20])))

    async def generate_report_json(
        self,
        repos_with_commits: List[tuple[Dict, List[Dict]]],
        including_inactive: bool = True,
    ) -> Dict:
        """Generate a report data dictionary for all repositories"""
        repo_data_list = []
        total_repos_count = len(repos_with_commits)
        total_commits_count = 0
        active_repos_count = 0

        for repo, commits in repos_with_commits:
            if not commits and not including_inactive:
                continue

            total_commits_count += len(commits)
            active_repos_count += 1
            summary = await self.generate_repo_summary(repo, commits)

            item = {
                "name": repo["full_name"],
                "url": repo["html_url"],
                "commit_count": len(commits),
                "summary": summary,
            }
            if repo["topics"]:
                item["topics"] = repo["topics"]

            repo_data_list.append(item)

        return {
            "total_repos_count": total_repos_count,
            "active_repos_count": active_repos_count,
            "total_commits_count": total_commits_count,
            "repos": repo_data_list,
        }

    @staticmethod
    def merge_reports(left: Dict, right: Dict) -> Dict:
        """Merge two report dictionaries"""
        logger.info(
            f"Merging reports: {left['total_repos_count']} and {right['total_repos_count']}"
        )
        return {
            "total_repos_count": left["total_repos_count"] + right["total_repos_count"],
            "active_repos_count": left["active_repos_count"]
            + right["active_repos_count"],
            "total_commits_count": left["total_commits_count"]
            + right["total_commits_count"],
            "repos": left["repos"] + right["repos"],
        }

    @staticmethod
    def json_report_to_markdown(json_report: Dict) -> str:
        """Generate markdown report from report data dictionary"""
        if not json_report["repos"]:
            return "# Recent Activity in Starred Repositories\nNo recent activity found in starred repositories."

        active_repos = [
            r for r in json_report["repos"] if r["commit_count"] > 0 and r["summary"]
        ]
        topic_freq = {}
        topic_groups = {"Other": {"repos": [], "topics": set()}}
        processed = set()

        # Build topic frequency map, excluding 'hacktoberfest'
        for repo in active_repos:
            for topic in repo.get("topics", []):
                if topic != "hacktoberfest":
                    topic_freq[topic] = topic_freq.get(topic, 0) + 1

        # Group repositories by common topics
        for i, repo in enumerate(active_repos):
            if repo["name"] in processed:
                continue

            topics = set(t for t in repo.get("topics", []) if t != "hacktoberfest")
            if not topics:
                topic_groups["Other"]["repos"].append(repo)
                processed.add(repo["name"])
                continue

            similar = [repo]
            shared_topics = topics.copy()

            for other in active_repos[i + 1 :]:
                if other["name"] not in processed and other.get("topics"):
                    other_topics = set(other["topics"])
                    if shared_topics & other_topics:
                        similar.append(other)
                        shared_topics &= other_topics
                        processed.add(other["name"])

            group_key = (
                "Other"
                if len(shared_topics) == 0 or len(similar) == 1
                else ", ".join(sorted(shared_topics, key=lambda t: (-topic_freq[t], t)))
            )

            if group_key not in topic_groups:
                topic_groups[group_key] = {"repos": [], "topics": shared_topics}
            topic_groups[group_key]["repos"].extend(similar)
            processed.add(repo["name"])

        # Generate markdown content
        sections = []
        groups = sorted(k for k in topic_groups if k != "Other") + ["Other"]

        for group in groups:
            repos = sorted(
                topic_groups[group]["repos"],
                key=lambda x: (-x["commit_count"], x["name"].lower()),
            )

            header = (
                f"\n## {group}"
                if group == "Other"
                else f"\n## {', '.join(f'[{t}](https://github.com/topics/{t})' for t in group.split(', '))}"
            )
            sections.append(header)

            sections.extend(
                f"- [{r['name']}]({r['url']}) [{r['commit_count']}]({r['url']}/commits): {r['summary']}"
                for r in repos
            )

        return (
            "# Recent Activity in Starred Repositories\n"
            f"_{json_report['active_repos_count']} active repos with {json_report['total_commits_count']} new commits_\n"
            + "\n".join(sections)
        )
