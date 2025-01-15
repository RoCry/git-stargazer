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
Repository: {repo_data["full_name"]}
Description: {repo_data.get("description", "No description")}
Recent commits: {len(commits)}

Commit details:
{commits_str}

Please generate `<EXACTLY ONE emoji> <minimalistic title with no more than 80 characters>` to summarize the recent commit messages above.
If nothing meaningful, just return `NONE`.
        """

        lines = commits_str.split("\n")
        commits_compact_str = (
            "\n".join(lines)
            if len(lines) < 5
            else "\n".join(lines[:2]) + f"\n... and {len(lines) - 2} more commits ..."
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

        # Filter active repos
        active_repos = [repo for repo in json_report["repos"] if repo["commit_count"] > 0 and repo["summary"]]
        
        # Count topic frequencies
        topic_counts = {}
        for repo in active_repos:
            for topic in repo.get("topics", []):
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Assign repos to topics
        topic_repos = {}
        for repo in active_repos:
            topics = repo.get("topics", [])
            if not topics:
                main_topic = "Other"
            else:
                # Find most frequent topic for this repo
                main_topic = max(topics, key=lambda t: topic_counts.get(t, 0))
                # If topic only has one repo, move to Other
                if topic_counts[main_topic] == 1:
                    main_topic = "Other"
                    
            if main_topic not in topic_repos:
                topic_repos[main_topic] = []
            topic_repos[main_topic].append(repo)
        
        # Sort topics and repos
        sections_md = []
        sorted_topics = sorted(topic_repos.keys())
        if "Other" in sorted_topics:
            sorted_topics.remove("Other")
            sorted_topics.append("Other")
        
        for topic in sorted_topics:
            repos = topic_repos[topic]
            repos.sort(key=lambda x: x["name"].lower())
            
            sections_md.append(f"\n## {topic}")
            for repo in repos:
                section_md = f"- [{repo['name']}]({repo['url']}/commits) {repo['commit_count']}: {repo['summary']}"
                sections_md.append(section_md)

        return (
            "# Recent Activity in Starred Repositories\n"
            f"_Tracking {json_report['active_repos_count']}/{json_report['total_repos_count']} "
            f"repos with {json_report['total_commits_count']} new commits_\n"
            + "\n".join(sections_md)
        )
