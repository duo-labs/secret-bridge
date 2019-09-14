import unittest
import json

from constants import (GITHUB_EVENT_TYPE_HEADER, GITHUB_SIGNATURE_HEADER,
                       WEBHOOK_PUSH_EVENT_TYPE)
from commands.webhook.server import app, generate_event

EXAMPLE_WEBHOOK_EVENT = json.loads('''{
  "ref": "refs/heads/master",
  "before": "68c2560b7047fbad11f4a7b2bbea2bb7b8c79233",
  "after": "e429a3471e63729f93c04a129aa31e592416f359",
  "created": false,
  "deleted": false,
  "forced": false,
  "base_ref": null,
  "compare": "https://github.com/test-leaks/test-repo/compare/68c2560b7047...e429a3471e63",
  "commits": [
    {
      "id": "e429a3471e63729f93c04a129aa31e592416f359",
      "tree_id": "7bca076d8901b22c4c8928badfc910dce969669f",
      "distinct": true,
      "message": "added fake password",
      "timestamp": "2019-08-01T14:52:16-05:00",
      "url": "https://github.com/test-leaks/test-repo/commit/e429a3471e63729f93c04a129aa31e592416f359",
      "author": {
        "name": "Jordan Wright",
        "email": "jwright@duosecurity.com",
        "username": "jordan-wright"
      },
      "committer": {
        "name": "Jordan Wright",
        "email": "jwright@duosecurity.com",
        "username": "jordan-wright"
      },
      "added": [],
      "removed": [],
      "modified": [
        "fake_secrets.py"
      ]
    }
  ],
  "repository": {
    "id": 199934657,
    "node_id": "MDEwOlJlcG9zaXRvcnkxOTk5MzQ2NTc=",
    "name": "test-repo",
    "full_name": "test-leaks/test-repo",
    "private": false,
    "owner": {
      "name": "test-leaks",
      "email": null,
      "login": "test-leaks",
      "id": 52979725,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjUyOTc5NzI1",
      "avatar_url": "https://avatars0.githubusercontent.com/u/52979725?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/test-leaks",
      "html_url": "https://github.com/test-leaks",
      "followers_url": "https://api.github.com/users/test-leaks/followers",
      "following_url": "https://api.github.com/users/test-leaks/following{/other_user}",
      "gists_url": "https://api.github.com/users/test-leaks/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/test-leaks/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/test-leaks/subscriptions",
      "organizations_url": "https://api.github.com/users/test-leaks/orgs",
      "repos_url": "https://api.github.com/users/test-leaks/repos",
      "events_url": "https://api.github.com/users/test-leaks/events{/privacy}",
      "received_events_url": "https://api.github.com/users/test-leaks/received_events",
      "type": "Organization",
      "site_admin": false
    },
    "html_url": "https://github.com/test-leaks/test-repo",
    "description": "A test repository",
    "fork": false,
    "url": "https://github.com/test-leaks/test-repo",
    "forks_url": "https://api.github.com/repos/test-leaks/test-repo/forks",
    "keys_url": "https://api.github.com/repos/test-leaks/test-repo/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/test-leaks/test-repo/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/test-leaks/test-repo/teams",
    "hooks_url": "https://api.github.com/repos/test-leaks/test-repo/hooks",
    "issue_events_url": "https://api.github.com/repos/test-leaks/test-repo/issues/events{/number}",
    "events_url": "https://api.github.com/repos/test-leaks/test-repo/events",
    "assignees_url": "https://api.github.com/repos/test-leaks/test-repo/assignees{/user}",
    "branches_url": "https://api.github.com/repos/test-leaks/test-repo/branches{/branch}",
    "tags_url": "https://api.github.com/repos/test-leaks/test-repo/tags",
    "blobs_url": "https://api.github.com/repos/test-leaks/test-repo/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/test-leaks/test-repo/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/test-leaks/test-repo/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/test-leaks/test-repo/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/test-leaks/test-repo/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/test-leaks/test-repo/languages",
    "stargazers_url": "https://api.github.com/repos/test-leaks/test-repo/stargazers",
    "contributors_url": "https://api.github.com/repos/test-leaks/test-repo/contributors",
    "subscribers_url": "https://api.github.com/repos/test-leaks/test-repo/subscribers",
    "subscription_url": "https://api.github.com/repos/test-leaks/test-repo/subscription",
    "commits_url": "https://api.github.com/repos/test-leaks/test-repo/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/test-leaks/test-repo/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/test-leaks/test-repo/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/test-leaks/test-repo/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/test-leaks/test-repo/contents/{+path}",
    "compare_url": "https://api.github.com/repos/test-leaks/test-repo/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/test-leaks/test-repo/merges",
    "archive_url": "https://api.github.com/repos/test-leaks/test-repo/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/test-leaks/test-repo/downloads",
    "issues_url": "https://api.github.com/repos/test-leaks/test-repo/issues{/number}",
    "pulls_url": "https://api.github.com/repos/test-leaks/test-repo/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/test-leaks/test-repo/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/test-leaks/test-repo/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/test-leaks/test-repo/labels{/name}",
    "releases_url": "https://api.github.com/repos/test-leaks/test-repo/releases{/id}",
    "deployments_url": "https://api.github.com/repos/test-leaks/test-repo/deployments",
    "created_at": 1564610399,
    "updated_at": "2019-08-01T15:22:49Z",
    "pushed_at": 1564689149,
    "git_url": "git://github.com/test-leaks/test-repo.git",
    "ssh_url": "git@github.com:test-leaks/test-repo.git",
    "clone_url": "https://github.com/test-leaks/test-repo.git",
    "svn_url": "https://github.com/test-leaks/test-repo",
    "homepage": null,
    "size": 0,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": "Python",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 0,
    "license": null,
    "forks": 0,
    "open_issues": 0,
    "watchers": 0,
    "default_branch": "master",
    "stargazers": 0,
    "master_branch": "master",
    "organization": "test-leaks"
  },
  "pusher": {
    "name": "jordan-wright",
    "email": "jmwright798@gmail.com"
  },
  "sender": {
    "login": "jordan-wright",
    "id": 1317288,
    "node_id": "MDQ6VXNlcjEzMTcyODg=",
    "avatar_url": "https://avatars3.githubusercontent.com/u/1317288?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/jordan-wright",
    "html_url": "https://github.com/jordan-wright",
    "followers_url": "https://api.github.com/users/jordan-wright/followers",
    "following_url": "https://api.github.com/users/jordan-wright/following{/other_user}",
    "gists_url": "https://api.github.com/users/jordan-wright/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/jordan-wright/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/jordan-wright/subscriptions",
    "organizations_url": "https://api.github.com/users/jordan-wright/orgs",
    "repos_url": "https://api.github.com/users/jordan-wright/repos",
    "events_url": "https://api.github.com/users/jordan-wright/events{/privacy}",
    "received_events_url": "https://api.github.com/users/jordan-wright/received_events",
    "type": "User",
    "site_admin": false
  }
}''')


