# Git Stargazer

Git Stargazer automatically tracks and reports activity in your starred GitHub repositories, helping you stay updated with projects you're interested in through daily reports and RSS feeds.

## Features

- 📊 Daily activity reports for your starred repositories
- 📝 Reports in JSON and Markdown formats with commit summaries
- 📡 RSS feed for easy monitoring
- 🤖 Bot activity filtering
- 🎯 Configurable repository limits and time windows
- ⚡ Intelligent caching for optimal GitHub API usage

## Quick Start

1. Fork this repository
2. Set up required secrets:
   - Go to Settings > Secrets and variables > Actions
   - Add `RELEASE_TOKEN`: A GitHub Personal Access Token with `repo` scope
   - Add `DEEPSEEK_API_KEY`: (Optional) For AI-powered commit summaries

3. Configure variables (optional):
   - Go to Settings > Secrets and variables > Actions > Variables
   - `REPO_LIMIT`: Maximum repositories to fetch (default: 100)
   - `EMPTY_REPO_CONSECUTIVE_LIMIT`: Stop after this many consecutive empty repos

## Automated Reports

Reports are automatically generated:
- Daily at 6:30 AM UTC+8 (22:30 UTC previous day)
- On-demand via manual workflow trigger

### Viewing Reports

- Latest report: Available at the "latest" release tag
- Daily archives: Check the "Releases" section
- GitHub Pages: View reports on your fork's GitHub Pages

### Report Formats

- **Markdown Report**: Human-readable activity summary grouped by repository topics
- **JSON Report**: Structured data for programmatic use
- **RSS Feed**: Subscribe to updates in your favorite RSS reader

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
