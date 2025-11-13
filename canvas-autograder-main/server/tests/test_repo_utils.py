import pytest
import os
import shutil
from utils.repo_utils import clone_repo
from git import Repo, GitCommandError


class TestCloneRepo:
    """Tests for repository cloning functionality."""

    def test_clone_valid_repo(self, temp_dir):
        """Test cloning a valid public GitHub repository."""
        # Using a small, stable public repo for testing
        url = "https://github.com/octocat/Hello-World.git"
        repo_dir = os.path.join(temp_dir, "test_repo")

        clone_repo(url, repo_dir)

        # Verify the repo was cloned
        assert os.path.exists(repo_dir)
        assert os.path.isdir(os.path.join(repo_dir, ".git"))

        # Verify it's a valid git repository
        repo = Repo(repo_dir)
        assert not repo.bare

    def test_clone_repo_removes_existing_dir(self, temp_dir):
        """Test that cloning removes existing directory before cloning."""
        url = "https://github.com/octocat/Hello-World.git"
        repo_dir = os.path.join(temp_dir, "test_repo")

        # Create a directory with some content
        os.makedirs(repo_dir)
        dummy_file = os.path.join(repo_dir, "dummy.txt")
        with open(dummy_file, "w") as f:
            f.write("This should be removed")

        # Clone repo should remove the existing directory
        clone_repo(url, repo_dir)

        # Verify old content is gone and repo was cloned
        assert not os.path.exists(dummy_file)
        assert os.path.exists(repo_dir)
        assert os.path.isdir(os.path.join(repo_dir, ".git"))

    def test_clone_invalid_url(self, temp_dir):
        """Test cloning with an invalid repository URL."""
        url = "https://github.com/thisrepodoesnotexist/invalid-repo-12345.git"
        repo_dir = os.path.join(temp_dir, "test_repo")

        with pytest.raises(Exception):
            clone_repo(url, repo_dir)

    def test_clone_malformed_url(self, temp_dir):
        """Test cloning with a malformed URL."""
        url = "not-a-valid-url"
        repo_dir = os.path.join(temp_dir, "test_repo")

        with pytest.raises(Exception):
            clone_repo(url, repo_dir)

    def test_clone_to_nested_path(self, temp_dir):
        """Test cloning to a nested directory path."""
        url = "https://github.com/octocat/Hello-World.git"
        repo_dir = os.path.join(temp_dir, "nested", "path", "test_repo")

        clone_repo(url, repo_dir)

        assert os.path.exists(repo_dir)
        assert os.path.isdir(os.path.join(repo_dir, ".git"))

    def test_clone_repo_preserves_commit_history(self, temp_dir):
        """Test that cloning preserves the commit history."""
        url = "https://github.com/octocat/Hello-World.git"
        repo_dir = os.path.join(temp_dir, "test_repo")

        clone_repo(url, repo_dir)

        repo = Repo(repo_dir)
        commits = list(repo.iter_commits())

        # The Hello-World repo should have multiple commits
        assert len(commits) > 0

    def test_clone_empty_url(self, temp_dir):
        """Test cloning with an empty URL string."""
        url = ""
        repo_dir = os.path.join(temp_dir, "test_repo")

        with pytest.raises(Exception):
            clone_repo(url, repo_dir)

    def test_clone_with_git_extension(self, temp_dir):
        """Test cloning with .git extension in URL."""
        url = "https://github.com/octocat/Hello-World.git"
        repo_dir = os.path.join(temp_dir, "test_repo")

        clone_repo(url, repo_dir)

        assert os.path.exists(repo_dir)
        assert os.path.isdir(os.path.join(repo_dir, ".git"))

    def test_clone_without_git_extension(self, temp_dir):
        """Test cloning without .git extension in URL."""
        url = "https://github.com/octocat/Hello-World"
        repo_dir = os.path.join(temp_dir, "test_repo")

        clone_repo(url, repo_dir)

        assert os.path.exists(repo_dir)
        assert os.path.isdir(os.path.join(repo_dir, ".git"))


class TestCloneRepoEdgeCases:
    """Tests for edge cases in repository cloning."""

    def test_clone_repo_with_special_characters_in_path(self, temp_dir):
        """Test cloning to a path with special characters."""
        url = "https://github.com/octocat/Hello-World.git"
        repo_dir = os.path.join(temp_dir, "test repo with spaces")

        clone_repo(url, repo_dir)

        assert os.path.exists(repo_dir)
        assert os.path.isdir(os.path.join(repo_dir, ".git"))

    def test_clone_repo_idempotency(self, temp_dir):
        """Test that cloning the same repo twice works correctly."""
        url = "https://github.com/octocat/Hello-World.git"
        repo_dir = os.path.join(temp_dir, "test_repo")

        # Clone once
        clone_repo(url, repo_dir)
        assert os.path.exists(repo_dir)

        # Clone again - should remove old and clone fresh
        clone_repo(url, repo_dir)
        assert os.path.exists(repo_dir)
        assert os.path.isdir(os.path.join(repo_dir, ".git"))

    @pytest.mark.slow
    def test_clone_large_repo(self, temp_dir):
        """Test cloning a larger repository (marked as slow test)."""
        # This is a larger repo, so we mark it as slow
        url = "https://github.com/torvalds/linux.git"
        repo_dir = os.path.join(temp_dir, "large_repo")

        # This test is commented out by default as it takes a long time
        # Uncomment if you want to test large repo cloning
        pytest.skip("Skipping large repo test - too slow for regular testing")

        # clone_repo(url, repo_dir)
        # assert os.path.exists(repo_dir)