class TestWebhook(unittest.TestCase):
    def setUp(self):
        app.config['GITHUB_WEBHOOK_SECRET'] = 'test_secret'
        self.app = app.test_client()

    def test_no_event_header(self):
        response = self.app.post('/webhook')
        self.assertEqual(response.status_code, 400)

    def test_ignored_event_type(self):
        response = self.app.post(
            '/webhook', headers={GITHUB_EVENT_TYPE_HEADER: 'IssuesEvent'})
        self.assertEqual(response.status_code, 204)

    def test_no_signature_header(self):
        response = self.app.post(
            '/webhook',
            headers={GITHUB_EVENT_TYPE_HEADER: WEBHOOK_PUSH_EVENT_TYPE})
        self.assertEqual(response.status_code, 400)

    def test_event_generation(self):
        event = generate_event(EXAMPLE_WEBHOOK_EVENT)
        self.assertEqual(len(event.payload['commits']), 1)
        self.assertEqual(event.repo.name,
                         EXAMPLE_WEBHOOK_EVENT['repo']['name'])
        self.assertEqual(event.type, WEBHOOK_PUSH_EVENT_TYPE)
        expected_url = 'https://api.github.com/repos/{}'.format(
            EXAMPLE_WEBHOOK_EVENT['repo']['full_name'])
        self.assertEqual(event.repo.url, expected_url)
