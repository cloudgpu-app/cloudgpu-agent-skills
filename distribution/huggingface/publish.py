"""Upload the reviewed static demo using an owner-supplied HF_TOKEN. No GPU Space."""
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copytree, copy2
from huggingface_hub import HfApi
root = Path(__file__).resolve().parents[2]
repo = os.environ['HF_SPACE_ID']  # owner/space-name, explicitly selected by owner
api = HfApi(token=os.environ['HF_TOKEN'])
api.create_repo(repo_id=repo, repo_type='space', space_sdk='static', exist_ok=True)
with TemporaryDirectory() as temp:
    d = Path(temp)
    copy2(root / 'docs/index.html', d / 'index.html')
    copy2(Path(__file__).with_name('README.md'), d / 'README.md')
    copytree(root / 'docs/assets', d / 'assets', ignore=lambda p, names: [n for n in names if n.endswith(('.mp4', '.webm'))])
    api.upload_folder(repo_id=repo, repo_type='space', folder_path=str(d), commit_message='Publish Agent Compute Lab static demo')
print(f'https://huggingface.co/spaces/{repo}')
