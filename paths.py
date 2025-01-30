import os


env_dir = os.path.expanduser("~")
download_dir = os.path.join(env_dir, 'Downloads')

project_dir = os.path.dirname(os.path.abspath(__file__))
destination_dir = os.path.join(project_dir, 'files')

# Exiba os diretórios para verificação
print(f"env_dir: {env_dir}")
print(f"download_dir: {download_dir}")
print(f"project_dir: {project_dir}")
print(f"destination_dir: {destination_dir}")
