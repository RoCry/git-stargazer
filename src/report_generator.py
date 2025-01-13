from typing import List, Dict
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
        """Generate a summary for a single repository and its recent commits"""
        if not commits:
            return ""

        prompt = f"""
Repository: {repo_data['full_name']}
Description: {repo_data.get('description', 'No description')}
Recent commits: {len(commits)}

Commit details:
{self._format_commits(commits)}

Please provide a brief summary of the recent development activity in this repository.
Focus on the main changes and patterns in the commit messages.
Keep the summary concise (2-3 sentences).
        """

        logger.info(f"Generating summary for {repo_data['full_name']}, prompt: {prompt}")
        response = await acompletion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content

    def _format_commits(self, commits: List[Dict]) -> str:
        """Format commits for the prompt"""
        return "\n".join(
            f"- {commit['commit']['message']}" 
            for commit in commits
        )

    async def generate_full_report(self, repos_with_commits: List[tuple[Dict, List[Dict]]]) -> str:
        """Generate a full report for all repositories"""
        sections = []
        
        for repo, commits in repos_with_commits:
            if commits:
                summary = await self.generate_repo_summary(repo, commits)
                # Add repository metadata
                repo_info = (
                    f"## [{repo['full_name']}]({repo['html_url']})\n\n"
                    f"⭐ {repo['stargazers_count']} | "
                    f"🔀 {repo['forks_count']} | "
                    f"📝 {repo['language'] or 'N/A'}\n\n"
                    f"{summary}\n\n"
                    f"Recent commits: {len(commits)}\n"
                    f"Last updated: {commits[0]['commit']['committer']['date'] if commits else 'N/A'}\n"
                )
                sections.append(repo_info)
        
        if not sections:
            return "No recent activity found in starred repositories."
            
        return (
            "# Recent Activity in Starred Repositories\n\n"
            "_Generated report of recent development activities in starred repositories_\n\n"
            + "\n".join(sections)
        ) 