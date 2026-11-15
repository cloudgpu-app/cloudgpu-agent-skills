"""Upload reviewed static files; --dry-run uses no credentials or network."""
import argparse
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copytree, copy2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    with TemporaryDirectory() as temp:
        d = Path(temp)
        copy2(root / 'docs/index.html', d / 'index.html')
        copy2(Path(__file__).with_name('README.md'), d / 'README.md')
        copytree(root / 'docs/assets', d / 'assets')
        copy2(root / 'docs/task-budget.html', d / 'task-budget.html')
        files = [p for p in d.rglob('*') if p.is_file()]
        assert (d / 'assets/read-only-tour.mp4').is_file()
        assert (d / 'assets/tour.vtt').is_file()
        if args.dry_run:
            print(json.dumps({'sdk': 'static', 'files': len(files), 'bytes': sum(p.stat().st_size for p in files), 'network_calls': 0}))
            return
        from huggingface_hub import HfApi
        repo = os.environ['HF_SPACE_ID']  # Explicit owner/space-name, never guessed.
        api = HfApi(token=os.environ['HF_TOKEN'])
        api.create_repo(repo_id=repo, repo_type='space', space_sdk='static', exist_ok=True)
        info = api.space_info(repo)
        if info.sdk != 'static':
            raise SystemExit('Existing Space is not static; refusing to change its compute configuration.')
        api.upload_folder(repo_id=repo, repo_type='space', folder_path=str(d), commit_message='Publish Agent Compute Lab static demo')
    print(f'https://huggingface.co/spaces/{repo}')


if __name__ == '__main__':
    main()
